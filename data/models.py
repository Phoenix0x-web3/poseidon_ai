import json
from pathlib import Path

from data.config import DATA_DIR
from libs.eth_async.classes import Singleton
from libs.eth_async.data.models import RawContract, DefaultABIs


class Contracts(Singleton):

    ETH = RawContract(
        title='ETH',
        address='0x0000000000000000000000000000000000000000',
        abi=DefaultABIs.Token
    )

LANG_MAP = {
    "en": "English",
    "mr": "Marathi",
    "ur": "Urdu",
    "ar": "Arabic",
    "zh": "Mandarin",
    "id": "Indonesian",
    "vi": "Vietnamese",
    "tr": "Turkish",
    "ru": "Russian",
    "pt": "Portuguese",
    "de": "German",
    "fr": "French",
    "es": "Spanish",
    "ko": "Korean",
    "ja": "Japanese",
    "hi": "Hindi",
}

def ai_models():
    path = Path(DATA_DIR) / "lang_map.json"
    voices = json.loads(path.read_text(encoding="utf-8"))

    for voice in voices:
        languages = voice.get("languages") or {}
        lang_map = {}

        for code, model_id in languages.items():
            if code in LANG_MAP:
                human = LANG_MAP[code]
                lang_map[human] = {
                    "code": code,
                    "model_id": model_id
                }

        voice["lang_map"] = lang_map
        voice.pop('lang')
        voice.pop('languages')
        voice.pop('models')

    return [voice for voice in voices if 'English' in list(voice['lang_map'].keys())]