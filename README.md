# 🤖 PRTS-Bot: A Knowledge Driven Arknights Chatbot

We aim to construct a knowledge-based chatbot for Arknights.

The key feature of PRTS-Bot is its ability to answer questions about Arknights using the knowledge base from the PRTS wiki.

## 🗂 Project Structure

The project is structured as follows:

### ✍️ Rewriter

The Rewriter is responsible for rewriting the user query into more reasonable, clear, and fine-grained queries. It uses a large language model (LLM) to rewrite the user query into one or more queries to retrieve relevant pages.

### 🔀 Query Router

The Query Router determines the target subclassification of documents based on the user query. It uses a large language model (LLM) to classify the user query into one or more of the predefined categories.
The categories are subfolders in the `data/documents` directory, which contains the documents for each category.
In PRTS-Bot, we directly scan the folders in `data/documents` and classify the user query into one or more of the predefined categories.

### 🔍 Retriever

The Retriever is responsible for retrieving relevant pages from the local database. More details can be found in the **PRTS-Bot Retriever** section.


### 📝 Generator

The Generator produces the final answer based on the retrieved pages. It uses an LLM to generate and format the answer in a user-friendly way.

## 📚 PRTS-Bot Retriever

In PRTS-Bot, we introduce our MediaWiki-based search engine, **PRTS-Bot Retriever (PRTSBR)**. This component also serves as the course project for the Information Retrieval course at Nanjing University.

### 🧩 Components

- 🕷️ **Crawler**  
  Responsible for crawling the PRTS wiki and downloading pages. It uses the MediaWiki API to download pages in XML format. This can also fit other wikis that support the MediaWiki API.

- 🗂️ **Processor**
  Responsible for the stopword removal and text cleaning of the downloaded pages. In `file_process.py`, using jieba to segment Chinese text.

- 📖 **Indexer**  
  Responsible for indexing the downloaded pages and storing them in a local database. 

- 📂 **Retriever**  
  Responsible for retrieving relevant pages from the local database.

- 🔄 **Reranker**
  The Reranker reranks the retrieved pages based on their relevance to the user query. It uses BGE model to rerank pages using vector based method and select the most relevant ones.

### 🔗 Usage
To Start the PRTS-Bot Retriever, run the following scripts:

```bash
cd crawler
python3 cate_xml_download.py
python3 xml2txt.py
```
This command start the crawler, which will download the pages from the PRTS wiki and process them into text documents. You can change the base URL and categories in `crawler/cate_xml_download.py` to crawl other wikis that support the MediaWiki API.


To index the downloaded pages (using BM25), run:
```bash
cd retriever/Custom_BM25
python3 file_process.py
python3 indexer.py
```
This will process the downloaded pages and index them using BM25. The indexed pages will be stored in the `retriever/Custom_BM25/` directory. You can customize the stopwords and other parameters in `retriever/Custom_BM25/file_process.py` and `retriever/Custom_BM25/stopwords.txt`.

To rerank the retrieved pages using BGE or e5, run:
```bash
cd reranker
python3 bge_reranker.py
```
or
```bash
cd reranker
python3 e5_reranker.py
```

`NOTE: The reranker need to be run under GPU environment, and the BGE model requires about 3GB in memory, so make sure you have enough GPU memory.`

As for course project in IR class, the result is presented within the output of reranker. We can enter the query and get the reranked results shown in the terminal.


## 📄 Data Source & License Notice

This project uses data from [PRTS.wiki](https://prts.wiki/), which is licensed under the **Creative Commons Attribution-NonCommercial-ShareAlike 4.0 International (CC BY-NC-SA 4.0)** license.

Please note:

-  The **data** in this project is subject to the terms of the **CC BY-NC-SA 4.0** license:
  -  **Attribution** is required.
  -  **NonCommercial** use only — commercial usage is **not allowed**.
  -  **ShareAlike** — any modifications must be shared under the same license.

-  The **code** in this repository is licensed under the **MIT License** and may be used freely under its terms.

>  If you use this project or its data, please ensure you comply with the relevant licenses for each component.

For more information about the data license, see [https://creativecommons.org/licenses/by-nc-sa/4.0/](https://creativecommons.org/licenses/by-nc-sa/4.0/)
