from langchain_community.document_loaders import PyPDFLoader
from langchain_community.retrievers import BM25Retriever


def build_retriever():

    loader = PyPDFLoader("data/bandaruvenkateshrao_resume.pdf")

    documents = loader.load()

    retriever = BM25Retriever.from_documents(documents)

    retriever.k = 4

    return retriever