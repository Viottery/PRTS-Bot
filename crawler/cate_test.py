import requests

def get_page_categories(page_title):
    API_URL = 'https://prts.wiki/api.php'
    params = {
        'action': 'query',
        'format': 'json',
        'prop': 'categories',
        'titles': page_title,
        'cllimit': 'max'  # 获取所有分类
    }

    response = requests.get(API_URL, params=params)
    data = response.json()

    pages = data.get('query', {}).get('pages', {})
    for page_id, page_data in pages.items():
        categories = page_data.get('categories', [])
        category_titles = [cat['title'] for cat in categories]
        return category_titles

# 示例用法
page_title = '泰拉词库'  # 替换为您感兴趣的页面标题
categories = get_page_categories(page_title)
print(f'页面 "{page_title}" 所属的分类有：')
for category in categories:
    print(f'- {category}')
