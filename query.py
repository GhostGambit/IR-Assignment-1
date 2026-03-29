import re
from preprocessing import stemming



def get_postings(term, inverted_index):
    #get tokens from query and convert it to the stemmed woriding according to the indexed
    stemmed_word = stemming(term.lower().strip())
    return inverted_index.get(stemmed_word, set()).copy()


def boolean_query(query, inverted_index, all_doc_ids):
  
    query = query.strip()

    #each of the quesry gets a uniqe counter
    _placeholder_counter = [0] 

    while "(" in query:
        close = query.index(")")
        open_ = query.rindex("(", 0, close)
        inner = query[open_ + 1: close].strip()

        inner_result = boolean_query(inner, inverted_index, all_doc_ids)

        #avoid collisions in nested queries
        _placeholder_counter[0] += 1
        placeholder = f"__TEMP{_placeholder_counter[0]}__"
        inverted_index[placeholder] = inner_result  # temp store result

        query = query[:open_] + placeholder + query[close + 1:]

    # dectect OR query using the Re
    or_parts = re.split(r"\bOR\b", query)
    if len(or_parts) > 1:
        result = set()
        for part in or_parts:
            result = result | boolean_query(part.strip(), inverted_index, all_doc_ids)
        return result

    #detect AND query using RE
    and_parts = re.split(r"\bAND\b", query)
    if len(and_parts) > 1:
        
        result = all_doc_ids.copy()
        for part in and_parts:
            result = result & boolean_query(part.strip(), inverted_index, all_doc_ids)
        return result

    #handle NOT query
    not_match = re.match(r"^NOT\s+(.+)$", query, re.IGNORECASE)
    if not_match:
        inner = not_match.group(1).strip()
        inner_result = boolean_query(inner, inverted_index, all_doc_ids)
        return all_doc_ids - inner_result

    #a basic single term query requires no splitting
    term = query.strip()

    
    if term in inverted_index and isinstance(inverted_index[term], set):
        result = inverted_index[term].copy()
        #cleaning  of temp place holder so it does not take up index space
        if term.startswith("__TEMP"):
            del inverted_index[term]
        return result

    # regular vocabulary term
    return get_postings(term, inverted_index)



def proximity_query(t1, t2, k, positional_index):
   
   #words appearing at at distance to each other 
   # t1.t2 stemming both to be processes
    t1 = stemming(t1.lower().strip())
    t2 = stemming(t2.lower().strip())
    k = int(k)

    #using t1 t2 positional index to finding the common docs
    docs_t1 = set(positional_index.get(t1, {}).keys())
    docs_t2 = set(positional_index.get(t2, {}).keys())
    common_docs = docs_t1 & docs_t2

    result = set()
    for doc_id in common_docs:
        positions_t1 = positional_index[t1][doc_id]
        positions_t2 = positional_index[t2][doc_id]
        found = False
        for p1 in positions_t1:
            if found:
                break
            for p2 in positions_t2:
                if abs(p1 - p2) <= k:
                    result.add(doc_id)
                    found = True
                    break  # stop checking positions 

    return result


def query_type(query_str, inverted_index, positional_index, all_doc_ids):
    #strips query and checks wether it has and or not so it is a boolean quesry 
    query_str = query_str.strip()

    #if poximity query checks word 1 word2 and doc num
    prox_match = re.match(r"^(\w+)\s+(\w+)\s*/(\d+)$", query_str)
    if prox_match:
        t1 = prox_match.group(1)
        t2 = prox_match.group(2)
        k = prox_match.group(3)
        return proximity_query(t1, t2, int(k), positional_index)

    
    return boolean_query(query_str, inverted_index, all_doc_ids)
