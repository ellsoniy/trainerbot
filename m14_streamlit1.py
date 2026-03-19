import streamlit as st
import tempfile
import os
from langchain_chroma import Chroma
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from dotenv import load_dotenv

load_dotenv()

st.title("TrainerBot")
st.caption("Ask your course materials anything")

uploaded = st.file_uploader("Upload PDF", type="pdf")

if uploaded:
    # Save uploaded file temporarily
    with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as f:
        f.write(uploaded.read())
        tmp_path = f.name

    with st.spinner("Reading PDF..."):
        loader = PyPDFLoader(tmp_path)
        pages = loader.load()
        splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)
        chunks = splitter.split_documents(pages)
        for chunk in chunks:
            chunk.page_content = chunk.page_content.encode('utf-8', 'ignore').decode('utf-8')
        embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
        db = Chroma.from_documents(chunks, embeddings)

    st.success("PDF loaded!")
    question = st.text_input("Your question:")

    if question:
        with st.spinner("Thinking..."):
            results = db.similarity_search(question, k=3)
            context = "\n".join([r.page_content for r in results])
            prompt = ChatPromptTemplate.from_messages([
                ("system", "Answer using only this context:\n{context}"),
                ("human", "{question}")
            ])
            llm = ChatGroq(model="llama-3.3-70b-versatile")
            chain = prompt | llm | StrOutputParser()
            answer = chain.invoke({"context": context, "question": question})
        st.write("**Answer:**", answer)
    
    os.unlink(tmp_path)