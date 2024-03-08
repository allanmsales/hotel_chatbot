from entity.chatbot import Chatbot
from langchain_community.llms import Ollama
from langchain_core.output_parsers import StrOutputParser
llm = Ollama(model="llama2")
output_parser = StrOutputParser()


def ner(input):
    chatbot = Chatbot()
    chatbot.get_next_question()
    chatbot.switch_to_ner()
    chain = chatbot.prompt | llm | output_parser
    question = chain.invoke({"input": f"{input}"})
    chatbot.save_on_memory(chatbot.next_question, question)
    print(chatbot.question_dict)
