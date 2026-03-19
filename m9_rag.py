from langchain_chroma import Chroma
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
import os
from dotenv import load_dotenv
load_dotenv()

# 1. Load PDF
loader = PyPDFLoader("UPW Master Deck.pdf")
pages = loader.load()

# 2. Split into chunks
splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)
chunks = splitter.split_documents(pages)


# Clean special characters
for chunk in chunks:
    chunk.page_content = chunk.page_content.encode('utf-8', 'ignore').decode('utf-8')


# 3. Embed + store
embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
db = Chroma.from_documents(chunks, embeddings)

# 4. Prompt
prompt = ChatPromptTemplate.from_messages([
    ("system", "Answer using only this context:\n{context}"),
    ("human", "{question}")
])

llm = ChatGroq(api_key=os.getenv("GROQ_API_KEY")
               , model="llama-3.3-70b-versatile")
chain = prompt | llm | StrOutputParser()

# 5. Ask
question = input("Ask about your PDF: ")
results = db.similarity_search(question, k=3)
context = "\n".join([r.page_content for r in results])
print(chain.invoke({"context": context, "question": question}))