
import tkinter as tk
from tkinter import ttk, scrolledtext
from query import query_type

BG          = "#0d1117"   
PANEL       = "#161b22"   
BORDER      = "#30363d"   
ACCENT      = "#f78166"  
ACCENT2     = "#58a6ff"   
TEXT_MAIN   = "#e6edf3"  
TEXT_DIM    = "#8b949e"   
SUCCESS     = "#3fb950"   
TAG_BG      = "#1f2937"   
FONT_MONO   = ("Courier New", 11)
FONT_BODY   = ("Georgia", 11)
FONT_TITLE  = ("Georgia", 20, "bold")
FONT_LABEL  = ("Georgia", 10)
FONT_SMALL  = ("Courier New", 9)


EXAMPLE_QUERIES = [
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


def launch_gui(inverted_index, positional_index, doc_map, all_doc_ids):
    """Build and run the Tkinter GUI window."""

    root = tk.Tk()
    root.title("CS4051 — Boolean IR System")
    root.configure(bg=BG)
    root.geometry("980x720")
    root.minsize(800, 580)

    # ── Title bar ─────────────────────────────────────────────────────
    header = tk.Frame(root, bg=BG, pady=14)
    header.pack(fill="x", padx=24)

    tk.Label(
        header, text="🔍  Boolean IR System",
        font=FONT_TITLE, bg=BG, fg=TEXT_MAIN
    ).pack(side="left")

    tk.Label(
        header,
        text=f"{len(all_doc_ids)} docs  •  {len(inverted_index)} terms",
        font=FONT_LABEL, bg=BG, fg=TEXT_DIM
    ).pack(side="right", pady=8)

    sep = tk.Frame(root, bg=BORDER, height=1)
    sep.pack(fill="x", padx=0)

    
    body = tk.Frame(root, bg=BG)
    body.pack(fill="both", expand=True, padx=0, pady=0)

   
    sidebar = tk.Frame(body, bg=PANEL, width=230)
    sidebar.pack(side="left", fill="y")
    sidebar.pack_propagate(False)

    tk.Label(
        sidebar, text="Example Queries",
        font=("Georgia", 11, "bold"), bg=PANEL, fg=TEXT_DIM,
        anchor="w", padx=14, pady=10
    ).pack(fill="x")

    tk.Frame(sidebar, bg=BORDER, height=1).pack(fill="x", padx=10)

    
    eg_canvas = tk.Canvas(sidebar, bg=PANEL, highlightthickness=0)
    eg_scroll = tk.Scrollbar(sidebar, orient="vertical", command=eg_canvas.yview)
    eg_frame  = tk.Frame(eg_canvas, bg=PANEL)

    eg_frame.bind("<Configure>", lambda e: eg_canvas.configure(
        scrollregion=eg_canvas.bbox("all")
    ))
    eg_canvas.create_window((0, 0), window=eg_frame, anchor="nw")
    eg_canvas.configure(yscrollcommand=eg_scroll.set)

    eg_canvas.pack(side="left", fill="both", expand=True)
    eg_scroll.pack(side="right", fill="y")

    def load_example(q):
        query_var.set(q)
        run_query()

    for q in EXAMPLE_QUERIES:
        btn = tk.Button(
            eg_frame, text=q,
            font=FONT_SMALL, bg=PANEL, fg=ACCENT2,
            activebackground=TAG_BG, activeforeground=ACCENT2,
            relief="flat", anchor="w", padx=12, pady=4,
            cursor="hand2", wraplength=200, justify="left",
            command=lambda qq=q: load_example(qq)
        )
        btn.pack(fill="x", pady=1)
        btn.bind("<Enter>", lambda e, b=btn: b.configure(bg=TAG_BG))
        btn.bind("<Leave>", lambda e, b=btn: b.configure(bg=PANEL))

    
    right = tk.Frame(body, bg=BG)
    right.pack(side="left", fill="both", expand=True)

    
    input_frame = tk.Frame(right, bg=BG, pady=12)
    input_frame.pack(fill="x", padx=20)

    tk.Label(
        input_frame, text="Enter Query",
        font=("Georgia", 10, "bold"), bg=BG, fg=TEXT_DIM
    ).pack(anchor="w")

    query_row = tk.Frame(input_frame, bg=BG)
    query_row.pack(fill="x", pady=(4, 0))

    query_var = tk.StringVar()

    entry_bg = tk.Frame(query_row, bg=ACCENT, padx=1, pady=1)
    entry_bg.pack(side="left", fill="x", expand=True)

    entry = tk.Entry(
        entry_bg, textvariable=query_var,
        font=FONT_MONO, bg=PANEL, fg=TEXT_MAIN,
        insertbackground=ACCENT, relief="flat",
        bd=8
    )
    entry.pack(fill="x")
    entry.focus()

    def run_query(event=None):
        q = query_var.get().strip()
        if not q:
            return
        results_box.configure(state="normal")
        results_box.delete("1.0", "end")

        try:
            result_ids = query_type(
                q, inverted_index, positional_index, all_doc_ids
            )
            sorted_ids = sorted(result_ids)
            count = len(sorted_ids)

            # Header
            results_box.insert("end", f"Query:  ", "label")
            results_box.insert("end", f"{q}\n", "query")
            results_box.insert("end", f"Matched: ", "label")
            results_box.insert("end", f"{count} document(s)\n\n", "count")

            if count == 0:
                results_box.insert("end", "  No documents matched this query.\n", "dim")
            else:
                # Doc IDs line
                results_box.insert("end", "Document IDs:\n", "label")
                results_box.insert("end", f"  {sorted_ids}\n\n", "ids")

                # Per-doc details
                results_box.insert("end", "Documents:\n", "label")
                for doc_id in sorted_ids:
                    fname = doc_map.get(doc_id, "unknown")
                    results_box.insert("end", f"  [{doc_id:>3}]  ", "docid")
                    results_box.insert("end", f"{fname}\n", "fname")

        except Exception as e:
            results_box.insert("end", f"Error: {e}\n", "error")

        results_box.configure(state="disabled")

    entry.bind("<Return>", run_query)

    run_btn = tk.Button(
        query_row, text="Search",
        font=("Georgia", 11, "bold"),
        bg=ACCENT, fg="#0d1117",
        activebackground="#e05a45", activeforeground="#0d1117",
        relief="flat", padx=18, pady=4,
        cursor="hand2", command=run_query
    )
    run_btn.pack(side="left", padx=(8, 0))

    clear_btn = tk.Button(
        query_row, text="Clear",
        font=("Georgia", 10),
        bg=PANEL, fg=TEXT_DIM,
        activebackground=TAG_BG,
        relief="flat", padx=10, pady=4,
        cursor="hand2",
        command=lambda: [query_var.set(""), results_box.configure(state="normal"),
                         results_box.delete("1.0", "end"),
                         results_box.configure(state="disabled")]
    )
    clear_btn.pack(side="left", padx=(4, 0))

    
    hint = tk.Label(
        input_frame,
        text="Syntax:  term  |  t1 AND t2  |  t1 OR t2  |  NOT t1  |  t1 AND (t2 OR t3)  |  t1 t2 /k",
        font=("Courier New", 9), bg=BG, fg=TEXT_DIM, anchor="w"
    )
    hint.pack(anchor="w", pady=(6, 0))

    
    tk.Frame(right, bg=BORDER, height=1).pack(fill="x", padx=20, pady=(4, 0))

    res_label = tk.Frame(right, bg=BG, pady=6)
    res_label.pack(fill="x", padx=20)
    tk.Label(res_label, text="Results", font=("Georgia", 10, "bold"),
             bg=BG, fg=TEXT_DIM).pack(anchor="w")

    results_box = scrolledtext.ScrolledText(
        right, font=FONT_MONO,
        bg=PANEL, fg=TEXT_MAIN,
        insertbackground=ACCENT,
        relief="flat", bd=0,
        padx=16, pady=12,
        state="disabled",
        wrap="word"
    )
    results_box.pack(fill="both", expand=True, padx=20, pady=(0, 16))

    
    results_box.tag_configure("label",  foreground=TEXT_DIM,  font=("Georgia", 10, "bold"))
    results_box.tag_configure("query",  foreground=ACCENT2,   font=FONT_MONO)
    results_box.tag_configure("count",  foreground=SUCCESS,   font=("Courier New", 11, "bold"))
    results_box.tag_configure("ids",    foreground=ACCENT,    font=FONT_MONO)
    results_box.tag_configure("docid",  foreground=ACCENT,    font=FONT_MONO)
    results_box.tag_configure("fname",  foreground=TEXT_MAIN, font=FONT_MONO)
    results_box.tag_configure("dim",    foreground=TEXT_DIM,  font=FONT_BODY)
    results_box.tag_configure("error",  foreground="#ff6b6b", font=FONT_MONO)

    
    status = tk.Frame(root, bg=PANEL, pady=4)
    status.pack(fill="x", side="bottom")
    tk.Label(
        status,
        text="CS4051 — Information Retrieval  •  Boolean IR Model  •  Spring 2026",
        font=("Georgia", 9), bg=PANEL, fg=TEXT_DIM
    ).pack()

    root.mainloop()
