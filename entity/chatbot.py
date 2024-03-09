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
        self.system = "You are a hotel host chatbot. Your answers are short and restricted to the exact informantion that you need to know."
        self.question_dict = {
            'name': {
                'prompt': f'{self.system} The client just started the conversation. Elaborate a question to know the name of your interlocutor',
                'value': None
                },
            'checkin': {
                'prompt': f'{self.system} Elaborate a short question to know the date of checkin',
                'value': None
                },
            'checkout': {
                'prompt': f'{self.system} Elaborate a short question to know the day of checkout',
                'value': None
                },
            'guesses': {
                'prompt': f'{self.system} Elaborate a short question to know the number of guesses',
                'value': None
            },
            'room': {
                'prompt': f'{self.system} Elaborate a short question to know the room size. The available sizes are BIG, SMALL and MEDIUM',
                'value': None
            },
            'payment': {
                'prompt': f'{self.system} Elaborate a short question to know what payment method the client prefer, the available options are CREDIT CARD or DEPOSIT',
                'value': None 
            },
            'breakfast': {
                'prompt': f'{self.system} Elaborate a short question to know what will be the breakfast plan, the availabel options are NO BREAKFAST, FULL BREAKFAST',
                'value': None
            },
            'restrictions': {
                'prompt': f'{self.system} Elaborate a short question to know if the client have some dietary restrictions',
                'value': None
            },
            'referral': {
                'prompt': f'{self.system} Elaborate a short question to know how did the customer find out about the hotel',
                'value': None
            },
            'driver': {
                'prompt': f'{self.system} Elaborate a short question to know whether the customer will need a driver or transfer service',
                'value': None
            },
            'finish': {
                'prompt': f'{self.system} You need to end the conversation now. Say thanks and good bye.',
                'value': 'finish'
            }
        }
        self.prompt = None
        self.next_question = None
        self.next_step = None

    def get_next_question(self):
        for key in self.question_dict:
            if self.question_dict[key]['value'] is None:
                self.next_step = key
                self.next_question = self.question_dict[key]['prompt']
                break
            self.next_question = self.question_dict['finish']['prompt']

    def switch_to_questions(self):
        self.prompt = ChatPromptTemplate.from_messages([
            ("system", f"{self.next_question}"),
            ("user", "{input}")
        ])

    def switch_to_ner(self, field):
        self.prompt = ChatPromptTemplate.from_messages([
            ("system", f"You are a Named Entity Recognozer system. Answer only the {field} in the input."),
            ("user", "{input}")
        ])

    def save_on_memory(self, field, value):
        self.question_dict[field]['value'] = value
