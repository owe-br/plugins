#!/usr/bin/env python3
"""Run locally: python3 scripts/check-openai-export.py."""

import copy
import io
import json
import runpy
import tempfile
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
exporter = runpy.run_path(str(ROOT / "scripts/export-openai.py"))
assert exporter["OAUTH_EXTENSIONS"] == {
    "com.openai": {"auth": {"type": "oauth", "client": {"mode": "cimd"}}}
}, "The supported auth profile must match OpenAI's documented OAuth/CIMD settings."



def refuses(function, value):
    try:
        function(value)
    except ValueError:
        return
    raise AssertionError("An invalid config or listing was accepted.")


with tempfile.TemporaryDirectory() as temporary:
    destination = Path(temporary)
    plugins = sorted(path.name for path in (ROOT / "plugins").iterdir() if path.is_dir())
    for plugin in plugins:
        source = exporter["plugin_files"](plugin)
        source_mcp = json.loads(source["mcp.json"])
        output = destination / f"{plugin}.zip"
        exporter["export_plugin"](plugin, output, destination / plugin)
        first = output.read_bytes()
        exporter["export_plugin"](plugin, output)
        assert output.read_bytes() == first, "The same source must produce the same ZIP."
        with zipfile.ZipFile(io.BytesIO(first)) as archive:
            assert set(archive.namelist()) == set(source), "Only tracked plugin files belong in the ZIP."
            for name, content in source.items():
                if name != "mcp.json":
                    assert archive.read(name) == content, f"The exporter changed {name}."
            packaged = json.loads(archive.read("mcp.json"))
        portable, profiles = exporter["validation_documents"](packaged)
        assert portable == source_mcp, "The transport must remain unchanged."
        assert profiles and all(profile == exporter["OAUTH_EXTENSIONS"] for profile in profiles)
        assert exporter["plugin_files"](plugin) == source, "The source plugin must remain unchanged."

        server_name = next(iter(source_mcp["mcpServers"]))
        for override in (
            {"headers": {"Authorization": "Bearer do-not-package"}},
            {"url": "https://user:password@example.com/mcp"},
            {"url": "https://example.com/mcp?token=do-not-package"},
            {"type": "stdio"},
        ):
            invalid = copy.deepcopy(source_mcp)
            invalid["mcpServers"][server_name].update(override)
            refuses(exporter["openai_mcp"], invalid)
        for auth in (
            {"type": "oauth", "client": {"mode": "dcr"}},
            {"type": "oauth", "client": {"mode": "cimd", "clientSecret": "do-not-package"}},
            {"type": "api_key"},
            {},
        ):
            invalid = copy.deepcopy(packaged)
            invalid["mcpServers"][server_name]["extensions"]["com.openai"]["auth"] = auth
            refuses(exporter["validation_documents"], invalid)

        manifest = json.loads(source["plugin.json"])
        listing = manifest["extensions"]["com.openai"]["interface"]
        for override in (
            {"shortDescription": "x" * 31},
            {"displayName": "x" * 31},
            {"shortDescription": "Two\nlines"},
            {"category": "Research"},
            {"capabilities": ["x" * 121]},
            {"defaultPrompt": ["a", "b", "c", "d"]},
            {"longDescription": listing["longDescription"] + " The first month is free."},
            {"longDescription": listing["longDescription"] + " Each search costs one credit."},
        ):
            invalid = copy.deepcopy(manifest)
            invalid["extensions"]["com.openai"]["interface"].update(override)
            refuses(exporter["check_listing"], invalid)

print(
    f"Passed: {len(plugins)} exports, unchanged source files, stable ZIPs, and invalid configs and"
    " listings refused."
)
