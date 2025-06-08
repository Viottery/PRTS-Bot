import json
import os
import sys
from pathlib import Path
from openai import OpenAI


class PRTSClient:
    def __init__(self, config_path: str = "config.secret.json", prompts_path: str = "prompts_generator.json"):
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
                  "system": "你是PRTS-Bot，《明日方舟》游戏的智能助手, 请根据用户给出的查询和我们提供的知识文档，给出恰当合理、有逻辑、并且适当可爱的回复。"
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

    def evaluate_statements(self, prompt: str, model: str = "o4-mini-2025-04-16") -> str:
        response = self.client.chat.completions.create(
            model=model,
            messages=[
                {"role": "system", "content": self.prompts["system"]},
                {"role": "user", "content": prompt}
            ],
        )
        arguments = str(response.choices[0].message.content)
        return arguments


if __name__ == "__main__":
    client = PRTSClient()
    print("Server is running...")
    prompt = input("请输入查询：")
    result = client.evaluate_statements(prompt)
    print(result)
