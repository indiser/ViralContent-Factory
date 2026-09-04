from curl_cffi import requests
import json
import random
import os
import re
import html
from dotenv import load_dotenv
from langdetect import detect, LangDetectException
from llm_router import chat_fast, chat_strong
from datetime import datetime
import ctypes
import time
from requests.exceptions import RequestException
load_dotenv()

def prevent_sleep():
    if os.name == 'nt':
        try:
            ctypes.windll.kernel32.SetThreadExecutionState(0x80000000 | 0x00000001)
        except: pass

prevent_sleep()

script_dir=os.path.dirname(os.path.abspath(__file__))
file_path=os.path.join(script_dir,"scripts.json")
database = []
existing_ids = set()

with open("cookies.json", "r", encoding="utf-8") as filp:
    raw_cookies = json.load(filp)

if os.path.exists(file_path):
    with open(file_path, "r", encoding="UTF-8") as filp:
        try:
            database = json.load(filp)
            existing_ids = {item["id"] for item in database}
        except json.JSONDecodeError:
            # Failsafe: If the file is corrupted, wipe it and start fresh.
            print("WARNING: Database corrupted. Starting fresh.")


LIMIT = 1000
# 1. Define your fallback hierarchy
SUBREDDITS = [
    "AmItheAsshole",
    "AITAH",               # The uncensored alternative to AITA
    "TrueOffMyChest",
    "confessions",
    "confession",
    "tifu",
    "pettyrevenge",        # High-satisfaction payoff stories
    "entitledparents",     # Massive engagement and rage-bait
    "MaliciousCompliance", # Clever revenge stories
    "EntitledPeople",
    "relationships",
    "relationship_advice",
    "Vent",
    "stories",
    "moraldilemmas",
    "EntitledPeople",
    "self",
    "PointlessStories",
    "TwoHotTakes",
    "dating",
    "offmychest",
    "UnsentLetters",
    "SeriousConversation",
    "Adulting",
    "lonely",
    "BreakUps",
    "TalesFromTheFrontDesk",
    "legaladvice",
    "RBI",
    "UnresolvedMysteries",
    "Glitch_in_the_Matrix",
    "raisedbynarcissists",
    "dadjokes",
    "Jokes"
]

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Accept": "application/json",
    "Accept-Language": "en-US,en;q=0.9",
    "Sec-Ch-Ua": '"Not_A Brand";v="8", "Chromium";v="120", "Google Chrome";v="120"',
    "Sec-Ch-Ua-Mobile": "?0",
    "Sec-Ch-Ua-Platform": '"Windows"',
}

COOKIES = {cookie['name'] : cookie['value'] for cookie in raw_cookies}

session = requests.Session(impersonate="chrome120")
session.cookies.update(COOKIES)
session.headers.update(HEADERS)

def sanitize_text(raw_text: str) -> str:
    text=html.unescape(raw_text)
    # 1. Strip rogue URLs first
    text = re.sub(r'http\S+', '', raw_text)
    text = re.sub(r'\b[ru]/[A-Za-z0-9_-]+\b', '', text)
    text = re.sub(r'(?i)\bTL;?DR\b.*', '', text, flags=re.DOTALL)
    text = re.sub(r'(?i)\bEdit:? ?\d?\b.*', '', text, flags=re.DOTALL)
    text = re.sub(r'(?i)\bUpdate:? ?\d?\b.*', '', text, flags=re.DOTALL)
    text = re.sub(r'[*_~•▪●\t]', ' ', text)
    text = re.sub(r' +', ' ', text).strip()

    # 2. Dynamic Age/Gender Translation (e.g., "19F" -> "a 19 year old female")
    text = re.sub(r'\b(\d{2})[Ff]\b', r'a \1 year old woman', text)
    text = re.sub(r'\b(\d{2})[Mm]\b', r'a \1 year old man', text)
    text = re.sub(r'\b[Ff](\d{2})\b', r'a \1 year old woman', text)
    text = re.sub(r'\b[Mm](\d{2})\b', r'a \1 year old man', text)
    

    # 3. The Master Acronym Dictionary
    slang_map = {
        "AITA": "Am I the jerk",
        "AITAH": "Am I the jerk here",
        "WIBTA": "Would I be the jerk",
        "TIFU": "Today I messed up",
        "MC": "Malicious compliance",
        "gf": "girlfriend",
        "bf": "boyfriend",
        "MIL": "mother in law",
        "FIL": "father in law",
        "SIL": "sister in law",
        "BIL": "brother in law",
        "EM": "entitled mom",
        "ED": "entitled dad",
        "EK": "entitled kid",
        "EP": "entitled parent",
        "OP": "the original poster",
        "idk": "I don't know",
        "tbh": "to be honest",
        "btw": "by the way",
        "tf": "the heck",
        "wtf": "what the heck"
    }
    
    # 4. Apply Word-Boundary Replacements
    for slang, replacement in slang_map.items():
        # \b ensures 'gf' doesn't trigger inside other words
        # re.IGNORECASE handles 'aita', 'AITA', and 'Aita' automatically
        pattern = r'\b' + re.escape(slang) + r'\b'
        text = re.sub(pattern, replacement, text, flags=re.IGNORECASE)
        
    return text

