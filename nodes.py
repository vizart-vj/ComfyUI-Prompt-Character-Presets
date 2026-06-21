import os
import json

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

class PromptPresetsNode:
    def __init__(self):
        pass

    @classmethod
    def INPUT_TYPES(cls):
        default_path = os.path.join(os.path.expanduser("~"), "comfyui_presets.json").replace("\\", "/")
        presets = load_presets_from_path(default_path)
        
        prompt_list = list(presets.get("prompts", {}).keys())
        character_list = list(presets.get("characters", {}).keys())
        
        if not prompt_list:
            prompt_list = ["None"]
        else:
            prompt_list.insert(0, "None")
            
        if not character_list:
            character_list = ["None"]
        else:
            character_list.insert(0, "None")

        return {
            "required": {
                "config_path": ("STRING", {"default": default_path, "multiline": False}),
                "character_preset": (character_list, {}),
                "prompt_preset": (prompt_list, {}),
                "new_preset_name": ("STRING", {"default": "", "placeholder": "Имя нового пресета/персонажа"}),
                "new_preset_value": ("STRING", {"multiline": True, "default": "", "placeholder": "Описание или текст промпта"}),
            }
        }

    RETURN_TYPES = ("STRING", "STRING")
    RETURN_NAMES = ("character_text", "prompt_text")
    FUNCTION = "get_presets"
    CATEGORY = "PromptUtils"

    @classmethod
    def VALIDATE_INPUTS(cls, **kwargs):
        return True

    def get_presets(self, config_path, character_preset, prompt_preset, new_preset_name, new_preset_value):
        presets = load_presets_from_path(config_path)
        
        char_out = ""
        if character_preset and character_preset != "None":
            char_out = presets.get("characters", {}).get(character_preset, "")
            if not char_out:
                print(f"[PromptPresets] Warning: Character '{character_preset}' not found in JSON.")

        prompt_out = ""
        if prompt_preset and prompt_preset != "None":
            prompt_out = presets.get("prompts", {}).get(prompt_preset, "")
            if not prompt_out:
                print(f"[PromptPresets] Warning: Prompt '{prompt_preset}' not found in JSON.")

        return (char_out, prompt_out)

NODE_CLASS_MAPPINGS = {
    "PromptPresetsNode": PromptPresetsNode
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "PromptPresetsNode": "Prompt & Character Presets"
}
