import pinecone 
import datetime
from langchain.vectorstores import Pinecone
from langchain.embeddings import OpenAIEmbeddings
from langchain.llms import OpenAI
from langchain.chains.question_answering import load_qa_chain
from langchain.agents import initialize_agent, Tool, load_tools
from langchain.chains.conversation.memory import ConversationBufferMemory
import openai
import os
import dotenv

dotenv.load_dotenv()

OPENAI_API_KEY = os.environ.get('OPENAI_API_KEY')
PINECONE_API_KEY = os.environ.get('PINECONE_API_KEY')
PINECONE_API_ENV = os.environ.get('PINECONE_API_ENV')
#for v2

openai.api_key = OPENAI_API_KEY
embed_model = "text-embedding-ada-002"

os.environ["OPENAI_API_KEY"] = OPENAI_API_KEY
os.environ["SERPAPI_API_KEY"] = os.environ.get('SERPAPI_API_KEY')

llm=OpenAI(temperature=0, verbose=True)

pinecone.init(
    api_key=PINECONE_API_KEY,
    environment=PINECONE_API_ENV
)

bot_name = "Sam"
def get_response(index_name, msg, OPENAI_API_KEY):
    embeddings = OpenAIEmbeddings(openai_api_key=OPENAI_API_KEY) #setup embedding hook
    index_name.lower() #this will be the name of the dataset (ticker, company name, etc.)
    llm = OpenAI(temperature=0, openai_api_key=OPENAI_API_KEY)
    chain = load_qa_chain(llm, chain_type="stuff")
    docsearch = Pinecone.from_existing_index(index_name, embeddings)
    docs = docsearch.similarity_search(msg, include_metadata=True)
    output = chain.run(input_documents=docs, question=msg)
    return output

embed_model = "text-embedding-ada-002"

def get_response_v2(index_name, query, OPENAI_API_KEY ):
    primer = f"""You are Q&A bot. A highly intelligent system that answers
    user questions based on the information provided by the user above
    each question. If the information can not be found in the information
    provided by the user you truthfully say "I don't have information about that.".
    """
    res = openai.Embedding.create(
        input=[query],
        engine=embed_model
    )

    # retrieve from Pinecone
    xq = res['data'][0]['embedding']
    index = pinecone.GRPCIndex(index_name)
    # get relevant contexts (including the questions) from pinecone
    res = index.query(xq, top_k=5, include_metadata=True)
    # get list of retrieved text
    contexts = [item['metadata']['text'] for item in res['matches']]
    augmented_query = "\n\n---\n\n".join(contexts)+"\n\n-----\n\n"+query
 
    res = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": primer},
            {"role": "user", "content": augmented_query}
        ]
    )
    return res['choices'][0]['message']['content']


langtools = load_tools(["serpapi","llm-math"], llm=llm)
#tools += langtools
tools=langtools  

#session_state["agent_memory"] 
mem =  ConversationBufferMemory(memory_key="chat_history") # You can use other memory types as well!
agent_chain = initialize_agent(tools,  llm, agent="conversational-react-description", memory=mem, verbose=False) # verbose=True to see the agent's thought process

    
def get_response_v3(index_name, query, OPENAI_API_KEY ):
    # this is going to use agent/tools
    current_datetime_utc = datetime.datetime.utcnow()
    q2 = f"The current date/time is: {current_datetime_utc}. In relation to the company with ticker symbol {index_name.upper()}, provide a detailed and professional answer with no additional commentary regarding the following question: {query}"
    return agent_chain.run(input=q2) 
    




# this is the real time chat and it is NOT USED BY THE CHAT WINDOW
if __name__ == "__main__":
    print("Real Time Chat Test chat! (type 'quit' to exit)")
    while True:
        # Get input from the user
        sentence = input("You: ")
        # Exit the program if the user types 'quit'
        if sentence == "quit":
            break
        ticker = "tsla".lower()
        # Get a response from the chatbot and print it to the console
        resp = get_response_v3(ticker, sentence, OPENAI_API_KEY)
        print(resp)
