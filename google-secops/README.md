# Google SecOps

Google SecOps Antigravity plugin enabling analytics and threat detection.

This directory contains a custom Antigravity (agy) plugin scaffolded with the `agy-plugin-cookiecutter` template.

## Plugin Anatomy

- **Manifest (`plugin.json`)**: Identifies the plugin to the `agy` runtime and registers basic metadata.

- **MCP Config (`mcp_config.json`)**: Connects the agent to the python stdio-based Model Context Protocol server located at `scripts/mcp_server.py`.
- **MCP Server (`scripts/mcp_server.py`)**: Realizes standard JSON-RPC tools (`greet_user`, `system_info`) without needing external package dependencies.


- **Hooks (`hooks/hooks.json`)**: Intercepts actions in the runtime loop. Standard configuration maps a validation utility on `PostToolUse` trigger.


- **Skills (`skills/`)**: Contains executable workflows for the agent:
  - **[`secops-threat-hunter`](skills/secops-threat-hunter/SKILL.md)**: Analyzes security events and drafts target rules.
  - **[`secops-triage`](skills/triage/SKILL.md)**: Expert guidance for security alert triage.
  - **[`secops-investigate`](skills/investigate/SKILL.md)**: Expert guidance for deep security investigations.
  - **[`secops-hunt`](skills/hunt/SKILL.md)**: Expert guidance for proactive threat hunting.
  - **[`secops-cases`](skills/cases/SKILL.md)**: Lists recent SOAR cases.

- **Commands (`commands/`)**: Custom slash shortcuts to trigger workflows:
  - `/secops:cases`
  - `/secops:triage <ALERT_ID>`
  - `/secops:hunt <THREAT>`
  - `/secops:investigate <CASE_ID>`


- **Rules (`rules/`)**: Contains behavioral rules defining guidelines and styles for the agent:
  - **[`secops-quality-gates`](rules/secops-quality-gates.md)**: Custom rules, constraints, and workspace styles.


## Installation

You can install this plugin locally by placing it at either the workspace level or the user global directory:

### 1. Workspace Level Installation (Recommended for project-specific use)
Copy this plugin folder to a folder named `.agents/plugins/` (or `_agents/plugins/`) at the root of your target workspace:
```bash
mkdir -p /path/to/target/workspace/.agents/plugins/
cp -r . /path/to/target/workspace/.agents/plugins/google-secops
```

### 2. User Global Level Installation (Available across all workspaces)
Copy this plugin folder to your home global config directory:
```bash
mkdir -p ~/.gemini/config/plugins/
cp -r . ~/.gemini/config/plugins/google-secops
```

## Management and Testing

The `agy` command-line utility provides commands to manage and test your plugin:

### Validate the Plugin Structure
Verify that your directories, JSON schemas, and frontmatter conform to requirements:
```bash
chmod +x scripts/validate.sh
./scripts/validate.sh
```
Or run the native validator command:
```bash
agy plugin validate .
```

### Check Available Plugins
List the currently loaded plugins to confirm that the agent recognizes your new plugin:
```bash
agy plugin list
```

## Development and Customization

1. **Adding Skills**: Create a new subfolder under `skills/` and put a markdown file `skills/<skill-name>/SKILL.md` containing proper YAML frontmatter headers (`name` and `description`).
2. **Adding Rules**: Create a markdown file at `rules/<rule-name>.md` to enforce custom agent guidelines.
3. **Extending MCP Tools**: Open `scripts/mcp_server.py` and register new python methods under the `self.tools` catalog. If you install the official python `mcp` library via `pip install mcp`, you can switch to the high-level decorator-based SDK example included at the bottom of the script file.
4. **Modifying Hooks**: Edit `hooks.json` to attach command line scripts or plugins to events like `PreToolUse`, `PostToolUse`, `PreThought`, or `PostThought`.

### Pre-commit hooks
Don't forget to configure or verify standard pre-commit hooks for this repository to ensure quality check steps:
```bash
pre-commit install
```
