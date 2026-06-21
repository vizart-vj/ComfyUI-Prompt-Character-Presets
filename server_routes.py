import os
import json
from server import PromptServer
from aiohttp import web

DEFAULT_DATA = {
    "prompts": {
        "Cinematic Movie": "cinematic shot, 8k resolution, highly detailed, dramatic lighting",
        "Anime Style": "anime aesthetic, vibrant colors, studio ghibli style, detailed background"
    },
    "characters": {
        "Character 1 (Hero)": "a brave warrior, silver armor, blue eyes",
        "Character 2 (Mage)": "a wise sorcerer, hooded purple robe"
    }
}

def load_presets_from_path(file_path):
    if not file_path:
        return DEFAULT_DATA
    file_path = file_path.strip().strip('"').strip("'")
    if not os.path.exists(file_path):
        try:
            dir_name = os.path.dirname(file_path)
            if dir_name and not os.path.exists(dir_name):
                os.makedirs(dir_name, exist_ok=True)
            with open(file_path, "w", encoding="utf-8") as f:
                json.dump(DEFAULT_DATA, f, indent=4, ensure_ascii=False)
            return DEFAULT_DATA
        except Exception:
            return DEFAULT_DATA
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return DEFAULT_DATA

def save_presets_to_path(file_path, data):
    file_path = file_path.strip().strip('"').strip("'")
    try:
        with open(file_path, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=4, ensure_ascii=False)
        return True
    except Exception as e:
        print(f"[PromptPresets] Save error: {e}")
        return False

@PromptServer.instance.routes.post("/prompt_presets/manage")
async def manage_presets_api(request):
    try:
        json_data = await request.json()
        action = json_data.get("action")
        config_path = json_data.get("config_path")
        preset_type = json_data.get("type")
        name = json_data.get("name")
        value = json_data.get("value")

        presets = load_presets_from_path(config_path)

        if action == "add" and name:
            if preset_type not in presets:
                presets[preset_type] = {}
            presets[preset_type][name] = value
            save_presets_to_path(config_path, presets)
            return web.json_response({"status": "success", "keys": list(presets[preset_type].keys())})

        elif action == "delete" and name:
            if preset_type in presets and name in presets[preset_type]:
                del presets[preset_type][name]
                save_presets_to_path(config_path, presets)
            return web.json_response({"status": "success", "keys": list(presets.get(preset_type, {}).keys())})

    except Exception as e:
        print(f"[PromptPresets] API error: {e}")
        
    return web.json_response({"status": "error"})

def setup_routes():
    pass
