# indexer.py：The indexer.py script builds a BM25 reverser index from preprocessed documents.
import sys
import json


def main():
    # if len(sys.argv) != 2:
    #     print("用法: python indexer.py <预处理后文档 JSON 文件>")
    #     sys.exit(1)
    # input_path = sys.argv[1]
    input_path = 'preprocessed.json'
    with open(input_path, 'r', encoding='utf-8') as f:
        docs = json.load(f)  # Load preprocessed documents from JSON file

    postings = {}    # Reverse index:    term -> {doc_id: term frequency}
    doc_lens = {}    # Document lengths: doc_id -> length
    doc_titles = {}  # Document titles:  doc_id -> title
    doc_paths = {}   # Document paths:   doc_id -> path

    for doc in docs:
        doc_id = str(doc['id'])  # representing document ID as a string
        tokens = doc['tokens']
        doc_titles[doc_id] = doc['title']
        doc_paths[doc_id] = doc['path']
        doc_lens[doc_id] = len(tokens)
        # Count term frequency in the document
        for term in tokens:
            if term not in postings:
                postings[term] = {}
            postings[term][doc_id] = postings[term].get(doc_id, 0) + 1

    N = len(docs)                         # The total number of documents
    avg_len = sum(doc_lens.values()) / N  # Average document length
    # Save the index to a JSON file
    index_data = {
        'postings': postings,
        'doc_lens': doc_lens,
        'doc_titles': doc_titles,
        'doc_paths': doc_paths,
        'N': N,
        'avg_len': avg_len
    }
    with open('bm25_index.json', 'w', encoding='utf-8') as f:
        json.dump(index_data, f, ensure_ascii=False, indent=2)
    print(f"索引构建完成，文档总数: {N}，索引已保存到 bm25_index.json")


if __name__ == '__main__':
    main()
