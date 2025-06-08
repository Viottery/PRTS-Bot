# bge_reranker.py: BGE Reranker for BM25 Search Results, the main() serve as the entry point for the script.
import sys
import os
from FlagEmbedding import FlagReranker

os.environ['HF_ENDPOINT'] = 'https://hf-mirror.com'

# import bm25_search
bm25_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'Custom_BM25'))
if bm25_path not in sys.path:
    sys.path.insert(0, bm25_path)
from bm25_search import BM25Searcher


def load_doc_content(doc_path):
    """
    Load the content of a document, skipping the first line (usually a header).
    :param doc_path:
    :return: The content of the document as a string, excluding the first line.
    """
    with open(doc_path, 'r', encoding='utf-8') as f:
        lines = f.readlines()
    if len(lines) < 2:
        return ""
    return "".join(lines[1:]).strip()


class BGEReranker:
    """
    BGE Reranker for BM25 Search Results.
    """
    def __init__(self, model_name='BAAI/bge-reranker-v2-m3', device='cuda', use_fp16=False):
        self.reranker = FlagReranker(
            model_name,
            query_max_length=256,
            passage_max_length=4096,
            use_fp16=use_fp16,
            devices=[device] if device else None
        )

    def rerank(self, query, candidate_docs, normalize=True):
        """
        candidate_docs: list of dicts {'title':..., 'path':..., 'content':...}
        """
        pairs = [[query, doc['content'] if doc['content'] else doc['title']] for doc in candidate_docs]
        scores = self.reranker.compute_score(pairs, normalize=normalize)
        scored_docs = list(zip(scores, candidate_docs))
        scored_docs.sort(key=lambda x: x[0], reverse=True)
        return scored_docs


def main():
    bm25 = BM25Searcher(index_path='../Custom_BM25/bm25_index.json', stopwords_path='../Custom_BM25/stopwords.txt')
    reranker = BGEReranker(use_fp16=False)  # If use_fp16=True, it can speed up the process but may slightly reduce accuracy.

    while True:
        query = input("请输入查询（exit退出）：").strip()
        if query.lower() == 'exit':
            break

        # Get top 20 candidate documents using BM25
        candidates_raw = bm25.search(query, top_k=20)

        candidate_docs = []
        for path, score, title in candidates_raw:
            content = load_doc_content(path)
            candidate_docs.append({'title': title, 'path': path, 'content': content})

        if not candidate_docs:
            continue

        reranked = reranker.rerank(query, candidate_docs)

        print(f"\n重排后 Top {len(reranked)} 结果：")
        for rank, (score, doc) in enumerate(reranked, start=1):
            print(f"{rank}. [{score:.4f}] {doc['title']} - {doc['path']}")


if __name__ == '__main__':
    main()
