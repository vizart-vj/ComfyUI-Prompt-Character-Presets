# ComfyUI Prompt Presets Node

A ComfyUI custom node for managing prompt and character presets with a convenient UI interface.

## Features

- **Prompt Presets** - Save and load frequently used prompt texts
- **Character Presets** - Store character descriptions for consistent generation
- **Quick Add/Delete** - Add or remove presets directly from the node UI
- **JSON Storage** - All presets stored in a portable JSON file
- **Dynamic Dropdowns** - Preset lists update automatically after changes

## Installation

1. Navigate to your ComfyUI `custom_nodes` folder
2. Clone this repository:
```bash
git clone https://github.com/vizart-vj/ComfyUI-Prompt-Character-Presets.git
```
3. Restart ComfyUI

## Usage

1. Add the **Prompt & Character Presets** node from the `PromptUtils` category
2. The node creates a default presets file at `~/comfyui_presets.json` on first run
3. Use the UI buttons to manage your presets:
   - **Add Char** / **Del Char** - Manage character presets
   - **Add Prompt** / **Del Prompt** - Manage prompt presets

### Node Outputs

| Output | Description |
|--------|-------------|
| `character_text` | The selected character description |
| `prompt_text` | The selected prompt text |

## Configuration

The presets file path can be changed via the `config_path` input. Default location:
- Windows: `%USERPROFILE%\comfyui_presets.json`
- Linux/Mac: `~/comfyui_presets.json`

### JSON Format

```json
{
    "prompts": {
        "Cinematic Movie": "cinematic shot, 8k resolution, highly detailed, dramatic lighting",
        "Anime Style": "anime aesthetic, vibrant colors, studio ghibli style, detailed background"
    },
    "characters": {
        "Character 1 (Hero)": "a brave warrior, silver armor, blue eyes",
        "Character 2 (Mage)": "a wise sorcerer, hooded purple robe"
    }
}
```

## Example Workflow

```
[Prompt Presets] --> character_text --> [Positive Prompt]
                     prompt_text  ---->
```

## Requirements

- ComfyUI (latest version recommended)
- No additional Python packages required

## License

MIT License
