# Retriever Part: Main Retriever and Reranker.

`NOTE: The retriever need to be run after crawler.`
in PRTS-Bot, we introduce our MediaWiki-based search engine, **PRTS-Bot Retriever (PRTSBR)**. This component also serves as the course project for the Information Retrieval course at Nanjing University.

## Main Retriever
We use a custom BM25 as main retriever. in `Custom_BM25` folder, we have the following files:
- `file_process.py`: This file is responsible for processing the downloaded pages, including stopword removal and text cleaning. It uses jieba to segment Chinese text.
- `indexer.py`: This file is responsible for indexing the processed pages and storing them in a local database. It uses the BM25 algorithm to index the pages.
- `stopwords.txt`: This file contains the stopwords used for text cleaning. You can customize the stopwords according to your needs.
- `bm25_search.py`: This file is responsible for searching the indexed pages using the BM25 algorithm. It takes a user query and returns the top relevant pages.

## Reranker
We use dense retrieval methods to rerank the retrieved pages. In `reranker` folder, we have the following files:
- `bge_reranker.py`: This file is responsible for reranking the retrieved pages using the BGE model. It uses the BGE model to compute the relevance scores of the pages and returns the top relevant pages.
- `e5_reranker.py`: This file is responsible for reranking the retrieved pages using the e5 model. It uses the e5 model to compute the relevance scores of the pages and returns the top relevant pages.

also, we can use similar programs to adapt to other dense vector retriever or rerankers, such as `colbert`, `dpr`, etc. Just change the reranker file to use the corresponding model.

`NOTE: To have a faster running time, the dense models are put on GPU. Make sure you have enough GPU memory. The BGE model requires about 3GB in memory, while the e5 model requires about 1GB in memory.`

