import re
import os

#stored stopwrods for 0(1) retrival if file fails
Array_STOPWORDS = {
    "a", "is", "the", "of", "all", "and", "to", "can", "be", "as",
    "once", "for", "at", "am", "are", "has", "have", "had", "up",
    "his", "her", "in", "on", "no", "we", "do"
}

#load stopwords from file line by line
def load_stopwords(filepath="stopwords.txt"):
    
    if os.path.exists(filepath):
        with open(filepath, "r", encoding="utf-8") as f:
            words = set(line.strip().lower() for line in f if line.strip())
        print(f"[Preprocessing] Loaded {len(words)} stopwords from '{filepath}'")
        return words
    else:
        print(f"[Preprocessing] '{filepath}' not found !!ERROR!!")
        return Array_STOPWORDS


def stemming(word):
    #removing suffixes
    suffixes = ["tion", "ness", "ment", "ing", "ed", "er", "es", "ly", "s"]
    for suffix in suffixes:
        #min stemmin length =3 so over stripping is avoided
        if word.endswith(suffix) and len(word) - len(suffix) >= 3:
            return word[: -len(suffix)]
    return word


def preprocess(text, stopwords):

    #lowercase
    text = text.lower()

    #create token withon numbers or any charachters use of regular expression done here
    tokens = re.findall(r"[a-zA-Z]+", text)

    #remove stopwords and then apply stemming
    processed_tokens = []
    for pos, token in enumerate(tokens):
        if token not in stopwords:
            stemmed = stemming(token)
            processed_tokens.append((stemmed, pos))

    return processed_tokens
