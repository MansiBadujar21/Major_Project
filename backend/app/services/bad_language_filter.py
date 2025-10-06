import json
from pathlib import Path


class BadLanguageFilter:
    def __init__(self) -> None:
        data_path = Path(__file__).resolve().parent.parent / "data" / "bad_words.json"
        if data_path.exists():
            with open(data_path, "r", encoding="utf-8") as f:
                self.bad_words: set[str] = set(json.load(f))
        else:
            self.bad_words = set()

    def contains_bad_language(self, text: str) -> bool:
        lower = text.lower()
        return any(bad in lower for bad in self.bad_words)


