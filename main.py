import json
import os
from time import sleep

from query_router.openai_client import OpenAIClient
from retriever.Custom_BM25.bm25_search import BM25Searcher
from retriever.reranker.bge_reranker import BGEReranker, load_doc_content
from generator.generator import PRTSClient

import botpy
from botpy import logging
from botpy.ext.cog_yaml import read
from botpy.message import GroupMessage, Message, C2CMessage
_log = logging.get_logger()


class MyClient(botpy.Client):
    async def on_ready(self):
        _log.info(f"robot 「{self.robot.name}」 on_ready!")
        self.router_client = OpenAIClient()
        print("Routing server is running...")
        self.bm25 = BM25Searcher(index_path='retriever/Custom_BM25/bm25_index.json',
                            stopwords_path='retriever/Custom_BM25/stopwords.txt')
        print("BM25 index loaded.")
        self.reranker = BGEReranker(use_fp16=False)  # 设置为 True 可加速但可能略微降低精度
        print("BGE reranker loaded.")

        self.bot_client = PRTSClient()
        print("PRTS client loaded.")

    async def on_group_at_message_create(self, message: GroupMessage):

        query = message.content
        try:
            # 使用 OpenAIClient 进行查询路由
            target_folders = self.router_client.evaluate_statements(query)
            print(f"路由到目标子文件夹：{target_folders}")
            target_folders_lst = []
            for item in target_folders:
                if target_folders[item]:
                    target_folders_lst.append(item)

            # 使用 BM25 获取 Top20 候选文档
            candidates_raw = self.bm25.search(query, top_k=10, target_folders=target_folders_lst)

            candidate_docs = []
            for path, score, title in candidates_raw:
                path = path.replace('../../', '')
                print(path)
                content = load_doc_content(path)
                candidate_docs.append({'title': title, 'path': path, 'content': content})

            if not candidate_docs:
                raise ValueError("No candidate documents found.")

            reranked = self.reranker.rerank(query, candidate_docs)

            print(f"\n重排后 Top {len(reranked)} 结果：")
            for rank, (score, doc) in enumerate(reranked, start=1):
                print(f"{rank}. [{score:.4f}] {doc['title']} - {doc['path']}")

            # 取top-k作为提供的文档池
            top_k_docs = reranked[:10]
            document = ""
            for rank, (score, doc) in enumerate(top_k_docs, start=1):
                if score >= 0.03:
                    document += f"{doc['title']} - {doc['content']}\n\n"

            input_str = f"以下是与查询相关的文档列表：\n{document}\n\n请根据这些文档回答以下的用户问题：\n{query}"
            print(input_str)
            # 使用 PRTSClient 生成最终回答
            cnt = 0
            response = ""
            exp = ""
            print("开始生成结果...")
            while cnt < 5:
                try:
                    response = self.bot_client.evaluate_statements(input_str)
                    print(f"生成的回答：{response}")
                    break
                except Exception as e:
                    cnt += 1
                    exp = e
                    sleep(3)
                    print(f"生成回答失败，正在重试... {e}")
                sleep(3)
            if not response:
                response = f"生成回答失败，请稍后再试。{exp}"
        except Exception as e:
            # 不用RAG，直接生成回答
            response = self.bot_client.evaluate_statements(query)
            print(f"RAG失败或没有候选文档，直接生成回答 {e}")

        messageResult = await message._api.post_group_message(
            group_openid=message.group_openid,
              msg_type=0,
              msg_id=message.id,
              content=f"{response}")
        _log.info(messageResult)

    async def on_c2c_message_create(self, message: C2CMessage):





        await message._api.post_c2c_message(
            openid=message.author.user_openid,
            msg_type=0, msg_id=message.id,
            content=f"我收到了你的消息：{message.content}"
        )


def main():
    test_config = read("config.yaml")
    print(test_config)
    intents = botpy.Intents(public_guild_messages=True, public_messages=True)
    client = MyClient(intents=intents, is_sandbox=True)
    client.run(appid=test_config["appid"], secret=test_config["secret"])


    #
    #
    # while True:
    #     query = input("请输入查询（exit退出）：").strip()
    #     if query.lower() == 'exit':
    #         break
    #     # try:
    #     # 使用 OpenAIClient 进行查询路由
    #     target_folders = router_client.evaluate_statements(query)
    #     print(f"路由到目标子文件夹：{target_folders}")
    #     target_folders_lst = []
    #     for item in target_folders:
    #         if target_folders[item]:
    #             target_folders_lst.append(item)
    #
    #     # 使用 BM25 获取 Top20 候选文档
    #     candidates_raw = bm25.search(query, top_k=10, target_folders=target_folders_lst)
    #
    #     candidate_docs = []
    #     for path, score, title in candidates_raw:
    #         path = path.replace('../../', '')
    #         print(path)
    #         content = load_doc_content(path)
    #         candidate_docs.append({'title': title, 'path': path, 'content': content})
    #
    #     if not candidate_docs:
    #         continue
    #
    #     reranked = reranker.rerank(query, candidate_docs)
    #
    #     print(f"\n重排后 Top {len(reranked)} 结果：")
    #     for rank, (score, doc) in enumerate(reranked, start=1):
    #         print(f"{rank}. [{score:.4f}] {doc['title']} - {doc['path']}")
    #
    #     # 取top10作为提供的文档池
    #     top_k_docs = reranked[:3]
    #     document = ""
    #     for rank, (score, doc) in enumerate(top_k_docs, start=1):
    #         document += f"{doc['title']} - {doc['content']}\n\n"
    #
    #     input_str = f"以下是与查询相关的文档列表：\n{document}\n\n请根据这些文档回答以下问题：\n{query}"
    #     print(input_str)
    #     # 使用 PRTSClient 生成最终回答
    #     cnt = 0
    #     while cnt < 5:
    #         try:
    #             response = bot_client.evaluate_statements(input_str)
    #             print(f"生成的回答：{response}")
    #             break
    #         except:
    #             cnt += 1

        # except Exception as e:
        #     print(f"发生错误 {e}，请检查输入或系统状态。")
        #     continue


if __name__ == '__main__':
    main()
