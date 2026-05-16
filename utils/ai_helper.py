import os
import google.generativeai as genai
from dotenv import load_dotenv
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS
from langchain_community.embeddings import HuggingFaceEmbeddings
load_dotenv()

api_key = os.getenv("GOOGLE_API_KEY")

print("API KEY:", api_key)

genai.configure(api_key=api_key)

# GEMINI MODEL
model = genai.GenerativeModel(
    "models/gemini-2.5-flash"
)


# SUMMARY FUNCTION
def generate_summary(text):

    prompt = f"""
    Summarize the following study material
    in simple and easy language.

    Text:
    {text[:4000]}
    """

    response = model.generate_content(prompt)

    return response.text


# QUESTION GENERATOR
def generate_questions(text):

    prompt = f"""
    Generate 10 important questions
    from the following material.

    Text:
    {text[:4000]}
    """

    response = model.generate_content(prompt)

    return response.text


# MCQ GENERATOR
def generate_mcqs(text):

    prompt = f"""
    Generate 10 MCQs from the following material.

    Format:

    Question
    A)
    B)
    C)
    D)
    Correct Answer:

    Text:
    {text[:4000]}
    """

    response = model.generate_content(prompt)

    return response.text

# CREATE VECTOR STORE
def create_vector_store(text):

    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=500,
        chunk_overlap=50
    )

    chunks = text_splitter.split_text(text)

    embeddings = HuggingFaceEmbeddings(
        model_name="sentence-transformers/all-MiniLM-L6-v2"
    )

    vector_store = FAISS.from_texts(
        chunks,
        embeddings
    )

    return vector_store

# CHAT WITH PDF
def ask_pdf_question(vector_store, question):

    docs = vector_store.similarity_search(question)

    context = " ".join([
        doc.page_content for doc in docs
    ])

    prompt = f"""
    Answer the question using the PDF content below.

    Context:
    {context}

    Question:
    {question}
    """

    response = model.generate_content(prompt)

    return response.text