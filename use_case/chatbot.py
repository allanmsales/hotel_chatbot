from langchain_community.llms import Ollama
from langchain_core.output_parsers import StrOutputParser
from langchain_core.messages import HumanMessage, AIMessage
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain.chains import create_retrieval_chain
from entity.chatbot import Chatbot
from entity.database import Database
llm = Ollama(model="llama2")
output_parser = StrOutputParser()
chatbot = Chatbot()


def chatbot_interface(input):
    chatbot.chat_history.append(HumanMessage(content=input))
    chatbot.get_next_question()
    chatbot.switch_to_ner(chatbot.next_step)
    chain = chatbot.prompt | llm | output_parser
    question = chain.invoke({"input": f"{input}"})
    chatbot.save_on_memory(chatbot.next_step, question)
    chatbot.get_next_question()
    chatbot.switch_to_questions()
    document_chain = create_stuff_documents_chain(llm, chatbot.prompt)
    retrieval_chain = create_retrieval_chain(chatbot.retriever_chain, document_chain)
    question = retrieval_chain.invoke({"chat_history": chatbot.chat_history, "input": input})
    chatbot.get_answers()
    chatbot.chat_history.append(AIMessage(content=question['answer']))
    print(chatbot.next_step)
    if chatbot.next_step == 'finish':
        database = Database(chatbot.answers)
        database.save_data()
    return question['answer']
