import json
import os
import sys
from pathlib import Path
from openai import OpenAI


class OpenAIClient:
    def __init__(self, config_path: str = "config.secret.json", prompts_path: str = "prompts.json"):
        self.config = self._load_or_create_config(config_path)
        self.prompts = self._load_prompts(prompts_path)
        self.client = OpenAI(
            api_key=self.config["api_key"],
            base_url=self.config["base_url"]
        )

    def _load_or_create_config(self, path: str) -> dict:
        if not os.path.exists(path):
            default_config = {
                "api_key": "your-api-key",
                "base_url": "https://your-custom-base-url.com/v1"
            }
            with open(path, "w") as f:
                json.dump(default_config, f, indent=4)
            print(f"配置文件 '{path}' 已创建，请根据实际情况修改其中的 'api_key' 和 'base_url'。")
            sys.exit(1)
        with open(path, "r") as f:
            return json.load(f)

    def _load_prompts(self, path: str) -> dict:
        if not os.path.exists(path):
            print(f"提示词文件 '{path}' 不存在，请确保该文件存在并包含有效的 JSON 数据。")
            with open(path, "w", encoding="utf-8") as f:
                default_prompts = {
                  "system": "你是一个查询路由助手。",
                  "user": "请判断用户给出的查询应当路由到哪些明日方舟wiki相关的文档集："
                }
                json.dump(default_prompts, f, indent=4, ensure_ascii=False)
            sys.exit(1)
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)

    def _get_folders(self, base_path: str) -> list:
        leaf_folders = []
        for folder in Path(base_path).rglob('*'):
            if folder.is_dir():
                # 检查当前文件夹是否是叶节点文件夹
                if not any(child.is_dir() for child in folder.iterdir()):
                    folder_name = folder.relative_to(base_path).as_posix()
                    leaf_folders.append(folder_name)
        # print(leaf_folders)
        return leaf_folders

    def evaluate_statements(self, prompt: str, model: str = "gpt-4o-mini") -> dict:
        folders = self._get_folders("data/documents")
        num_statements = len(folders)

        statements = {f"{i+1}": folder for i, folder in enumerate(folders)}
        # print(statements)

        properties = {}
        for i in range(num_statements):
            properties[f"{statements[f'{i+1}']}"] = {
                "type": "boolean",
                "description": f"文档集：{statements[f'{i+1}']}"
            }
        # print(properties)

        function_schema = {
            "name": "evaluate_statements",
            "description": "根据用户的查询语义判断应当在哪些数据集检索文档",
            "parameters": {
                "type": "object",
                "properties": properties,
                "required": [f"{statements[f'{i+1}']}" for i in range(num_statements)],
                "additionalProperties": False
            }
        }

        # prompt = self.prompts["user"] + "\n" + "\n".join([f"{i+1}. {folder}" for i, folder in enumerate(folders)])
        # print("prompt: ")
        # print(prompt)
        response = self.client.chat.completions.create(
            model=model,
            messages=[
                {"role": "system", "content": self.prompts["system"]},
                {"role": "user", "content": prompt}
            ],
            tools=[{"type": "function", "function": function_schema}]
        )

        arguments = response.choices[0].message.tool_calls[0].function.arguments
        return json.loads(arguments)


if __name__ == "__main__":
    client = OpenAIClient()
    print("Server is running...")
    prompt = input("请输入查询：")
    result = client.evaluate_statements(prompt)
    print(result)