def rank_best_hook(original_title: str, ai_hook: str) -> str:
    """Acts as a ruthless A/B tester to select the most viral hook."""
    
    # If the AI failed to generate a hook earlier and returned the title, skip the API call.
    if original_title == ai_hook:
        return original_title
        
    system_prompt = (
        "You are a ruthless TikTok retention strategist. I will give you Option A and Option B for a video hook. "
        "Your job is to pick the hook that creates the highest 'curiosity gap' and emotional shock value. "
        "Option A is the raw human title. Option B is an AI-optimized hook. "
        "Evaluate both objectively based on human psychology. Do not automatically favor the AI. "
        "YOU MUST REPLY WITH EXACTLY ONE LETTER: 'A' for Option A, or 'B' for Option B. DO NOT OUTPUT ANY OTHER TEXT."
    )
    
    user_prompt = f"Option A: {original_title}\n\nOption B: {ai_hook}"


    try:
        winner = chat_fast(system_prompt, user_prompt).strip().upper()
        
        if winner == "A":
            print(f"JUDGE DECISION: Human Title Wins.")
            return original_title
        elif winner == "B":
            print(f"JUDGE DECISION: AI Hook Wins.")
            return ai_hook
        else:
            return ai_hook 
    except Exception as e:
        print(f"Hook Ranking Failed: {e}. Defaulting to AI Hook.")
        return ai_hook

def generate_seo_tags(story_text: str) -> list:
    """Forces the LLM to extract exactly 5 hyper-relevant SEO keywords."""
    context_chunk = story_text[:1000]
    
    system_prompt = (
        "You are an expert YouTube SEO strategist. Read the following story context and extract exactly 5 highly relevant keywords for YouTube tags. "
        "RULES:\n"
        "1. Output ONLY a comma-separated list of 5 words or short phrases.\n"
        "2. Do NOT use hashtags (#).\n"
        "3. Always include 'reddit' and 'storytime' as two of the tags.\n"
        "4. No introductory text, no quotes, no explanations."
    )
    user_prompt = context_chunk

    try:
        raw_tags = chat_fast(system_prompt, user_prompt)
        tag_list = [tag.strip().strip('"\'') for tag in raw_tags.split(',')]
        
        if len(tag_list) < 2:
            raise ValueError("LLM returned malformed tags.")
        return tag_list
    except Exception as e:
        print(f"SEO Tag Generation Failed: {e}. Defaulting to static tags.")
        return ["reddit", "storytime", "aita", "drama", "redditstories"]
    
def detect_gender_llm(title: str, story_text: str) -> str:
    """Uses a free LLM to semantically infer the narrator's gender."""
    
    # We only need the first ~1000 characters to get the context. 
    # Sending the whole story wastes tokens.
    context_chunk = story_text
    
    # The Prompt Engineering: Strict constraints.
    system_prompt = (
        "You are a text analyzer. Read the following Reddit story and determine the gender of the narrator (the 'I' character). "
        "Look for explicit tags (like 19F) OR context clues (like 'my husband', 'my boyfriend', 'pregnant', etc). "
        "If it is completely ambiguous, guess based on the statistical likelihood of the writing style. "
        "YOU MUST REPLY WITH EXACTLY ONE LETTER: 'M' for Male, or 'F' for Female. DO NOT OUTPUT ANY OTHER TEXT."
    )

    user_prompt = f"Title: {title}\n\nStory: {context_chunk}"


    try:
        # Route to cheap/fast models
        ai_guess = chat_fast(system_prompt, user_prompt).strip().upper()
        if ai_guess in ["M", "F"]:
            return ai_guess
        else:
            print(f"WARNING: LLM hallucinated an invalid response: {ai_guess}. Defaulting to F.")
            return "F"
    except Exception as e:
        print(f"LLM Gender Detection Failed: {e}. Defaulting to F.")
        return "F"

