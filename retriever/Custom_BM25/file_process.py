# preprocess.py：文档预处理模块
import sys, os, json, jieba, re, string


# 加载停用词表
def load_stopwords(path):
    stopwords = set()
    with open(path, 'r', encoding='utf-8') as f:
        for line in f:
            w = line.strip()
            if w:
                stopwords.add(w)
    return stopwords


# 文本清洗分词函数：去除非中文字符，分词并过滤停用词和标点
def tokenize(text, stopwords):
    # 仅保留中文、字母和数字，将其他字符替换为空格
    text = re.sub(r"[^\u4e00-\u9fa5A-Za-z0-9]+", " ", text)
    # jieba 分词
    words = jieba.lcut(text)
    # 定义标点集合
    punctuation = set(string.punctuation + "，。！？、；：（）《》【】“”‘’")
    # 过滤停用词和标点
    tokens = [w for w in words if w and w not in stopwords and w not in punctuation]
    return tokens


def main():
    # if len(sys.argv) != 2:
    #     print("用法: python preprocess.py <输入目录>")
    #     sys.exit(1)
    # input_dir = sys.argv[1]
    stopwords = load_stopwords('stopwords.txt')  # 假设停用词表文件名为 stopwords.txt

    corpus = []
    doc_id = 0
    base_dir = '../../data/documents'
    for root, dirs, files in os.walk(base_dir):
        for filename in files:
            if not filename.endswith('.txt'):
                continue
            filepath = os.path.join(root, filename)
            with open(filepath, 'r', encoding='utf-8') as f:
                lines = f.readlines()
            if not lines:
                continue

            foldername = os.path.basename(root)
            orig_title = lines[0].strip()
            title = f"{foldername}_{orig_title}"

            content = "".join(lines[1:])
            tokens = tokenize(content, stopwords)

            corpus.append({
                'id': doc_id,
                'title': title,
                'tokens': tokens,
                'path': filepath
            })
            doc_id += 1

    with open('preprocessed.json', 'w', encoding='utf-8') as f:
        json.dump(corpus, f, ensure_ascii=False, indent=2)

    print(f"预处理完成，处理文档数: {doc_id}，结果已保存到 preprocessed.json")

if __name__ == '__main__':
    main()
