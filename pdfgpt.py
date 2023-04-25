# reads pdf files in a directory and allows to run gpt queries on the data

import os
import sys
import langchain
import openai
from langchain.text_splitter import CharacterTextSplitter

def search_pdf_files(directory):
    pdf_files = []
    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.endswith(".pdf"):
                pdf_files.append(os.path.join(root, file))
    return pdf_files
import PyPDF2
def read_pdf_file(pdf_file):
    # read pdf file using pypdf
    pdf_text = ""
    with open(pdf_file, 'rb') as f:
        pdf = PyPDF2.PdfReader(f)
        for page in pdf.pages:
            pdf_text += page.extract_text()
    return pdf_text

def read_pdf_files(directory):
    pdf_files = search_pdf_files(directory)
    pdf_text = ""
    for pdf_file in pdf_files:
        pdf_text += read_pdf_file(pdf_file)
    split_text = langchain.text_splitter.CharacterTextSplitter(
        separator = "\n",
        chunk_size = 1000,
        chunk_overlap = 250,
        length_function = len,
    ).split_text(pdf_text)
    return split_text

from langchain.chains.question_answering import load_qa_chain
class PDFGPT:
    def __init__(self, directory):
        self.directory = directory
        self.split_text = read_pdf_files(directory)
        print(self.split_text)
        embeddings = langchain.embeddings.openai.OpenAIEmbeddings()
        self.search = langchain.vectorstores.FAISS.from_texts(self.split_text, embedding = embeddings)
        self.chain = load_qa_chain(langchain.llms.OpenAI(), chain_type = "stuff")


    def query(self, query):
        docs = self.search.similarity_search(query)
        print(self.chain.run(input_documents = docs, question = query))


if __name__ == "__main__":
    # load openai api key from .env file
    # read .env file
    openai_api_key = None
    with open(".env", "r") as f:
        for line in f.readlines():
            if line.startswith("OPENAI_API_KEY"):
                openai_api_key = line.split("=")[1].strip()
                os.environ["OPENAI_API_KEY"] = openai_api_key
    if os.getenv("OPENAI_API_KEY") == None:
        print("OPENAI_API_KEY not set")
        openai_api_key = input("Enter OPENAI_API_KEY: ")
        os.environ["OPENAI_API_KEY"] = openai_api_key

    pdfgpt = PDFGPT('/app/data_source')
    while True:
        query = input("Query: ")
        pdfgpt.query(query)

