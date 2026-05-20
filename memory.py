import json
import os
from datetime import datetime

MEMORY_FILE = "memory.json"

def load_memory():
    """Loads the memory from the JSON file."""
    if not os.path.exists(MEMORY_FILE):
        return {"past_topics": [], "content_history": []}
    
    with open(MEMORY_FILE, "r") as f:
        try:
            return json.load(f)
        except json.JSONDecodeError:
            return {"past_topics": [], "content_history": []}

def save_memory(memory_data):
    """Saves the memory to the JSON file."""
    with open(MEMORY_FILE, "w") as f:
        json.dump(memory_data, f, indent=4)

def add_to_memory(topic, platform, niche, script, hashtags):
    """Adds a newly created content piece to the memory."""
    memory = load_memory()
    
    entry = {
        "timestamp": datetime.now().isoformat(),
        "niche": niche,
        "platform": platform,
        "topic": topic,
        "script_snippet": script[:100] + "..." if len(script) > 100 else script,
        "hashtags": hashtags
    }
    
    if topic not in memory.get("past_topics", []):
        memory.setdefault("past_topics", []).append(topic)
        
    memory.setdefault("content_history", []).append(entry)
    save_memory(memory)

def get_past_topics_for_niche(niche):
    """Retrieves a list of past topics generated for a specific niche to avoid duplicates."""
    memory = load_memory()
    return [
        entry["topic"] for entry in memory.get("content_history", []) 
        if entry.get("niche", "").lower() == niche.lower()
    ]
