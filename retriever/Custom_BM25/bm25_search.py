# bm25_search.py：检索查询模块
import json, math, jieba, sys, re, string

# 分词并过滤停用词
def tokenize_query(query, stopwords):
    # 仅保留中文、字母和数字
    query = re.sub(r"[^\u4e00-\u9fa5A-Za-z0-9]+", " ", query)
    words = jieba.lcut(query)
    punctuation = set(string.punctuation + "，。！？、；：（）《》【】“”‘’")
    tokens = [w for w in words if w and w not in stopwords and w not in punctuation]
    return tokens

def main():
    # 加载倒排索引和元信息
    with open('bm25_index.json', 'r', encoding='utf-8') as f:
        index = json.load(f)
    postings = index['postings']
    doc_lens = index['doc_lens']
    doc_titles = index['doc_titles']
    doc_paths = index['doc_paths']
    N = index['N']
    avg_len = index['avg_len']

    # 加载停用词表
    stopwords = set()
    with open('stopwords.txt', 'r', encoding='utf-8') as f:
        for line in f:
            w = line.strip()
            if w:
                stopwords.add(w)

    # 接受用户查询输入
    query = input("请输入查询: ")
    query_terms = tokenize_query(query, stopwords)
    if not query_terms:
        print("查询词经过过滤后为空。")
        return

    # BM25 参数
    k1 = 1.5
    b = 0.75

    scores = {}  # 累计每个文档的得分
    for term in query_terms:
        if term not in postings:
            continue  # 查询词不在索引中
        posting = postings[term]      # dict: doc_id -> tf
        df = len(posting)
        # 计算 IDF
        idf = math.log((N - df + 0.5) / (df + 0.5) + 1e-9)
        # 遍历包含该词的所有文档，累加得分
        for doc_id, tf in posting.items():
            tf = int(tf)
            doc_len = float(doc_lens[doc_id])
            # BM25 词项得分公式
            score = idf * ( (tf * (k1 + 1)) / (tf + k1 * (1 - b + b * doc_len / avg_len)) )
            scores[doc_id] = scores.get(doc_id, 0.0) + score

    if not scores:
        print("未找到匹配文档。")
        return

    # 按得分排序，返回 Top-k 文档
    top_k = 5
    ranked = sorted(scores.items(), key=lambda x: x[1], reverse=True)
    print(f"Top {top_k} 检索结果：")
    for rank, (doc_id, score) in enumerate(ranked[:top_k], start=1):
        title = doc_titles.get(doc_id, "N/A")
        path = doc_paths.get(doc_id, "")
        print(f"{rank}. [{score:.4f}] {title} - {path}")

if __name__ == '__main__':
    main()
