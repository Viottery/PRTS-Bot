import os
import sys
import torch
import torch.nn.functional as F
from torch import Tensor
from transformers import AutoTokenizer, AutoModel

# 动态导入 bm25_search
bm25_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'Custom_BM25'))
if bm25_path not in sys.path:
    sys.path.insert(0, bm25_path)
from bm25_search import BM25Searcher

def average_pool(last_hidden_states: Tensor, attention_mask: Tensor) -> Tensor:
    last_hidden = last_hidden_states.masked_fill(~attention_mask[..., None].bool(), 0.0)
    return last_hidden.sum(dim=1) / attention_mask.sum(dim=1)[..., None]

def load_doc_content(doc_path):
    try:
        with open(doc_path, 'r', encoding='utf-8') as f:
            lines = f.readlines()
        if len(lines) < 2:
            return ""
        return "".join(lines[1:]).strip()
    except Exception as e:
        print(f"无法读取文档 {doc_path}: {e}")
        return ""

class E5Reranker:
    def __init__(self, model_name='intfloat/multilingual-e5-small', device=None):
        self.device = device if device else ('cuda' if torch.cuda.is_available() else 'cpu')
        self.tokenizer = AutoTokenizer.from_pretrained(model_name)
        self.model = AutoModel.from_pretrained(model_name).to(self.device)

    def rerank(self, query, candidate_docs):
        """
        candidate_docs: list of dicts {'title':..., 'path':..., 'content':...}
        """
        inputs = [f"query: {query}"]
        doc_texts = [f"passage: {doc['content']}" if doc['content'] else f"passage: {doc['title']}" for doc in candidate_docs]
        inputs.extend(doc_texts)

        batch_dict = self.tokenizer(inputs, max_length=512, padding=True, truncation=True, return_tensors='pt').to(self.device)
        with torch.no_grad():
            outputs = self.model(**batch_dict)
        embeddings = average_pool(outputs.last_hidden_state, batch_dict['attention_mask'])
        embeddings = F.normalize(embeddings, p=2, dim=1)

        query_embedding = embeddings[0]
        doc_embeddings = embeddings[1:]
        scores = torch.matmul(doc_embeddings, query_embedding.unsqueeze(1)).squeeze(1).cpu().tolist()

        scored_docs = list(zip(scores, candidate_docs))
        scored_docs.sort(key=lambda x: x[0], reverse=True)
        return scored_docs

def main():
    bm25 = BM25Searcher(index_path='../Custom_BM25/bm25_index.json', stopwords_path='../Custom_BM25/stopwords.txt')
    reranker = E5Reranker()

    while True:
        query = input("请输入查询（exit退出）：").strip()
        if query.lower() == 'exit':
            break

        # 先用 BM25 拿 Top20 候选
        candidates_raw = bm25.search(query, top_k=20)

        candidate_docs = []
        for path, score, title in candidates_raw:
            content = load_doc_content(path)
            candidate_docs.append({'title': title, 'path': path, 'content': content})
        print(f"候选文档数: {len(candidate_docs)}")
        for rank, doc in enumerate(candidate_docs, start=1):
            print(f"{rank}. {doc['title']} - {doc['path']}")
        reranked = reranker.rerank(query, candidate_docs)

        print(f"\n重排后 Top {len(reranked)} 结果：")
        for rank, (score, doc) in enumerate(reranked, start=1):
            print(f"{rank}. [{score:.4f}] {doc['title']} - {doc['path']}")

if __name__ == '__main__':
    main()
