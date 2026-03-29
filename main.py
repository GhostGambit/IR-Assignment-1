import sys
import os
from preprocessing import load_stopwords
from indexer import (
    build_inverted_index,
    build_positional_index,
    save_index,
    load_index,
    index_exist,
)
from query import query_type


DOCS_FOLDER    = "Trump_Speechs"   # folder containing the 56 .txt speech files
STOPWORDS_FILE = "stopwords.txt"   
GOLD_QUERIES = [
    "running",
    "NOT hammer",
    "actions AND wanted",
    "united OR plane",
    "pakistan OR afganistan OR aid",
    "biggest AND ( near OR box )",
    "box AND ( united OR year )",
    "biggest AND ( plane OR wanted OR hour )",
    "NOT ( united AND plane )",
    "Hillary AND Clinton",
    "after years /1",
    "develop solutions /1",
    "keep out /2",
]


def print_results(result_ids, doc_map):
    if not result_ids:
        print(" -> No matching documents.")
        return

    sorted_ids = sorted(result_ids)
    print(f" -> {len(sorted_ids)} doc(s) matched: {sorted_ids}")
    for doc_id in sorted_ids[:5]:
        print(f"     [{doc_id}] {doc_map.get(doc_id, '?')}")
    if len(sorted_ids) > 5:
        print(f"     ... and {len(sorted_ids) - 5} more.")


def setup(stopwords):
    #load indexs from the disk saved in json fil if dont exsist then create them.
    if index_exist():
        print(" Saved indexes found — loading from disk...")
        inverted_index, positional_index, doc_map = load_index()
    else:
        print(" No saved indexes — building from documents...")
        if not os.path.exists(DOCS_FOLDER):
            #if trump speech folder non exsistent then error and exit
            print(f"ERROR!!! Folder '{DOCS_FOLDER}' not found.")
            sys.exit(1)
        inverted_index, doc_map = build_inverted_index(DOCS_FOLDER, stopwords)
        positional_index, _    = build_positional_index(DOCS_FOLDER, stopwords)
        save_index(inverted_index, positional_index, doc_map)

    all_doc_ids = set(doc_map.keys())
    print(f" Ready. {len(all_doc_ids)} documents, {len(inverted_index)} unique terms.\n")
    return inverted_index, positional_index, doc_map, all_doc_ids




def run_cli(inverted_index, positional_index, doc_map, all_doc_ids):
    
    #run gold standar queries and get to know qurey type then complete accordingy
    print("=" * 62)
    print("  GOLD STANDARD QUERIES")
    print("=" * 62)
    for i, q in enumerate(GOLD_QUERIES, 1):
        print(f"\nQ{i:02d}: {q}")
        result = query_type(q, inverted_index, positional_index, all_doc_ids)
        print_results(result, doc_map)

    print("\n" + "=" * 62)
    print("  INTERACTIVE MODE  (type 'exit' to quit)")
    print("  Syntax examples:")
    print("    trump AND america")
    print("    NOT hillary")
    print("    jobs OR economy OR trade")
    print("    biggest AND ( plane OR box )")
    print("    make great /2")
    print("=" * 62 + "\n")

    while True:
        try:
            raw = input("Query> ").strip()
        except (EOFError, KeyboardInterrupt):
            print("\nGoodbye!")
            break

        if raw.lower() in ("exit", "quit", "q", ""):
            print("Goodbye!")
            break
        
        #store and print query type
        result = query_type(raw, inverted_index, positional_index, all_doc_ids)
        print_results(result, doc_map)
        print()



def main():
    stopwords = load_stopwords(STOPWORDS_FILE)
    inverted_index, positional_index, doc_map, all_doc_ids = setup(stopwords)

    if "--gui" in sys.argv:
        # Launch GUI
        try:
            from gui import launch_gui
            launch_gui(inverted_index, positional_index, doc_map, all_doc_ids)
        except ImportError as e:
            #Run gui using tkinter if fails then resort to the cli mode
            print(f"ERROR!!! Could not launch GUI: {e}")
            run_cli(inverted_index, positional_index, doc_map, all_doc_ids)
    else:
        run_cli(inverted_index, positional_index, doc_map, all_doc_ids)


if __name__ == "__main__":
    main()
