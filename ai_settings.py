import json
import os

SETTINGS_FILE = "ai_settings.json"
DEFAULT_SETTINGS = {
    "auto_reprice": False,
    "auto_list": False,
    "auto_source": False,
    "auto_order": False,
    "auto_inventory_sync": False,
    "auto_fulfill": False,
    "auto_message": False,
    "auto_predict": False,
    "auto_refund": False,
    "live_mode": False   # ⭐ NEW
}

}

def load_settings():
    if not os.path.exists(SETTINGS_FILE):
        save_settings(DEFAULT_SETTINGS)
        return DEFAULT_SETTINGS
    with open(SETTINGS_FILE, "r") as f:
        return json.load(f)

def save_settings(settings):
    with open(SETTINGS_FILE, "w") as f:
        json.dump(settings, f, indent=4)

def update_setting(key, value):
    settings = load_settings()
    settings[key] = value
    save_settings(settings)
    return settings
