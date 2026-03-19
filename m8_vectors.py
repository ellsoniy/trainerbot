from langchain_chroma import Chroma
from langchain_core.documents import Document
from langchain_groq import ChatGroq
from langchain_huggingface import HuggingFaceEmbeddings

# Embedding model — runs locally, no API key needed
embeddings = HuggingFaceEmbeddings(
    model_name="all-MiniLM-L6-v2"
)

# 5 sample documents
docs = [
    Document(page_content="SkillsFuture gives Singaporeans $500 credit for courses"),
    Document(page_content="BELLS offers AI and tech courses in Singapore"),
    Document(page_content="Python is used for machine learning and AI development"),
    Document(page_content="LangChain connects LLMs with tools and data sources"),
    Document(page_content="ChromaDB stores text as vectors for similarity search"),
]

# Store in ChromaDB
db = Chroma.from_documents(docs, embeddings)

# Search by meaning
query = "how do I pay for AI courses?"
results = db.similarity_search(query, k=2)

print("Query:", query)
print("\nMost relevant:")
for r in results:
    print("-", r.page_content)