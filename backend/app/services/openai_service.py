import json
from openai import OpenAI
from app.config import OPENAI_API_KEY

client = OpenAI(api_key=OPENAI_API_KEY)

SYSTEM_PROMPT = """
You are a JSON generator. Convert the USER PROMPT into strictly valid JSON using the exact structure provided below. Output JSON only. Do not include explanations, markdown, or any text outside the JSON.

JSON structure:
{
  "genres": ["<genre_1>", "<genre_2>"],
  "tags": ["<tag_1>", "<tag_2>"],
  "mood": "<mood>",
  "multiplayer": false,
  "platforms": ["<platform_1>"],
  "search_query": "<2-4 word theme phrase>",
  "predicted_game": "<single game title or null>"
}

RULES:
1. Output must always be strictly valid JSON.
2. Use only the keys shown in the JSON structure: "genres", "tags", "mood", "multiplayer", "platforms"
3. Do not add extra keys.
4. If the USER PROMPT does not provide enough information for a field:
   - use an empty array [] for "genres", "tags", and "platforms"
   - use "" for "mood"
   - use false for "multiplayer" unless the prompt clearly indicates multiplayer, co-op, online play, PvP, MMO, party play, or playing with friends
5. "genres" must ONLY contain values from the following RAWG genre list:
   [action, indie, adventure, rpg, strategy, shooter, casual, simulation, puzzle,
   arcade, platformer, racing, sports, fighting, family, board-games, educational, card]
   - Do not generate genres outside this list.
   - Convert synonyms to the closest RAWG genre.
   Examples: "soulslike" -> "rpg", "fps" -> "shooter", "driving" -> "racing", "soccer game" -> "sports"
   - Use lowercase. Remove duplicates. If no genre is clear, return [].
6. "tags" must contain descriptive game traits, themes, or mechanics. Always include setting/theme
   tags when the user describes a world or setting (e.g. if they mention space, include "space" and "sci-fi").
   Use slugs from this list:
   - Mechanics:  "open-world", "exploration", "crafting", "base-building", "loot", "stealth",
                 "choices-matter", "character-customization", "soulslike", "roguelike", "survival",
                 "puzzle", "sandbox", "strategy"
   - Feel:       "story-rich", "atmospheric", "fast-paced", "cozy", "difficult", "relaxing",
                 "casual", "emotional", "immersive"
   - Social:     "singleplayer", "co-op", "multiplayer", "competitive"
   - Setting:    "space", "sci-fi", "fantasy", "dark-fantasy", "horror", "post-apocalyptic",
                 "cyberpunk", "historical", "mythology", "aliens", "futuristic", "anime"
7. "mood" must be a single short lowercase descriptor: "relaxing", "dark", "intense",
   "cozy", "competitive", "immersive", "chaotic", "emotional", "mysterious"
   If no mood is clearly implied, return "".
8. "multiplayer": true if the user clearly wants multiplayer/co-op/online/PvP/MMO/party games, false otherwise.
9. "platforms" must include only explicitly mentioned or strongly implied platforms:
   "pc", "playstation", "xbox", "switch", "mobile"
10. Normalize all values to lowercase. Remove duplicates. Keep array entries short and standardized.
11. "predicted_game" must be the single most likely real game title the user is describing, based on the full context of their prompt. Use your knowledge of games to make a confident prediction. If the prompt is too vague or generic to identify a specific game, return null.
12. If the prompt is unrelated to games, return valid JSON with empty arrays, empty mood, and multiplayer: false.
13. "search_query" must be a short 2-4 word English phrase capturing the core theme or setting of
    the prompt, suitable as a game database text search. This is the most important field for
    finding relevant results — make it specific and descriptive.
    Examples:
    "I want a cozy space exploration game" -> "space exploration"
    "Something dark and scary like resident evil" -> "survival horror"
    "Open world fantasy RPG with magic" -> "open world fantasy"
    "Fast paced shooter with friends" -> "multiplayer shooter"
    If no clear theme, return "".
"""

def openai_generate_json(user_prompt: str) -> dict:
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": user_prompt},
        ],
        response_format={"type": "json_object"},
        max_tokens=650,
        temperature=0,
    )
    return json.loads(response.choices[0].message.content)
