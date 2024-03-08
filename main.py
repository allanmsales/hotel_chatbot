from langchain_community.llms import Ollama
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_community.embeddings import OllamaEmbeddings
from langchain_community.document_loaders import WebBaseLoader
from langchain_community.vectorstores import FAISS
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain.chains import create_retrieval_chain
from langchain_core.documents import Document
import json


question_dict = {
    'name': None,
    'day of checkin': None,
    'day of checkout': None,
    'number of guesses': None,
    'room size': None, #Not working
    'payment method': None,
    'breakfast plan': None, #Not worlking
    'dietary restrictions': None,
    'how did the customer find out about the hotel': None,
    'whether the customer will need a driver or transfer service': None
}

def build_prompt(question_dict):
        for key in question_dict:
            if question_dict[key] is None:
                prompt = ChatPromptTemplate.from_messages([
                    ("system", f"You are hotel host. You need to know the {key}."),
                    ("user", "{input}")
                ])
                return prompt
        prompt = ChatPromptTemplate.from_messages([
                ("system", f"You are hotel host. You need to end the conversation now. Say thanks and good bye."),
                ("user", "{input}")
            ])
        return prompt


def check_question():
    prompt = ChatPromptTemplate.from_messages([
        ("system", f"You are a Named Entity Recognozer system. Answer only the name in the input."),
        ("user", "{input}")
    ])
    return prompt


#prompt = build_prompt(question_dict)
prompt = check_question()

llm = Ollama(model="llama2")
output_parser = StrOutputParser()
chain = prompt | llm | output_parser


def make_question():
    question = chain.invoke({"input": f"My name is Jhon"})
    question_dict['name'] = question
    print(question_dict)


make_question()
