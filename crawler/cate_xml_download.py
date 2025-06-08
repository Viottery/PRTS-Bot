# Description: This script downloads all pages in a specified category from the PRTS wiki and saves them as XML files in a folder named after the category.
import os
import requests
import time


def get_category_members(category_name, limit=500, sleep_time=1):
    S = requests.Session()
    URL = "https://prts.wiki/api.php"
    members = []
    cmcontinue = ""

    while True:
        PARAMS = {
            "action": "query",
            "format": "json",
            "list": "categorymembers",
            "cmtitle": f"Category:{category_name}",
            "cmlimit": limit,
        }
        if cmcontinue:
            PARAMS["cmcontinue"] = cmcontinue

        R = S.get(url=URL, params=PARAMS)
        DATA = R.json()

        members.extend(DATA["query"]["categorymembers"])

        if "continue" in DATA:
            cmcontinue = DATA["continue"]["cmcontinue"]
            time.sleep(sleep_time)  # To avoid hitting the API too hard
        else:
            break

    return members


def export_page_xml(title):
    API_URL = 'https://prts.wiki/api.php'
    params = {
        'action': 'query',
        'format': 'xml',
        'export': '1',
        'titles': title
    }
    response = requests.get(API_URL, params=params)
    if response.status_code == 200:
        return response.text
    else:
        print(f'导出页面 "{title}" 失败，状态码：{response.status_code}')
        return None


def save_xml_to_folder(xml_content, folder_name, file_name):
    # 创建文件夹（如果不存在）
    os.makedirs(folder_name, exist_ok=True)
    # 构建完整的文件路径
    file_path = os.path.join(folder_name, f"{file_name}.xml")
    # 保存 XML 内容到文件
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(xml_content)
    print(f'页面 "{file_name}" 已保存到 {file_path}')


# 主程序
if __name__ == "__main__":
    categories = ["干员", "技术性文档", "敌人"]  # You can modify this list to include other categories you want to download
    for category in categories:

        pages = get_category_members(category)
        folder_name = category

        for page in pages:
            title = page['title']
            xml_content = export_page_xml(title)
            if xml_content:
                # Replace non-alphanumeric characters in the title to create a safe filename
                safe_title = "".join(c if c.isalnum() or c in " _-" else "_" for c in title)
                save_xml_to_folder(xml_content, folder_name, safe_title)
                time.sleep(0.3)  # To avoid hitting the API too hard
