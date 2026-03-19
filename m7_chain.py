from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.output_parsers import StrOutputParser
from langchain_core.messages import HumanMessage, AIMessage
import os
from dotenv import load_dotenv
load_dotenv()

# 1. LLM
llm = ChatGroq(
   api_key=os.getenv("GROQ_API_KEY"),
   model="llama-3.3-70b-versatile"
)

# # 2. Prompt template
# prompt = ChatPromptTemplate.from_messages([
#     ("system", "You are a helpful Singapore training assistant."),
#     ("human", "{question}")
# ])

prompt = ChatPromptTemplate.from_messages([
    ("system", "You are a helpful Singapore training assistant."),
    MessagesPlaceholder(variable_name="history"),
    ("human", "{question}")
])

chain = prompt | llm | StrOutputParser()

# Memory stored here
history = []

while True:
    user_input = input("You: ")
    if user_input == "quit":
        break
    
    response = chain.invoke({
        "question": user_input,
        "history": history
    })

     # Save to memory
    history.append(HumanMessage(content=user_input))
    history.append(AIMessage(content=response))
    
    print(f"AI: {response}\n")



# # 3. LCEL chain — pipe operator connects everything
# chain = prompt | llm | StrOutputParser()

# chain.invoke({"question": "What is SkillsFuture?"})

# 4. Run it
# response = chain.invoke({"question": "What is SkillsFuture?"})
# print(response)

# user_input = input("Ask your question: ")
# response = chain.invoke({"question": user_input})
# print(response)