# PRTS-Bot: A Knowledge Driven Arknights Chatbot
We want to construct a knowledge based chatbot for Arknights.

The key feature of PRTS-Bot is that it can answer questions about Arknights using the knowledge base from the PRTS wiki.

## Structure
The project is structured as follows:

### rewriter
The rewriter is responsible for rewriting the user query into more reasonable, clear and fine grained queries. It uses LLM to rewrite user query into one or more queries to retrieve the relevant pages.

### retriever
The retriever is responsible for retrieving the relevant pages from the local database. More details can be found in PRTS-Bot Retriever section.

### reranker
The reranker is responsible for reranking the retrieved pages based on their relevance to the user query. It uses LLM to rerank the pages and select the most relevant ones.

### generator
The generator is responsible for generating the final answer based on the retrieved pages. It uses LLM to generate the answer and format it in a user-friendly way.

## PRTS-Bot Retriever
In PRTS-Bot, we introduce our MediaWiki-based search engine, PRTS-Bot Retriever (PRTSBR). This part also serves as the course project for the Information Retrieval course at Nanjing University.

### Components
- **Crawler**: The crawler is responsible for crawling the PRTS wiki and downloading the pages. It uses the MediaWiki API to download the pages in XML format.
- **Indexer**: The indexer is responsible for indexing the downloaded pages and storing them in a local database. It uses the Whoosh library to create an inverted index for fast retrieval.
- **Retriever**: The retriever is responsible for retrieving the relevant pages from the local database. It uses the Whoosh library to search for the relevant pages based on the user query.