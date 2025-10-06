import yake


class KeywordExtractor:
    def __init__(self) -> None:
        self.kw = yake.KeywordExtractor(lan="en", n=1, top=20)

    def extract(self, text: str) -> list[str]:
        keywords = self.kw.extract_keywords(text)
        # returns list of (keyword, score); lower score is better
        return [k for k, _ in sorted(keywords, key=lambda x: x[1])[:10]]


