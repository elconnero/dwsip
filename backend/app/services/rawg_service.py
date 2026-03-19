import httpx
from app.config import RAWG_API_KEY
from app.schemas.prompt import GameFilters

RAWG_BASE_URL = "https://api.rawg.io/api"

PLATFORM_MAP = {
    "pc":          [4],
    "playstation": [187, 18],
    "xbox":        [186, 1],
    "switch":      [7],
    "mobile":      [3, 21],
}

VALID_TAGS = {
    # Mechanics
    "open-world", "exploration", "crafting", "base-building", "loot", "stealth",
    "choices-matter", "character-customization", "soulslike", "roguelike", "survival",
    "puzzle", "sandbox", "strategy",
    # Feel
    "story-rich", "atmospheric", "fast-paced", "cozy", "difficult", "relaxing",
    "casual", "emotional", "immersive",
    # Social
    "singleplayer", "co-op", "multiplayer", "competitive",
    # Setting
    "space", "sci-fi", "fantasy", "dark-fantasy", "horror", "post-apocalyptic",
    "cyberpunk", "historical", "mythology", "aliens", "futuristic", "anime",
}

def fetch_games(filters: GameFilters, page_size: int = 3) -> list[dict]:
    params = {
        "key":       RAWG_API_KEY,
        "page_size": page_size,
        "ordering":  "-rating",
    }

    if filters.search_query:
        params["search"] = filters.search_query

    if filters.genres:
        params["genres"] = ",".join(filters.genres)

    tags = [t for t in filters.tags if t in VALID_TAGS]
    if filters.multiplayer:
        tags.append("multiplayer")
    if tags:
        params["tags"] = ",".join(tags)

    if filters.platforms:
        platform_ids = []
        for p in filters.platforms:
            platform_ids.extend(PLATFORM_MAP.get(p, []))
        if platform_ids:
            params["platforms"] = ",".join(str(i) for i in platform_ids)

    with httpx.Client() as client:
        response = client.get(f"{RAWG_BASE_URL}/games", params=params)
        response.raise_for_status()
        return response.json().get("results", [])
