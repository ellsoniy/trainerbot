from langchain_groq import ChatGroq
from langchain_core.tools import Tool
from langchain_core.prompts import PromptTemplate
from langchain_core.runnables import RunnablePassthrough
from duckduckgo_search import DDGS
import os
from dotenv import load_dotenv
load_dotenv()

def search(query):
    with DDGS() as ddgs:
        results = ddgs.text(query, max_results=3)
        return "\n".join([r['body'] for r in results])

llm = ChatGroq(api_key=os.getenv("GROQ_API_KEY")
               , model="llama-3.3-70b-versatile")

# Bind tools directly to LLM
llm_with_tools = llm.bind_tools([
    {
        "type": "function",
        "function": {
            "name": "search",
            "description": "Search internet for current information",
            "parameters": {
                "type": "object",
                "properties": {
                    "query": {"type": "string"}
                },
                "required": ["query"]
            }
        }
    }
])

question = input("Ask agent: ")
response = llm_with_tools.invoke(question)

# Check if tool was called
if response.tool_calls:
    query = response.tool_calls[0]['args']['query']
    search_result = search(query)
    final = llm.invoke(f"Question: {question}\nSearch result: {search_result}\nAnswer:")
    print("\nFinal Answer:", final.content)
else:
    print("\nFinal Answer:", response.content)