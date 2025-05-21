import requests

API_URL = 'https://prts.wiki/api.php'
params = {
    'action': 'query',
    'prop': 'revisions',
    'titles': '泰拉词库',
    'rvslots': '*',
    'rvprop': 'content',
    'format': 'json'
}

response = requests.get(API_URL, params=params)
data = response.json()

# 处理返回的数据
pages = data['query']['pages']
for page_id in pages:
    page = pages[page_id]
    title = page['title']
    content = page['revisions'][0]['slots']['main']['*']
    print(f"Title: {title}")
    print(f"Content:\n{content}")
