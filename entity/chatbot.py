from langchain_core.prompts import ChatPromptTemplate
from langchain_community.embeddings import OllamaEmbeddings
from langchain_community.document_loaders import WebBaseLoader
from langchain_community.vectorstores import FAISS
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain.chains import create_retrieval_chain
from langchain_core.documents import Document
import json

class Chatbot:
    def __init__(self):
        self.question_dict = {
            'You need to know the name of your interlocutor': None,
            'You need to know the the day of checkin': None,
            'You need to know the the day of checkout': None,
            'You need to know the the number of guesses': None,
            'You need to know the the room size': None, #Not working
            'You need to know the the payment method': None,
            'You need to know what will be the breakfast plan': None, #Not worlking
            'You need to know if is there some dietary restrictions': None,
            'You need to know how did the customer find out about the hotel': None,
            'You need to know whether the customer will need a driver or transfer service': None,
            'finish': 'You are hotel host. You need to end the conversation now. Say thanks and good bye.' 
        }
        self.prompt = None
        self.next_question = None

    def get_next_question(self):
        for key in self.question_dict:
            if self.question_dict[key] is None:
                self.next_question = key
                break
            self.next_question = self.question_dict['finish']

    def switch_to_questions(self):
        self.prompt = ChatPromptTemplate.from_messages([
            ("system", f"{self.next_question}"),
            ("user", "{input}")
        ])

    def switch_to_ner(self):
        self.prompt = ChatPromptTemplate.from_messages([
            ("system", f"You are a Named Entity Recognozer system. Answer only the name in the input."),
            ("user", "{input}")
        ])

    def save_on_memory(self, field, value):
        self.question_dict[field] = value
