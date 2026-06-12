import os
import ollama

from langchain_community.document_loaders import (
    TextLoader,
    PyPDFLoader
)

from langchain_text_splitters import (
    RecursiveCharacterTextSplitter
)

from langchain_huggingface import (
    HuggingFaceEmbeddings
)

from langchain_community.vectorstores import (
    Chroma
)


DATA_FOLDER = "data/interview_materials"
VECTOR_DB = "vector_db"


def load_documents():

    documents = []

    for file in os.listdir(DATA_FOLDER):

        path = os.path.join(DATA_FOLDER, file)

        if file.endswith(".txt"):

            loader = TextLoader(
                path,
                encoding="utf-8"
            )

            documents.extend(
                loader.load()
            )

        elif file.endswith(".pdf"):

            loader = PyPDFLoader(path)

            documents.extend(
                loader.load()
            )

    return documents


def create_vector_db():

    documents = load_documents()

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=200
    )

    chunks = splitter.split_documents(
        documents
    )

    embeddings = HuggingFaceEmbeddings(
        model_name="all-MiniLM-L6-v2"
    )

    vectordb = Chroma.from_documents(
        documents=chunks,
        embedding=embeddings,
        persist_directory=VECTOR_DB
    )

    return vectordb



def get_relevant_docs(query):

    embeddings = HuggingFaceEmbeddings(
        model_name="all-MiniLM-L6-v2"
    )

    vectordb = Chroma(
        persist_directory=VECTOR_DB,
        embedding_function=embeddings
    )

    docs = vectordb.similarity_search(
        query,
        k=3
    )

    return docs


def ask_interview_coach(question):

    docs = get_relevant_docs(question)

    context = "\n\n".join(
        [doc.page_content for doc in docs]
    )

    prompt = f"""
    Answer the question using the provided context.

    Context:
    {context}

    Question:
    {question}

    Answer:
    """

    response = ollama.chat(
        model="qwen2.5:1.5b",
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ]
    )

    return response["message"]["content"]