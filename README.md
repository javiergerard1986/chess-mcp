# MCP Chess.com Server

MCP server exposing Chess.com public API data to Claude Desktop.

## Why Claude Desktop was returning 403

Chess.com may reject API requests that use the default Python `requests` user agent. When this MCP server is launched by Claude Desktop, every tool call goes through `src/chess/chess_api.py`, so the rejected Chess.com HTTP response is surfaced back to Claude as a 403.

The API client now sends an explicit `User-Agent` and `Accept: application/json` header for every Chess.com request.

## Optional Claude Desktop configuration

If Chess.com still returns 403, set a more specific user agent in your Claude Desktop MCP server config and restart Claude Desktop completely:

```json
{
  "mcpServers": {
    "chess": {
      "command": "uv",
      "args": ["run", "chess"],
      "cwd": "d:\\Repositories\\MCP\\code\\quickstart\\MCP-BUILD-CHESS-SERVER",
      "env": {
        "CHESS_API_USER_AGENT": "your-name chess-mcp contact@example.com"
      }
    }
  }
}
```

Replace `your-name chess-mcp contact@example.com` with an identifier/contact appropriate for you.

## Local verification

From this repository:

```powershell
$env:PYTHONPATH='src'
python -c "from chess.chess_api import get_player_profile; print(get_player_profile('hikaru')['username'])"
```

If that command returns the username without an HTTP error, the Chess.com request path is working.