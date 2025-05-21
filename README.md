# 🤖 PRTS-Bot: A Knowledge Driven Arknights Chatbot

We aim to construct a knowledge-based chatbot for Arknights.

The key feature of PRTS-Bot is its ability to answer questions about Arknights using the knowledge base from the PRTS wiki.

## 🗂 Project Structure

The project is structured as follows:

### ✍️ Rewriter

The Rewriter is responsible for rewriting the user query into more reasonable, clear, and fine-grained queries. It uses a large language model (LLM) to rewrite the user query into one or more queries to retrieve relevant pages.

### 🔍 Retriever

The Retriever is responsible for retrieving relevant pages from the local database. More details can be found in the **PRTS-Bot Retriever** section.

### 🔄 Reranker

The Reranker reranks the retrieved pages based on their relevance to the user query. It uses an LLM to rerank pages and select the most relevant ones.

### 📝 Generator

The Generator produces the final answer based on the retrieved pages. It uses an LLM to generate and format the answer in a user-friendly way.

## 📚 PRTS-Bot Retriever

In PRTS-Bot, we introduce our MediaWiki-based search engine, **PRTS-Bot Retriever (PRTSBR)**. This component also serves as the course project for the Information Retrieval course at Nanjing University.

### 🧩 Components

- 🕷️ **Crawler**  
  Responsible for crawling the PRTS wiki and downloading pages. It uses the MediaWiki API to download pages in XML format.

- 📖 **Indexer**  
  Responsible for indexing the downloaded pages and storing them in a local database. It uses the Whoosh library to create an inverted index for fast retrieval.

- 📂 **Retriever**  
  Responsible for retrieving relevant pages from the local database. It uses the Whoosh library to search based on the user query.

### 📄 Data Source & License Notice

This project uses data from [PRTS.wiki](https://prts.wiki/), which is licensed under the **Creative Commons Attribution-NonCommercial-ShareAlike 4.0 International (CC BY-NC-SA 4.0)** license.

Please note:

-  The **data** in this project is subject to the terms of the **CC BY-NC-SA 4.0** license:
  -  **Attribution** is required.
  -  **NonCommercial** use only — commercial usage is **not allowed**.
  -  **ShareAlike** — any modifications must be shared under the same license.

-  The **code** in this repository is licensed under the **MIT License** and may be used freely under its terms.

>  If you use this project or its data, please ensure you comply with the relevant licenses for each component.

For more information about the data license, see [https://creativecommons.org/licenses/by-nc-sa/4.0/](https://creativecommons.org/licenses/by-nc-sa/4.0/)
