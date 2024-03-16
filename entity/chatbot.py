from langchain_core.prompts import ChatPromptTemplate
from langchain_community.embeddings import OllamaEmbeddings
from langchain_community.document_loaders import WebBaseLoader
from langchain_community.vectorstores import FAISS
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain.chains import create_retrieval_chain
from langchain_core.documents import Document
import json

from langchain_community.document_loaders import WebBaseLoader
from langchain_community.embeddings import OllamaEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain_core.prompts import ChatPromptTemplate
from langchain_community.llms import Ollama
from langchain.chains import create_retrieval_chain
from langchain.chains import create_history_aware_retriever
from langchain_core.prompts import MessagesPlaceholder
from langchain_core.messages import HumanMessage, AIMessage
from langchain_core.documents import Document

class Chatbot:
    def __init__(self):
        self.system = "You are a hotel host chatbot. Your answers are short and restricted to the exact informantion that you need to know."
        self.ner = "You are a text extractor program. Your answer will be stored in a database, so you need to answer only the exact word that is asked, only one string in the answer."
        self.question_dict = {
            'name': {
                'prompt': f'{self.system} The client just started the conversation. Elaborate a question to know the name of your interlocutor',
                'ner': f'{self.ner} Extract the personal name in the input',
                'value': None
                },
            'checkin': {
                'prompt': f'{self.system} Elaborate a short question to know the date of checkin',
                'ner': f'{self.ner} Extract the date in the input and transform in the yyyy-mm-dd format',
                'value': None
                },
            'checkout': {
                'prompt': f'{self.system} Elaborate a short question to know the day of checkout',
                'ner': f'{self.ner} Extract the date in the input and transform in the yyyy-mm-dd format',
                'value': None
                },
            'guesses': {
                'prompt': f'{self.system} Elaborate a short question to know the number of guesses',
                'ner': f'{self.ner} Extract the number of guesses indicated by the input',
                'value': None
            },
            'room': {
                'prompt': f'{self.system} Elaborate a short question to know the room size. The available sizes are BIG, SMALL and MEDIUM',
                'ner': f'{self.ner} Extract the room size indicated by the input',
                'value': None
            },
            'payment': {
                'prompt': f'{self.system} Elaborate a short question to know what payment method the client prefer, the available options are CREDIT CARD or DEPOSIT',
                'ner': f'{self.ner} Extract the payment method indicated by the input',
                'value': None 
            },
            'breakfast': {
                'prompt': f'{self.system} Elaborate a short question to know what will be the breakfast plan, the availabel options are NO BREAKFAST, FULL BREAKFAST',
                'ner': f'{self.ner} Extract the breakfast plan indicated by the input',
                'value': None
            },
            'restrictions': {
                'prompt': f'{self.system} Elaborate a short question to know if the client have some dietary restrictions',
                'ner': f'{self.ner} Extract the dietary restictions indicated by the input',
                'value': None
            },
            'referral': {
                'prompt': f'{self.system} Elaborate a short question to know how did the customer find out about the hotel',
                'ner': f'{self.ner} Extract the referral indicated by the input',
                'value': None
            },
            'driver': {
                'prompt': f'{self.system} Elaborate a short question to know whether the customer will need a driver or transfer service',
                'ner': f'{self.ner} Extract YES or NO from the information if the client needs driver or transfor from what was indicated by the input',
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
        self.answers = None
        self.chat_history = [
            HumanMessage(content="Hi, I want to book a room."),
            AIMessage(content="Sure! Can you tell me your name, please?")
            ]

    def get_next_question(self):
        for key in self.question_dict:
            if self.question_dict[key]['value'] is None:
                self.next_step = key
                self.next_question = self.question_dict[key]['prompt']
                break
            self.next_step = 'finish'
            self.next_question = self.question_dict['finish']['prompt']

    def switch_to_questions(self):
        llm = Ollama(model="llama2")
        embeddings = OllamaEmbeddings()
        text_splitter = RecursiveCharacterTextSplitter()

        info = [Document(page_content="Our price is $100 per night. There are 3 types of rooms: BASIC, MEDIUM and BIG. The breakfast is served until 9:00 am.")]

        documents = text_splitter.split_documents(info)
        vector = FAISS.from_documents(documents, embeddings)
        retriever = vector.as_retriever()

        prompt = ChatPromptTemplate.from_messages([
            MessagesPlaceholder(variable_name="chat_history"),
            ("user", "{input}"),
            ("user", "Given the above conversation, generate a search query to look up in order to get information relevant to the conversation")
        ])

        self.retriever_chain = create_history_aware_retriever(llm, retriever, prompt)

        self.prompt = ChatPromptTemplate.from_messages([
            ("system", self.next_question + "Answer the user's questions based on the below context:\n\n{context}"),
            MessagesPlaceholder(variable_name="chat_history"),
            ("user", "{input}"),
        ])

    def switch_to_ner(self, key):
        self.prompt = ChatPromptTemplate.from_messages([
            ("system", self.question_dict[key]['ner']),
            ("user", "{input}")
        ])

    def save_on_memory(self, field, value):
        self.question_dict[field]['value'] = value


    def get_answers(self):
        answers = {}
        for key in self.question_dict:
            answers[key] = self.question_dict[key]['value']
        self.answers = answers