def generate_viral_hook(title: str, story_text: str) -> str:
    """Forces the LLM to rewrite a boring Reddit title into a high-retention hook."""
    context_chunk = story_text[:1000]
    
    system_prompt = (
        "You are a ruthless viral copywriter for TikTok, Intagram reels and YouTube Shorts. "
        "Read the following Reddit title and story. Your job is to rewrite the title into a highly engaging, "
        "dramatic, and aggressive hook that will stop people from scrolling. "
        "RULES: \n"
        "1. It MUST be under 12 words.\n"
        "2. DO NOT EVER start the hook with 'Am I the jerk' or 'Am I the asshole'. That is banned.\n"
        "3. Use a variety of psychological triggers. Start directly with the action (e.g., 'I destroyed my...', 'My insane mother...', 'Why I refused to...', 'The biggest mistake I...').\n"
        "4. DO NOT use hashtags, emojis, or quotation marks.\n"
        "5. Output ONLY the hook. Absolutely no other text."
    )
    user_prompt = f"Title: {title}\n\nStory: {context_chunk}"

    try:
        # Route to strong/creative models
        raw_hook = chat_strong(system_prompt, user_prompt)
        hook = raw_hook.strip().replace('"', '').replace('*', '')
        
        if len(hook.split()) > 20:
            return title
        return hook
    except Exception as e:
        print(f"LLM Hook Generation Failed: {e}. Defaulting to original title.")
        return title
    
def fetch_brainrot_story(subreddit_name: str, existing_ids:set ) -> dict:
    try:
        api_url = f"https://www.reddit.com/r/{subreddit_name}/top.json?t=day&limit={LIMIT}"
        time.sleep(5);
        response = session.get(url= api_url)
        response.raise_for_status()
        data = response.json()
    except requests.exceptions.HTTPError as e:
        print(f"HTTP Error on {subreddit_name}: {e}")
        raise RuntimeError(f"HTTP Error: {e}")
    except RequestException as e:
        print(f"Network drop on {subreddit_name}: {e}")
        raise RuntimeError(f"Network Error: {e}")

    for child in data['data']['children']:
        id = child['data']['id']
        original_story = child['data']['selftext']
        original_title = child['data']['title']
        url = child['data']['url']
        words = original_story.split()
        story=sanitize_text(original_story)
        title=sanitize_text(original_title)
        
        if id in existing_ids:
            print(f"Skipping {id}: Already exists in database.")
            continue # Skip to the next story immediately

        if story in ["[removed]", "[deleted]", ""]:
            continue
        
        if 120 < len(words) < 380:
            try:
                # If the library detects anything other than English ('en'), we dump it.
                if detect(story) != 'en':
                    print(f"Skipping {id}: Foreign language detected.")
                    continue
            except LangDetectException:
                # If the text is so corrupted it can't figure out the language, trash it.
                print(f"Skipping {id}: Unreadable text format.")
                continue
            
            pov_gender = detect_gender_llm(title=title,story_text=story)
            ai_generated_hook = generate_viral_hook(title=title, story_text=story)
            winning_hook=rank_best_hook(original_title=title.replace("\n\n"," ").replace("\n"," "),ai_hook=ai_generated_hook)
            dynamic_tags=generate_seo_tags(story_text=story)
            print(f"Voice assigned: {pov_gender}")
            print(f"Final Hook Selected: {winning_hook}")
            return {
                "id" : id,
                "original_title": original_title,
                "title": title.replace("\n\n"," ").replace("\n"," "),
                "hook": winning_hook, 
                "original_story": original_story,
                "story": story.replace("\n\n"," ").replace("\n"," ").replace('\"',"").replace("\\","").replace('/',""),
                "gender": pov_gender,
                'tags': dynamic_tags,
                "url" : url,
                "time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "posted_youtube": False,
                "posted_instagram": False,
                "posted_tiktok": False,
                "posted_facebook": False,    # Future
                "posted_snapchat": False,    # Future
                "posted_twitter": False,     # Future
                "posted_linkedin": False    
            }
            
    # If the loop finishes without returning, raise the alarm.
    raise ValueError(f"No viable stories found in r/{subreddit_name}.")


# --- The Master Execution (The Waterfall) ---

def load_from_local_database() -> dict:
    if not os.path.exists(file_path):
        raise FileNotFoundError("CRITICAL: Backlog missing.")
        
    with open(file_path, "r", encoding="UTF-8") as filp:
        database = json.load(filp)
    
    if all(item.get("used", True) for item in database):
        print("WARNING: Backlog exhausted. Resetting flags.")
        for item in database:
            item["used"] = False
        
    for item in database:
        if item.get("used") is False:
            item["used"] = True 
            
            # Save the mutated state back to the disk
            with open(file_path, "w", encoding="UTF-8") as filp:
                json.dump(database, filp, indent=4, ensure_ascii=False)
                
            return {"id": item["id"], "title": item["title"], "story": item["story"]}
            
    raise ValueError("FATAL: Backlog is completely empty.")


