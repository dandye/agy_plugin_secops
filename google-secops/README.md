# Google SecOps Antigravity Plugin

Google SecOps Antigravity (agy) plugin enabling security analytics, threat triage, investigation, and threat hunting.

## Quick Start

```bash
# Clone the repository
git clone git@depot.code.corp.goog:personal/dandye_agy_plugin_secops.git
cd dandye_agy_plugin_secops

# Install the plugin globally
agy plugin install google-secops
```

> [!IMPORTANT]
> **Tenant Configuration**: The target Google SecOps tenant coordinates and GCP credentials are hardcoded in `google-secops/GEMINI.md` (or `GEMINI.md` within the plugin folder) to use SecOps-Lab. You might want to modify this file to use your own Customer ID, Project ID, and Region.

## Plugin Components

- **Manifest**: `plugin.json` (or `google-secops/plugin.json`)
- **MCP Server**: `scripts/mcp_server.py` (or `google-secops/scripts/mcp_server.py`)
- **Rules**: `rules/secops-quality-gates.md` (or `google-secops/rules/secops-quality-gates.md`)
- **Skills**:
  - `secops-threat-hunter` — Event analysis and rule drafting.
  - `secops-triage` — Alert triage expert guidance.
  - `secops-investigate` — Deep security investigations.
  - `secops-hunt` — Proactive threat hunting.
  - `secops-cases` — List SOAR cases.

## Development

Validate structural integrity and configurations:
```bash
# From the repository root:
agy plugin validate google-secops

# Or from within the google-secops directory:
agy plugin validate .
```
