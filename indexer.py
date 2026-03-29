import os
import json
from collections import defaultdict
from preprocessing import preprocess


def build_inverted_index(docs_folder, stopwords):
    
    #creating inverted index using the previously proccessed data to tokens
    inverted_index = defaultdict(set)
    doc_map = {}

    #files sorted in order for easier retrival
    files = sorted(
        [f for f in os.listdir(docs_folder) if f.endswith(".txt")],
        key=lambda x: int(x.replace(".txt", "")) if x.replace(".txt", "").isdigit() else x
    )

    print(f" Found {len(files)} documents in '{docs_folder}'")

    for doc_id, filename in enumerate(files):
        doc_map[doc_id] = filename
        filepath = os.path.join(docs_folder, filename)

        #open sheech and store to preprocces and convert to inverted index
        with open(filepath, "r", encoding="utf-8", errors="ignore") as f:
            speech = f.read()

        tokens = preprocess(speech, stopwords)

        for term, _ in tokens:
            inverted_index[term].add(doc_id)

    print(f" Inverted index created !. Vocabulary size: {len(inverted_index)}")
    return inverted_index, doc_map


def build_positional_index(docs_folder, stopwords):
    #creating positional index using the previously proccessed data to tokens
    positional_index = defaultdict(lambda: defaultdict(list))
    doc_map = {}

    files = sorted(
        [f for f in os.listdir(docs_folder) if f.endswith(".txt")],
        key=lambda x: int(x.replace(".txt", "")) if x.replace(".txt", "").isdigit() else x
    )

    for doc_id, filename in enumerate(files):
        doc_map[doc_id] = filename
        filepath = os.path.join(docs_folder, filename)

        #open sheech and store to preprocces and convert to positional index
        with open(filepath, "r", encoding="utf-8", errors="ignore") as f:
            speech = f.read()

        tokens = preprocess(speech, stopwords)

        for term, pos in tokens:
            positional_index[term][doc_id].append(pos)

    print(f"Positional index built !.")
    return positional_index, doc_map


def save_index(inverted_index, positional_index, doc_map):
    # sets → lists for JSON
    inv = {k: list(v) for k, v in inverted_index.items()}
    pos = {
        k: {str(doc_id): positions for doc_id, positions in v.items()}
        for k, v in positional_index.items()
    }

    #create/open josn files to store both positional and inverted indexso they dont have 
    # to looked again and again hence reducing overhead
    # if File error it shows File Error
    with open("inverted_index.json", "w") as f:
        json.dump(inv, f, indent=2)
    with open("positional_index.json", "w") as f:
        json.dump(pos, f, indent=2)
    with open("doc_map.json", "w") as f:
        json.dump({str(k): v for k, v in doc_map.items()}, f, indent=2)

    print("Indexes saved to disk (inverted_index.json, positional_index.json, doc_map.json)")


def load_index():
    
    #load index previously saved and if error opening  it shows File Error else index loaded
    with open("inverted_index.json") as f:
        inv = json.load(f)
    with open("positional_index.json") as f:
        pos = json.load(f)
    with open("doc_map.json") as f:
        doc_map_raw = json.load(f)

    inverted_index = {k: set(v) for k, v in inv.items()}
    positional_index = {
        k: {int(doc_id): positions for doc_id, positions in v.items()}
        for k, v in pos.items()
    }
    doc_map = {int(k): v for k, v in doc_map_raw.items()}

    print(f" Indexes loaded. {len(doc_map)} docs, {len(inverted_index)} terms.")
    return inverted_index, positional_index, doc_map


def index_exist():
    #return true if all these file exsists if not main will promt to make these files
    return all(os.path.exists(f) for f in
               ("inverted_index.json", "positional_index.json", "doc_map.json"))
