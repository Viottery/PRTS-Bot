# preprocess.py：The text preprocessing module for the BM25 retriever
import sys, os, json, jieba, re, string


def load_stopwords(path):
    """
    Load stopwords from a file.
    :param path:
    :return: The set of stopwords loaded from the specified file.
    """
    stopwords = set()
    with open(path, 'r', encoding='utf-8') as f:
        for line in f:
            w = line.strip()
            if w:
                stopwords.add(w)
    return stopwords


def tokenize(text, stopwords):
    """
    Tokenize the input text, removing non-Chinese characters, stopwords, and punctuation.
    :param text:
    :param stopwords:
    :return: A list of tokens after preprocessing.
    """
    # Only keep Chinese characters, English letters, and digits
    text = re.sub(r"[^\u4e00-\u9fa5A-Za-z0-9]+", " ", text)
    # jieba tokenization
    words = jieba.lcut(text)
    # The set of punctuation characters to filter out
    punctuation = set(string.punctuation + "，。！？、；：（）《》【】“”‘’")
    # Filter out empty tokens, stopwords, and punctuation
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
            orig_title = filename.replace('.txt', '')
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
