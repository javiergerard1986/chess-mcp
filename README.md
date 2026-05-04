# MCP Chess.com Server

MCP server exposing Chess.com public API data to Claude Desktop.

## Why Claude Desktop was returning 403

Chess.com may reject API requests that use the default Python `requests` user agent. When this MCP server is launched by Claude Desktop, every tool call goes through `src/chess/chess_api.py`, so the rejected Chess.com HTTP response is surfaced back to Claude as a 403.

The API client now sends an explicit `User-Agent` and `Accept: application/json` header for every Chess.com request.

## Optional Claude Desktop configuration

To run this server from the GitHub repository with Claude Desktop, use `uvx --from` with a `git+https://` URL:

```json
{
  "mcpServers": {
    "chess": {
      "command": "uvx",
      "args": [
        "--from",
        "git+https://github.com/javiergerard1986/chess-mcp.git",
        "chess"
      ],
      "env": {
        "CHESS_API_USER_AGENT": "your-name chess-mcp contact@example.com"
      }
    }
  }
}
```

Important: Git repository dependencies must use the `git+` prefix. This is valid:

```text
git+https://github.com/javiergerard1986/chess-mcp.git
```

This is not valid for `uvx --from`:

```text
https://github.com/javiergerard1986/chess-mcp
```

If you prefer running from your local checkout instead, use:

```json
{
  "mcpServers": {
    "chess": {
      "command": "uv",
      "args": [
        "--directory",
        "d:\\Repositories\\MCP\\code\\quickstart\\MCP-BUILD-CHESS-SERVER",
        "run",
        "chess"
      ],
      "env": {
        "CHESS_API_USER_AGENT": "your-name chess-mcp contact@example.com"
      }
    }
  }
}
```

In either config, replace `your-name chess-mcp contact@example.com` with an identifier/contact appropriate for you. Restart Claude Desktop completely after changing the config.

## Local verification

From this repository:

```powershell
$env:PYTHONPATH='src'
python -c "from chess.chess_api import get_player_profile; print(get_player_profile('hikaru')['username'])"
```

If that command returns the username without an HTTP error, the Chess.com request path is working.