#!/usr/bin/env python3
"""Build OpenAI uploads from committed, credential-free OAuth remote plugins."""

import argparse
import io
import json
import re
import subprocess
import tarfile
import zipfile
from pathlib import Path, PurePosixPath
from urllib.parse import urlsplit

ROOT = Path(__file__).resolve().parents[1]
MCP_SCHEMA = "https://agent-plugins.org/schemas/1.0.0/mcp.schema.json"
OAUTH_EXTENSIONS = json.loads((ROOT / "schemas/openai-oauth.schema.json").read_text())["const"]
# OpenAI's limits for submitting a listing, from developers.openai.com/plugins/deploy/submission-errors.
# Uploading checks looser ones (a 240-character subtitle passes), so a plugin that uploads can still be
# refused at submission. These are checked here so CI refuses it first.
CATEGORIES = {
    "Productivity", "Creativity", "Developer Tools", "Business & Operations", "Data & Analytics",
    "Communication", "Education & Research", "Security", "Finance", "Healthcare", "Travel",
    "Entertainment", "Other",
}
ONE_LINE_LIMITS = {"displayName": 30, "shortDescription": 30, "developerName": 80}
# ponytail: a word list, not a reader. The listing may not advertise prices, plans, trials or credits,
# and these words are the ones that already drew that finding. OpenAI's review stays the judge.
PRICING_WORDS = re.compile(
    r"\b(free|trials?|discounts?|pricing|subscriptions?|credits?|quotas?|upgrades?|promotions?)\b", re.I
)


def openai_mcp(portable):
    if (
        not isinstance(portable, dict)
        or set(portable) != {"$schema", "mcpServers"}
        or portable["$schema"] != MCP_SCHEMA
    ):
        raise ValueError("Use the portable 1.0 MCP config as the source.")
    servers = portable["mcpServers"]
    if not isinstance(servers, dict) or not servers:
        raise ValueError("The plugin needs at least one OAuth remote server.")
    for name, server in servers.items():
        if not isinstance(server, dict) or set(server) != {"type", "url"}:
            raise ValueError(f"{name}: only a remote transport and URL can be exported.")
        if server["type"] not in ("streamable-http", "sse"):
            raise ValueError(f"{name}: local MCP servers cannot use this OAuth exporter.")
        if not isinstance(server["url"], str):
            raise ValueError(f"{name}: the MCP URL must be a string.")
        url = urlsplit(server["url"])
        if url.scheme != "https" or not url.hostname or url.username or url.password:
            raise ValueError(f"{name}: use an HTTPS URL without credentials.")
        if url.query or url.fragment:
            raise ValueError(f"{name}: remove query parameters and fragments from the MCP URL.")
    return {
        **portable,
        "mcpServers": {
            name: {**server, "extensions": OAUTH_EXTENSIONS} for name, server in servers.items()
        },
    }


def validation_documents(packaged):
    portable = {**packaged, "mcpServers": {}}
    extensions = []
    for name, server in packaged["mcpServers"].items():
        transport = {**server}
        profile = transport.pop("extensions", None)
        if profile != OAUTH_EXTENSIONS:
            raise ValueError(f"{name}: the OpenAI OAuth metadata does not match the documented profile.")
        portable["mcpServers"][name] = transport
        extensions.append(profile)
    openai_mcp(portable)
    return portable, extensions


