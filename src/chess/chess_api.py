# Chess.com API wrapper for MCP server
# This file provides helper functions to interact with the Chess.com public API.
import os

import requests

CHESS_API_BASE = "https://api.chess.com/pub"

# Chess.com rejects many requests made with the default Python requests
# User-Agent, which shows up most often when the server is launched by Claude
# Desktop instead of an interactive terminal. Send an identifiable User-Agent as
# requested by the Chess.com public API guidance.
HEADERS = {
    "User-Agent": os.getenv(
        "CHESS_API_USER_AGENT",
        "mcp-build-chess-server/0.1.0 (MCP Chess.com client)",
    ),
    "Accept": "application/json",
}

TIMEOUT_SECONDS = 15


def _get_json(path):
    url = f"{CHESS_API_BASE}{path}"
    response = requests.get(url, headers=HEADERS, timeout=TIMEOUT_SECONDS)

    try:
        response.raise_for_status()
    except requests.HTTPError as exc:
        raise requests.HTTPError(
            f"Chess.com API request failed with HTTP {response.status_code} for {url}. "
            "If this is a 403, verify the request includes an identifiable "
            "User-Agent and try again later if Chess.com is rate-limiting or blocking traffic.",
            response=response,
        ) from exc

    return response.json()


def get_player_profile(username):
    return _get_json(f"/player/{username}")


def get_player_stats(username):
    return _get_json(f"/player/{username}/stats")


def get_player_is_online(username):
    return _get_json(f"/player/{username}/is-online")


def get_player_current_games(username):
    return _get_json(f"/player/{username}/games")
