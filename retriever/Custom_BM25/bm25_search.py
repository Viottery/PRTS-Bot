import json
import math
import jieba
import re
import string
from typing import List, Tuple

class BM25Searcher:
    def __init__(self, index_path='bm25_index.json', stopwords_path='stopwords.txt'):
        self.index = self.load_index(index_path)
        self.postings = self.index['postings']
        self.doc_lens = self.index['doc_lens']
        self.doc_titles = self.index['doc_titles']
        self.doc_paths = self.index['doc_paths']
        self.N = self.index['N']
        self.avg_len = self.index['avg_len']

        self.stopwords = self.load_stopwords(stopwords_path)

        # BM25参数
        self.k1 = 1.5
        self.b = 0.75

    def load_index(self, path):
        with open(path, 'r', encoding='utf-8') as f:
            return json.load(f)

    def load_stopwords(self, path):
        stopwords = set()
        try:
            with open(path, 'r', encoding='utf-8') as f:
                for line in f:
                    w = line.strip()
                    if w:
                        stopwords.add(w)
        except FileNotFoundError:
            print(f"警告：停用词文件 {path} 不存在，未加载停用词。")
        return stopwords

    def tokenize_query(self, query: str) -> List[str]:
        query = re.sub(r"[^\u4e00-\u9fa5A-Za-z0-9]+", " ", query)
        words = jieba.lcut(query)
        punctuation = set(string.punctuation + "，。！？、；：（）《》【】“”‘’")
        tokens = [w for w in words if w and w not in self.stopwords and w not in punctuation]
        return tokens

    def search(self, query: str, top_k=5) -> List[Tuple[str, float, str]]:
        """
        输入查询，返回 Top-k 结果列表
        返回格式：[(文档路径, BM25得分, 文档标题), ...]
        """
        query_terms = self.tokenize_query(query)
        if not query_terms:
            print("查询词经过过滤后为空。")
            return []

        scores = {}
        for term in query_terms:
            if term not in self.postings:
                continue
            posting = self.postings[term]
            df = len(posting)
            idf = math.log((self.N - df + 0.5) / (df + 0.5) + 1e-9)
            for doc_id, tf in posting.items():
                tf = int(tf)
                doc_len = float(self.doc_lens[doc_id])
                score = idf * ((tf * (self.k1 + 1)) / (tf + self.k1 * (1 - self.b + self.b * doc_len / self.avg_len)))
                scores[doc_id] = scores.get(doc_id, 0.0) + score

        if not scores:
            print("未找到匹配文档。")
            return []

        ranked = sorted(scores.items(), key=lambda x: x[1], reverse=True)[:top_k]
        results = []
        for doc_id, score in ranked:
            title = self.doc_titles.get(doc_id, "N/A")
            path = self.doc_paths.get(doc_id, "")
            results.append((path, score, title))
        return results


# 如果直接执行此文件，支持命令行查询测试
if __name__ == '__main__':
    import sys
    bm25 = BM25Searcher()
    while True:
        query = input("请输入查询 (输入exit退出): ").strip()
        if query.lower() in ('exit', 'quit'):
            break
        results = bm25.search(query, top_k=5)
        print(f"Top {len(results)} 检索结果：")
        for rank, (path, score, title) in enumerate(results, start=1):
            print(f"{rank}. [{score:.4f}] {title} - {path}")
