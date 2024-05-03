import os
import firebase_admin
import pyttsx3
import streamlit as st
from PyPDF2 import PdfReader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_google_genai import GoogleGenerativeAIEmbeddings, ChatGoogleGenerativeAI
from langchain_community.vectorstores import FAISS
from langchain.chains.question_answering import load_qa_chain
from langchain.prompts import PromptTemplate
from dotenv import load_dotenv
from pathlib import Path
from firebase_admin import auth, exceptions, credentials, initialize_app
import asyncio
from httpx_oauth.clients.google import GoogleOAuth2
from pdf_utils import get_pdf_text, get_text_chunks, get_conversional_chain, get_vector_store


# Load environment variables from .env file
load_dotenv()


# Set up Google API key
os.environ["GOOGLE_API_KEY"] = "AIzaSyA-3ISr6EE5VZxRb59nmTBVSa2Cfb4pI-E"

#Initialise Firebase App
cred = credentials.Certificate("firebase.json")
try:
    firebase_admin.get_app()
except ValueError as e:
    initialize_app(cred)

# Initialize Google OAuth2 client
client_id = "1098334936655-d4f1bg1ujnoq8tlb06ngufmh5hg007un.apps.googleusercontent.com"
client_secret = "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"
redirect_url = "http://localhost:8501/"  # Your redirect URL

client = GoogleOAuth2(client_id=client_id, client_secret=client_secret)


st.session_state.email = ''

async def get_access_token(client: GoogleOAuth2, redirect_url: str, code: str):
    return await client.get_access_token(code, redirect_url)

async def get_email(client: GoogleOAuth2, token: str):
    user_id, user_email = await client.get_id_email(token)
    return user_id, user_email

def get_logged_in_user_email():
    try:
        query_params = st.experimental_get_query_params()
        code = query_params.get('code')
        if code:
            token = asyncio.run(get_access_token(client, redirect_url, code))
            st.experimental_set_query_params()

            if token:
                user_id, user_email = asyncio.run(get_email(client, token['access_token']))
                if user_email:
                    try:
                        user = auth.get_user_by_email(user_email)
                    except exceptions.FirebaseError:
                        user = auth.create_user(email=user_email)
                    st.session_state.email = user.email
                    return user.email
        return None
    except:
        pass


def show_login_button():
    authorization_url = asyncio.run(client.get_authorization_url(
        redirect_url,
        scope=["email", "profile"],
        extras_params={"access_type": "offline"},
    ))
    st.markdown(f'<a href="{authorization_url}" target="_self">Login</a>', unsafe_allow_html=True)
    get_logged_in_user_email()

def user_input(pdf_docs, user_question):
    embeddings = GoogleGenerativeAIEmbeddings(model="models/embedding-001")
    if not Path("index1.faiss").is_file():
        text = get_pdf_text(pdf_docs)
        text_chunks = get_text_chunks(text)
        get_vector_store(text_chunks)

    new_db = FAISS.load_local("index1.faiss", embeddings, allow_dangerous_deserialization=True)
    docs = new_db.similarity_search(user_question)
    chain = get_conversional_chain()
    response = chain({"input_documents": docs, "question": user_question}, return_only_outputs=True)
    return response["output_text"]

def main():
    st.set_page_config("Chat With PDF")
    st.header("Chat with PDF powered by Gemini pro🤖")

    pdf_docs = None

    st.sidebar.title("Menu:")
    st.sidebar.write("1. Upload your files")
    pdf_docs = st.sidebar.file_uploader("", type="pdf", accept_multiple_files=True)

    if pdf_docs:
        with st.spinner("Processing..."):
            text = get_pdf_text(pdf_docs)
            text_chunks = get_text_chunks(text)
            get_vector_store(text_chunks)

    user_question = st.text_input("Ask a Question here")
    if st.button("Find Answer"):
        if user_question:
            if pdf_docs:
                with st.spinner("Searching for answer..."):
                    reply = user_input(pdf_docs, user_question)
                    st.write("Reply: ", reply)
                    # Use pyttsx3 to read out the answer
                    engine = pyttsx3.init()
                    engine.setProperty('rate', 150)
                    engine.say(reply)
                    engine.runAndWait()
            else:
                st.warning("Please upload a PDF file first.")
        else:
            st.warning("Please enter a question.")

if __name__ == '__main__':
    main()
