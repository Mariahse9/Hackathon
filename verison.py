import re
from pathlib import Path

import nltk
from nltk.stem.snowball import SnowballStemmer
from razdel import tokenize

stemmer = SnowballStemmer("russian")


class EmailReceiver:
    def __init__(self, filepath):
        self.filepath = filepath
        self.is_good = True
        self.content = self.filereader()

    def filereader(self):
        if self.filepath.suffix.lower() in [
            ".bin",
            ".jpeg",
            ".jpg",
            ".png",
            ".exe",
            ".zip",
        ]:
            self.is_good = False
            return ""
        try:
            with open(self.filepath, encoding="utf-8", errors="ignore") as f:
                return f.read().lower()
        except Exception:
            return ""

    def textpreprocessing(self):
        if not self.content:
            return []

        tokens = tokenize(self.content)
        words = []

        punctuations = r'!"#$%&\'()*+,-./:;<=>?@[\]^_`{|}~'

        for word in tokens:
            if word.text not in punctuations:
                words.append(stemmer.stem(word.text))

        return words


class Rules:
    def __init__(self):
        self.rules = {
            "incidents": {
                "упал",
                "ошибк",
                "сбо",
                "срочн",
                "слома",
                "зависа",
                "проблем",
                "отвеча",
                "неисправн",
                "ремонт",
                "работа",
                "открыва",
            },
            "access_and_hr": {
                "доступ",
                "парол",
                "учетн",
                "vpn",
                "прав",
                "войт",
                "сотрудник",
                "заявк",
                "отпуск",
                "больничн",
            },
            "finance_and_docs": {
                "акт",
                "оплат",
                "счет",
                "договор",
                "согласован",
                "подпис",
                "закрыва",
                "реквизит",
                "приложен",
            },
            "meetings": {"созвон", "встрет", "встреч", "демо"},
            "info_and_requests": {
                "дайджест",
                "планов",
                "инструкц",
                "инструкци",
                "запрос",
            },
            "security_alerts": {"заблокирова", "аккаунт", "взлом", "мошенник"},
            "spam": {
                "скидк",
                "выигра",
                "реклам",
                "казин",
                "распродаж",
                "розыгрыш",
                "приз",
                "банк",
                "карт",
            },
        }

    def classify(self, email):
        if not email.is_good or not email.content:
            return "unclassified"

        errors_re = re.compile(r"(код ошибки|код):?\s*(err_\d+|[45]0\d)")
        if errors_re.search(email.content):
            return "errors"

        monitor_re = re.compile(r"alert|healthcheck|error_log\.txt")
        stems = email.textpreprocessing()

        if monitor_re.search(email.content):
            return "alerts"

        url_re = re.compile(r"http[s]?://\S+")

        if url_re.search(email.content) or self.rules["spam"].intersection(stems):
            return "spam"

        if self.rules["security_alerts"].intersection(stems):
            return "security_alerts"

        scores = {}

        for category, keywords in self.rules.items():
            score = sum(1 for stem in stems if stem in keywords)
            scores[category] = score
        category_current = max(scores, key=scores.get)
        if scores[category_current] > 0:
            return category_current

        return "unsorted"


class FileCEO:
    def __init__(self, out_dir):
        self.out_dir = out_dir

    def move_file(self, filepath, category):
        cat_dir = self.out_dir / category
        cat_dir.mkdir(parents=True, exist_ok=True)

        dir = cat_dir / filepath.name
        try:
            filepath.replace(dir)
            print(f"[{category.upper():<20}] {filepath.name}")
        except Exception as e:
            print(f"Ошибка перемещения: {e}")


def main():
    base_dir = Path(__file__).parent.parent
    inbox = base_dir / "data" / "inbox"
    outbox = base_dir / "data" / "outbox"

    if not inbox.exists():
        print("Папка inbox отсутствует")
        return

    classifier = Rules()
    filemanager = FileCEO(outbox)

    print("Начало сортировки писем")
    for item in inbox.iterdir():
        if item.is_file() and not item.name.startswith("."):
            email = EmailReceiver(item)
            category = classifier.classify(email)
            filemanager.move_file(item, category)


if __name__ == "__main__":
    main()
