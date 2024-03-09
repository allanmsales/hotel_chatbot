from entity.chatbot import Chatbot
from langchain_community.llms import Ollama
from langchain_core.output_parsers import StrOutputParser
llm = Ollama(model="llama2")
output_parser = StrOutputParser()
chatbot = Chatbot()

def chatbot_interface(input):
    chatbot.get_next_question()
    chatbot.switch_to_ner(chatbot.next_step)
    chain = chatbot.prompt | llm | output_parser
    question = chain.invoke({"input": f"{input}"})
    chatbot.save_on_memory(chatbot.next_step, question)
    chatbot.get_next_question()
    chatbot.switch_to_questions()
    chain = chatbot.prompt | llm | output_parser
    question = chain.invoke({"input": f"What else you need to know from me?"})
    chatbot.get_answers()
    print(chatbot.answers)
    return question
