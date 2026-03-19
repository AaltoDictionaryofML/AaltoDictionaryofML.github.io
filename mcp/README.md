# ADictML MCP Server

Exposes the Aalto Dictionary of Machine Learning as a
[Model Context Protocol](https://modelcontextprotocol.io/) server,
so AI coding assistants (Claude Code, VS Code Copilot, etc.) can
look up, search, and explore dictionary terms in context.

## Tools

| Tool | Description |
|---|---|
| `list_all_terms` | List all terms, optionally filtered by category |
| `lookup_term` | Full definition by key or display name |
| `search_terms` | Fuzzy/keyword search across names and descriptions |
| `get_related_terms` | Explore cross-references via the `see` field |

## Setup

### 1. Install dependency

```bash
pip install -r mcp/requirements.txt
```

### 2a. Claude Code

```bash
# Register user-scoped (available in all projects)
claude mcp add --scope user aalto-dictionary \
  -- python ~/AaltoDictionaryofML.github.io/mcp/server.py

# Verify inside a Claude Code session:
# /mcp  →  aalto-dictionary: connected
```

### 2b. VS Code (Copilot / GitHub Copilot Chat)

Add the following entry to your VS Code MCP config file:

- **macOS:** `~/Library/Application Support/Code/User/mcp.json`
- **Linux:** `~/.config/Code/User/mcp.json`
- **Windows:** `%APPDATA%\Code\User\mcp.json`

```json
{
  "servers": {
    "aalto-dictionary": {
      "type": "stdio",
      "command": "python",
      "args": ["~/AaltoDictionaryofML.github.io/mcp/server.py"]
    }
  }
}
```

Then open the Copilot Chat panel — the `aalto-dictionary` server will be listed under available tools.

## Usage in Claude Code

```
Look up "Byzantine robustness" in the Aalto Dictionary
Search the Aalto Dictionary for differential privacy
List all Regulation terms in the Aalto Dictionary
What terms are related to federated learning?
```

## Configuration

By default the server derives the repo root from its own file location
(`mcp/server.py` → parent directory). To override, set:

```bash
export ADDICTML_REPO=/path/to/custom/location
```

## Categories

- **ML Concepts** — `ADictML_CoreML.tex`
- **Math** — `ADictML_Math.tex`
- **ML Systems** — `ADictML_MLSystems.tex`
- **Reinforcement Learning** — `ADictML_RL.tex`
- **Regulation** — `ADictML_Regulation.tex`

The server reloads entries on each startup, so a `git pull` is enough
to pick up new terms.
