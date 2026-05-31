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
        if self.filepath.suffix.lower() in ['.bin', '.jpeg', '.jpg', '.png', '.exe', '.zip']:
            self.is_good = False
            return ''
        try:
            with open(self.filepath, encoding='utf-8', errors='ignore') as f:
                return f.read()
        except Exception:
            return ""

    def textpreprocessing(self):
        if not self.content:
            return []
            
        tokens = tokenize(self.content.lower())
        words = []
        
        punctuations = r'!"#$%&\'()*+,-./:;<=>?@[\]^_`{|}~'
        
        for word in tokens:
            if word.text not in punctuations:
                words.append(stemmer.stem(word.text))
                
        return words