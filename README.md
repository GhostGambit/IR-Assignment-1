# CS4051 — Boolean Information Retrieval System
### Information Retrieval · Spring 2026 · Programming Assignment 1

---

## Description

A Boolean Information Retrieval system built in Python that indexes 56 Trump speeches (June 2015 – November 2016) and retrieves documents using Boolean and proximity queries. The system builds an **Inverted Index** and a **Positional Index** from a preprocessing pipeline (tokenization, stopword removal, stemming). It supports `AND`, `OR`, `NOT`, nested expressions, and proximity queries (`word1 word2 /k`). Comes with both a terminal CLI and a dark-themed Tkinter GUI.

---

## Project Structure

```
├── main.py            # Entry point — run this
├── preprocessing.py   # Tokenization, stopword removal, stemming
├── indexer.py         # Builds, saves, and loads both indexes
├── query.py           # Boolean and proximity query engine
├── gui.py             # Tkinter GUI (launches automatically)
├── Trump_Speechs/     # Place your 56 .txt speech files here
├── stopwords.txt      # One stopword per line
└── README.md
```

---

## Requirements

- Python 3.7+
- No external libraries — uses only Python standard library (`re`, `os`, `json`, `tkinter`)

---

## Setup

**1. Clone the repository**
```bash
git https://github.com/GhostGambit/IR-Assignment-1
cd IR-Assignment-1
```

**2. Add the speech files**

Place all 56 `.txt` speech files inside a folder named exactly:
```
Trump_Speechs/
```

**3. Add stopwords (optional)**

Place a `stopwords.txt` file in the root directory with one stopword per line. If missing, a built-in fallback list is used automatically.

---

## How to Run

```bash
python main.py --gui        # Opens GUI 
python main.py     # Terminal-only mode
```

On the **first run**, the system reads all 56 documents, builds both indexes, and saves them to disk as JSON. Every run after that loads instantly from the saved files.

---

## Features

| Feature | Details |
|---|---|
| Preprocessing | Case folding, regex tokenization, stopword removal, suffix stemming |
| Inverted Index | `{ term → set of doc IDs }` saved and loaded from JSON |
| Positional Index | `{ term → { doc_id → [positions] } }` for proximity queries |
| Boolean Queries | `AND`, `OR`, `NOT`, nested parentheses, unlimited terms |
| Proximity Queries | `word1 word2 /k` — matches docs where terms are within k words |
| GUI | Dark-themed Tkinter window with sidebar, search box, colour-coded results |
| CLI | Terminal mode with all 13 gold-standard queries printed on startup |

---

## Query Syntax

| Query | Meaning |
|---|---|
| `trump` | Documents containing "trump" |
| `NOT hammer` | Documents that do NOT contain "hammer" |
| `actions AND wanted` | Documents containing both terms |
| `united OR plane` | Documents containing either term |
| `pakistan OR afganistan OR aid` | Any of the three terms |
| `biggest AND ( near OR box )` | "biggest" AND either "near" or "box" |
| `NOT ( united AND plane )` | Exclude docs containing both "united" and "plane" |
| `after years /1` | "after" and "years" within 1 word of each other |
| `keep out /2` | "keep" and "out" within 2 words of each other |

---

## How It Works

### 1. Preprocessing Pipeline
Every document is cleaned before indexing:
```
Raw text  →  lowercase  →  tokenize (regex)  →  remove stopwords  →  stem
```
Stemming strips common suffixes (`-ing`, `-ed`, `-tion`, `-ness` etc.) so "running" and "run" map to the same index term.

### 2. Inverted Index
Maps every stemmed term to the set of documents it appears in:
```python
{ "trump": {0, 3, 7},  "america": {0, 1, 2, 5} }
```
Boolean queries use Python set operations — `AND` = intersection (`&`), `OR` = union (`|`), `NOT` = complement (`all_docs - set`).

### 3. Positional Index
Extends the inverted index with exact token positions:
```python
{ "trump": { 0: [5, 22, 88],  3: [12, 45] } }
```
Used for proximity queries — checks if `|position1 - position2| <= k`.

### 4. Query Parsing
Operator precedence (highest to lowest):
1. Parentheses `( )` — resolved recursively
2. `NOT` — complement
3. `AND` — intersection
4. `OR` — union (lowest precedence)

---

## Gold Standard Queries

| # | Query | Docs matched |
|---|---|---|
| 1 | `running` | 44 |
| 2 | `NOT hammer` | 32 |
| 3 | `actions AND wanted` | 25 |
| 4 | `united OR plane` | 53 |
| 5 | `pakistan OR afganistan OR aid` | 13 |
| 6 | `biggest AND ( near OR box )` | 12 |
| 7 | `box AND ( united OR year )` | 11 |
| 8 | `biggest AND ( plane OR wanted OR hour )` | 31 |
| 9 | `NOT ( united AND plane )` | 39 |
| 10 | `Hillary AND Clinton` | 50 |
| 11 | `after years /1` | 3 |
| 12 | `develop solutions /1` | 2 |
| 13 | `keep out /2` | 5 |

---


---

## Author
Muhammad Umer Siddiqui
Roll No 23K-0644
BCS 6A
CS4051 — Information Retrieval
Spring 2026
