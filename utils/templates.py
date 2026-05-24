import json
import os

TEMPLATES_FILE = 'templates.json'

DEFAULT_TEMPLATES = [
    {
        "name": "NAND",
        "inputs": ["A", "B"],
        "outputs": ["Out"]
    },
    {
        "name": "Display",
        "inputs": ["Value"],
        "outputs": []
    }
]

def load_templates():
    if not os.path.exists(TEMPLATES_FILE):
        return DEFAULT_TEMPLATES.copy()
    
    try:
        with open(TEMPLATES_FILE, 'r') as f:
            return json.load(f)
    except Exception:
        return DEFAULT_TEMPLATES.copy()

def save_templates(templates):
    with open(TEMPLATES_FILE, 'w') as f:
        json.dump(templates, f, indent=4)
