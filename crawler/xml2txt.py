import os
import shutil
import re


def collect_all_files(folder_path):
    """
    Recursively collect all file paths in a folder.
    """
    all_files = []
    for root, _, files in os.walk(folder_path):
        for file in files:
            full_path = os.path.join(root, file)
            all_files.append(full_path)
    return all_files


def extract_wiki_text(xml_string):
    match = re.search(r"&lt;text[^&]*&gt;(.*?)&lt;/text&gt;", xml_string, re.DOTALL)
    if match:
        content = match.group(1)
        content = content.replace("&lt;", "<").replace("&gt;", ">").replace("&amp;", "&")
        return content.strip()
    return None

def extract_files_to_target(input_folder, output_base='../data/documents'):
    """
    process all files from input_folder to txt and save to ../data/documents/{folder_name}, preserving relative structure.
    """
    folder_name = os.path.basename(os.path.normpath(f"xmls/{input_folder}"))
    target_base = os.path.join(output_base, folder_name)

    all_files = collect_all_files(f"xmls/{input_folder}")
    print(f"Found {len(all_files)} files in 'xmls/{input_folder}'.")

    for filepath in all_files:
        with open(filepath, 'r', encoding='utf-8') as f:
            xml_content = f.read()

            text_content = extract_wiki_text(xml_content)
            if text_content:
                # Create the target directory structure
                relative_path = os.path.relpath(filepath, f"xmls/{input_folder}")
                target_path = os.path.join(target_base, os.path.dirname(relative_path))
                os.makedirs(target_path, exist_ok=True)

                # Save the extracted text to a .txt file
                output_file = os.path.join(target_base, os.path.splitext(os.path.basename(filepath))[0] + '.txt')

                with open(output_file, 'w', encoding='utf-8') as out_f:
                    out_f.write(text_content)
                print(f"Saved: {output_file}")


if __name__ == "__main__":
    # You can change the input folders here
    input_folders = ["干员", "技术性文档", "敌人"]
    for input_folder in input_folders:

        extract_files_to_target(input_folder)

        # The necessary code ends here. The following parts is specific process to some folders, if needed.

        # The following code is specific to the "干员" folder structure
        if input_folder == "干员":
            # 设置原始目录和目标目录
            source_folder = "../data/documents/干员"
            game_folder = os.path.join(source_folder, "游戏")
            story_folder = os.path.join(source_folder, "剧情")

            # 创建目标子目录（如果不存在）
            os.makedirs(game_folder, exist_ok=True)
            os.makedirs(story_folder, exist_ok=True)

            # 遍历所有 txt 文件
            for filename in os.listdir(source_folder):
                if filename.endswith(".txt"):
                    filepath = os.path.join(source_folder, filename)

                    # 读取文件内容
                    with open(filepath, "r", encoding="utf-8") as f:
                        content = f.read()

                    # 分割标记
                    split_marker = "==相关道具=="
                    if split_marker in content:
                        split_index = content.index(split_marker)

                        # 游戏部分：不包含分割符
                        game_content = content[:split_index]

                        # 剧情部分：包含分割符及其之后内容
                        story_content = content[split_index:]

                        # 写入“游戏”部分
                        with open(os.path.join(game_folder, filename), "w", encoding="utf-8") as f_game:
                            f_game.write(game_content.strip())

                        # 写入“剧情”部分
                        with open(os.path.join(story_folder, filename), "w", encoding="utf-8") as f_story:
                            f_story.write(story_content.strip())
                    else:
                        print(f"⚠️ 未找到分割符：{filename}")
                        with open(os.path.join(game_folder, filename), "w", encoding="utf-8") as f_game:
                            f_game.write(content.strip())
