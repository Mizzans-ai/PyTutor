#llm3.py
from langchain_ollama import OllamaLLM  # Updated import
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser


def llama3(role, prompt):
    llm = OllamaLLM(model="llama3.2")  # Using the updated OllamaLLM class


    prompt_template = ChatPromptTemplate.from_messages([
        ("system", role), ("user", prompt)
    ])


    output_parser = StrOutputParser()
    chain = prompt_template | llm | output_parser


    return chain.invoke({"question": prompt})