def check_listing(manifest):
    listing = manifest.get("extensions", {}).get("com.openai", {}).get("interface")
    if not isinstance(listing, dict):
        raise ValueError("plugin.json needs extensions.com.openai.interface for the OpenAI listing.")
    for field, limit in {**ONE_LINE_LIMITS, "longDescription": 4000}.items():
        value = listing.get(field)
        if not isinstance(value, str) or not value.strip():
            raise ValueError(f"interface.{field} is required.")
        if len(value) > limit:
            raise ValueError(f"interface.{field} is {len(value)} characters. OpenAI's limit is {limit}.")
        if field in ONE_LINE_LIMITS and "\n" in value:
            raise ValueError(f"interface.{field} must fit on one line.")
    if listing.get("category") not in CATEGORIES:
        raise ValueError(
            f"interface.category {listing.get('category')!r} is not one of OpenAI's: "
            + ", ".join(sorted(CATEGORIES))
            + "."
        )
    capabilities = listing.get("capabilities", [])
    if len(capabilities) > 20 or any(len(capability) > 120 for capability in capabilities):
        raise ValueError("interface.capabilities takes at most 20 entries of 120 characters each.")
    prompts = listing.get("defaultPrompt", [])
    prompts = [prompts] if isinstance(prompts, str) else prompts
    if len(prompts) > 3 or any(len(prompt) > 128 for prompt in prompts):
        raise ValueError("interface.defaultPrompt takes at most 3 prompts of 128 characters each.")
    text = " ".join([listing["shortDescription"], listing["longDescription"], *capabilities])
    found = sorted({word.lower() for word in PRICING_WORDS.findall(text)})
    if found:
        raise ValueError(
            f"The listing says {', '.join(found)}. OpenAI refuses prices, plans, trials and credits there."
        )


def plugin_files(plugin):
    if not re.fullmatch(r"[a-z0-9]+(?:[.-][a-z0-9]+)*", plugin):
        raise ValueError("Use a plugin name, such as featury.")
    archive = subprocess.run(
        ["git", "-C", str(ROOT), "archive", "--format=tar", f"HEAD:plugins/{plugin}"],
        check=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    ).stdout
    files = {}
    with tarfile.open(fileobj=io.BytesIO(archive)) as source:
        for member in source:
            if member.isdir():
                continue
            path = PurePosixPath(member.name)
            if not member.isfile() or path.is_absolute() or ".." in path.parts:
                raise ValueError(f"{member.name}: only regular files inside the plugin can be exported.")
            if any(part.startswith(".env") or ".bak-" in part for part in path.parts):
                raise ValueError(f"{member.name}: environment files and backups cannot be exported.")
            if path.suffix.lower() in (".key", ".pem", ".p12", ".pfx"):
                raise ValueError(f"{member.name}: key files cannot be exported.")
            with source.extractfile(member) as content:
                files[member.name] = content.read()
    return files


def export_plugin(plugin, output, validation_dir=None):
    files = plugin_files(plugin)
    try:
        check_listing(json.loads(files["plugin.json"]))
    except ValueError as error:
        raise ValueError(f"{plugin}: {error}") from None
    files["mcp.json"] = (
        json.dumps(openai_mcp(json.loads(files["mcp.json"])), indent=2) + "\n"
    ).encode()
    archive = io.BytesIO()
    with zipfile.ZipFile(archive, "w", compression=zipfile.ZIP_DEFLATED) as target:
        for name, content in sorted(files.items()):
            entry = zipfile.ZipInfo(name, date_time=(1980, 1, 1, 0, 0, 0))
            entry.compress_type = zipfile.ZIP_DEFLATED
            entry.external_attr = 0o100644 << 16
            target.writestr(entry, content)
    with zipfile.ZipFile(archive) as packaged:
        portable, extensions = validation_documents(json.loads(packaged.read("mcp.json")))
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_bytes(archive.getvalue())
    if validation_dir is not None:
        validation_dir.mkdir(parents=True, exist_ok=True)
        (validation_dir / "transport.json").write_text(json.dumps(portable, indent=2) + "\n")
        for index, profile in enumerate(extensions):
            (validation_dir / f"auth-{index}.json").write_text(json.dumps(profile, indent=2) + "\n")
    return output


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("plugin", help="OAuth remote plugin name, such as featury")
    parser.add_argument("--output", type=Path, help="ZIP path; defaults to dist/<plugin>-openai-plugin.zip")
    parser.add_argument("--validation-dir", type=Path, help="Write transport and auth JSON for schema checks")
    args = parser.parse_args()
    output = args.output or ROOT / "dist" / f"{args.plugin}-openai-plugin.zip"
    try:
        export_plugin(args.plugin, output, args.validation_dir)
    except subprocess.CalledProcessError as error:
        parser.error(error.stderr.decode().strip())
    except (ValueError, KeyError, OSError) as error:
        parser.error(str(error))
    print(output)


if __name__ == "__main__":
    main()
