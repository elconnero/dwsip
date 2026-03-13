from functools import partial
from datetime import datetime
import openai, random, time, os, requests, json, sys
from googleapiclient.discovery import build
from dotenv import load_dotenv
from difflib import SequenceMatcher

#Start of API function Calls
#OpenAI API
def openai_generate_json(user_prompt, openai_api_key):
     openai.api_key = openai_api_key
     response       = openai.completions.create(
         model      = 'gpt-3.5-turbo-instruct', #gpt-4o-mini
         prompt     = 
         """
            IMPORTANT:
                You are a JSON generator. Convert the USER PROMPT into strictly valid JSON using the exact structure provided below. Output JSON only. Do not include explanations, markdown, or any text outside the JSON.

                JSON structure:
                {
                "genres": ["<genre_1>", "<genre_2>"],
                "tags": ["<tag_1>", "<tag_2>"],
                "mood": "<mood>",
                "multiplayer": false,
                "platforms": ["<platform_1>"]
                }

                RULES:
                1. Output must always be strictly valid JSON.
                2. Use only the keys shown in the JSON structure:
                - "genres"
                - "tags"
                - "mood"
                - "multiplayer"
                - "platforms"
                3. Do not add extra keys.
                4. If the USER PROMPT does not provide enough information for a field:
                - use an empty array [] for "genres", "tags", and "platforms"
                - use "" for "mood"
                - use false for "multiplayer" unless the prompt clearly indicates multiplayer, co-op, online play, PvP, MMO, party play, or playing with friends
                5. "genres" must ONLY contain values from the following RAWG genre list:
                
                [action, indie, adventure, rpg, strategy, shooter, casual, simulation, puzzle,
                arcade, platformer, racing, sports, fighting, family, board-games, educational, card]

                Rules:
                - Do not generate genres outside this list.
                - Convert synonyms to the closest RAWG genre.
                Examples:
                "soulslike" → "rpg"
                "fps" → "shooter"
                "driving" → "racing"
                "soccer game" → "sports"
                - Use lowercase.
                - Remove duplicates.
                - If no genre is clear, return an empty array [].
                6. "tags" must contain descriptive game traits, themes, or mechanics, such as:
                - "open-world"
                - "story-rich"
                - "base-building"
                - "crafting"
                - "exploration"
                - "character-customization"
                - "loot"
                - "stealth"
                - "soulslike"
                - "choices-matter"
                - "fast-paced"
                - "cozy"
                - "difficult"
                - "competitive"
                - "singleplayer"
                - "co-op"
                7. "mood" must be a single short lowercase descriptor that best reflects the feeling the user wants, such as:
                - "relaxing"
                - "dark"
                - "intense"
                - "cozy"
                - "competitive"
                - "immersive"
                - "chaotic"
                - "emotional"
                - "mysterious"
                If no mood is clearly implied, return "".
                8. "multiplayer" must be:
                - true if the user clearly wants multiplayer, co-op, online, PvP, MMO, party games, or games to play with friends
                - false otherwise
                9. "platforms" must include only explicitly mentioned or strongly implied gaming platforms, such as:
                - "pc"
                - "playstation"
                - "xbox"
                - "switch"
                - "mobile"
                10. Normalize all values to lowercase.
                11. Remove duplicates from arrays.
                12. Keep array entries short and standardized.
                13. Do not guess specific games.
                14. If the prompt is unrelated to games, still return valid JSON with empty arrays, empty mood, and multiplayer set to false.

                USER PROMPT:
         """
         + user_prompt,
         max_tokens  = 650,
         temperature = 0,
         stop=["}}"]
     )
     openai_response_unrefined = response.choices[0].text.strip()

     #########DELETE###CODE##############DELETE###CODE##############DELETE###CODE#######
    #  print(f"Print of -- openai_response_unrefined:\n{openai_response_unrefined}\nEnd of Data print\n")
    #  input("openai_generate_json system check\nPress any key to continue...")
     #########DELETE###CODE##############DELETE###CODE##############DELETE###CODE#######

     try:
        # Attempt to load the OpenAI response as JSON
        openai_response_refined = json.loads(openai_response_unrefined)
        return openai_response_refined
     except json.JSONDecodeError as e:
        # In case of JSON decoding errors, provide a more detailed error message
        print(f"OPENAI API -> Error decoding JSON: {e}")
        print("Attempting to clean the output...")

        # Optional cleanup for known formatting issues
        # Remove any non-JSON text around the JSON structure
        json_start = openai_response_unrefined.find("{")
        json_end = openai_response_unrefined.rfind("}") + 1
        if json_start != -1 and json_end != -1:
            json_text = openai_response_unrefined[json_start:json_end]
            try:
                openai_response_refined = json.loads(json_text)
                return validate_json_schema
            except json.JSONDecodeError as e_inner:
                return f"Error: Could not decode JSON even after cleaning: {e_inner}"

        # If all else fails, return an error message
        return "OPENAI API -> Unable to parse JSON response."