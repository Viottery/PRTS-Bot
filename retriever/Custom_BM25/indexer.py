# indexer.py：倒排索引模块
import sys, json

def main():
    # if len(sys.argv) != 2:
    #     print("用法: python indexer.py <预处理后文档 JSON 文件>")
    #     sys.exit(1)
    # input_path = sys.argv[1]
    input_path = 'preprocessed.json'
    with open(input_path, 'r', encoding='utf-8') as f:
        docs = json.load(f)  # 加载预处理结果列表

    postings = {}    # 倒排索引：term -> {doc_id: tf, ...}
    doc_lens = {}    # 文档长度：doc_id -> len
    doc_titles = {}  # 文档标题：doc_id -> title
    doc_paths = {}   # 文档路径：doc_id -> path

    for doc in docs:
        doc_id = str(doc['id'])  # 转为字符串方便 JSON 保存
        tokens = doc['tokens']
        doc_titles[doc_id] = doc['title']
        doc_paths[doc_id] = doc['path']
        doc_lens[doc_id] = len(tokens)
        # 累计每个词在该文档中的词频
        for term in tokens:
            if term not in postings:
                postings[term] = {}
            postings[term][doc_id] = postings[term].get(doc_id, 0) + 1

    N = len(docs)                                      # 文档总数
    avg_len = sum(doc_lens.values()) / N               # 平均文档长度
    # 准备保存的索引数据
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
