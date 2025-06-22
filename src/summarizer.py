import os
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage

load_dotenv()

# Initialize model
llm = ChatOpenAI(model="gpt-3.5-turbo", temperature=0.2)

def generate_summary(text, context="Summarize this research paper:"):
    if not text.strip():
        return "No content to summarize."

    if len(text.split()) > 3000:
        text = " ".join(text.split()[:3000])  # Trim input for token limits

    prompt = f"{context}\n\n{text}"
    response = llm.invoke([HumanMessage(content=prompt)])
    return response.content
