import json, os
from query_router.openai_client import OpenAIClient
from retriever.Custom_BM25.bm25_search import BM25Searcher
from retriever.reranker.bge_reranker import BGEReranker, load_doc_content
from generator.generator import PRTSClient

# Pipeline: query_routing->BM25search->BGEreranker

def main():
    router_client = OpenAIClient()
    print("Routing server is running...")
    bm25 = BM25Searcher(index_path='retriever/Custom_BM25/bm25_index.json',
                        stopwords_path='retriever/Custom_BM25/stopwords.txt')
    print("BM25 index loaded.")
    reranker = BGEReranker(use_fp16=False)  # 设置为 True 可加速但可能略微降低精度
    print("BGE reranker loaded.")

    bot_client = PRTSClient()

    while True:
        query = input("请输入查询（exit退出）：").strip()
        if query.lower() == 'exit':
            break
        # try:
        # 使用 OpenAIClient 进行查询路由
        target_folders = router_client.evaluate_statements(query)
        print(f"路由到目标子文件夹：{target_folders}")
        target_folders_lst = []
        for item in target_folders:
            if target_folders[item]:
                target_folders_lst.append(item)

        # 使用 BM25 获取 Top20 候选文档
        candidates_raw = bm25.search(query, top_k=10, target_folders=target_folders_lst)

        candidate_docs = []
        for path, score, title in candidates_raw:
            path = path.replace('../../', '')
            print(path)
            content = load_doc_content(path)
            candidate_docs.append({'title': title, 'path': path, 'content': content})

        if not candidate_docs:
            continue

        reranked = reranker.rerank(query, candidate_docs)

        print(f"\n重排后 Top {len(reranked)} 结果：")
        for rank, (score, doc) in enumerate(reranked, start=1):
            print(f"{rank}. [{score:.4f}] {doc['title']} - {doc['path']}")

        # 取top10作为提供的文档池
        top_k_docs = reranked[:3]
        document = ""
        for rank, (score, doc) in enumerate(top_k_docs, start=1):
            document += f"{doc['title']} - {doc['content']}\n\n"

        input_str = f"以下是与查询相关的文档列表：\n{document}\n\n请根据这些文档回答以下问题：\n{query}"
        print(input_str)
        # 使用 PRTSClient 生成最终回答
        cnt = 0
        while cnt < 5:
            try:
                response = bot_client.evaluate_statements(input_str)
                print(f"生成的回答：{response}")
                break
            except:
                cnt += 1

        # except Exception as e:
        #     print(f"发生错误 {e}，请检查输入或系统状态。")
        #     continue


if __name__ == '__main__':
    main()
