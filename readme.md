## PDFGPT
### A GPT-3 based PDF query answering system

This is a simple demo of a GPT-3 based PDF query answering system. It reads all PDF files kept in data_source directory and generates embeddings for the data present in those PDFs. It then uses the embeddings to answer queries.

## How to run(containerised)
1. Install docker and docker-compose
2. Clone this repository
3. Set the environment variable `OPENAI_API_KEY` to your OpenAI API key in .env file, or in docker-compose.yml file, or enter it when prompted
4. Run `docker-compose run pdfgpt'
5. Wait for the container to build and start
6. When prompted, enter the query

