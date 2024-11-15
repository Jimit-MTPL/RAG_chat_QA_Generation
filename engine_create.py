from llama_index.core.memory import ChatMemoryBuffer
from index_creater import new_index
from setup_chromadb import create_or_get_vectordb
from setup_embedding_model import embed_model


def create_chat_engine():

        #memory = ChatMemoryBuffer.from_defaults(token_limit=1500)
        index = new_index(create_or_get_vectordb(), embed_model())
        query_engine = index.as_chat_engine(
        chat_mode="context",
        #memory=memory,
        system_prompt= """
        You are tasked with generating high-quality, meaningful question-answer pairs from the provided context. 
        The questions should cover all key points in the text, be diverse, and not repetitive. 
        The answers should be detailed, conversational, accurate, and provide explanations where necessary. 
        Avoid using wording that directly refers back to the text (like "according to the text"). 
        Ensure each question is unique and comprehensive.

        Format your response like this:
        Question: [Insert question here]
        Answer: [Insert detailed, conversational answer here]

        Make sure:
        1. Each question addresses a different key aspect or detail from the text.
        2. The answers are well-explained, providing context or additional information when necessary.
        3. Both questions and answers should be clear and specific without direct references to phrases from the text.
        4. The questions should be open-ended (who, what, when, where, why, how) and encourage detailed responses.
                                                 
        generate maximum 3 question-answer pairs from the provided context.
        """
        )
        return query_engine
        

        

def interact_with_llm(customer_query):
        #print("Command: ", customer_query)
        chat_engine = create_chat_engine()
        
        AgentChatResponse = chat_engine.chat(customer_query)
        answer = AgentChatResponse.response
        return answer