import os
from dotenv import load_dotenv
from langchain.text_splitter import CharacterTextSplitter
from langchain.document_loaders import TextLoader
from langchain.chains import RetrievalQA
from langchain.vectorstores import Chroma
from langchain_openai import OpenAIEmbeddings, OpenAI  # ✅ Updated import

load_dotenv()
OPENAI_KEY = os.getenv("OPENAI_API_KEY")

def load_vectorstore():
    loader = TextLoader("backend/policy_rules/risk_policies.txt")
    docs = loader.load()

    splitter = CharacterTextSplitter(chunk_size=500, chunk_overlap=50)
    split_docs = splitter.split_documents(docs)

    embedding = OpenAIEmbeddings(openai_api_key=OPENAI_KEY)
    vectorstore = Chroma.from_documents(split_docs, embedding, persist_directory="embeddings/vector_store")
    return vectorstore

def get_rationale(customer_data: dict):
    vectorstore = load_vectorstore()
    retriever = vectorstore.as_retriever()

    llm = OpenAI(temperature=0, openai_api_key=OPENAI_KEY)

    prompt = f"""Customer Profile:
{customer_data}

Based on the above customer profile and internal risk policy rules, generate a human-readable explanation (approval/rejection rationale) for this credit application. Mention relevant rules used in your decision."""

    chain = RetrievalQA.from_chain_type(
        llm=llm,
        retriever=retriever,
        return_source_documents=True
    )

    result = chain.invoke({"query": prompt})  # ✅ Use invoke instead of deprecated run()
    return result["result"]
