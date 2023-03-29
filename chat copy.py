import pinecone 
from langchain.vectorstores import Pinecone
from langchain.embeddings import OpenAIEmbeddings
from langchain.llms import OpenAI
from langchain.chains.question_answering import load_qa_chain

OPENAI_API_KEY = "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"
PINECONE_API_KEY = '64a2192e-42ae-466b-a79c-b9e0a2e73d87'
PINECONE_API_ENV = 'us-east1-gcp'


#for v2
import openai
openai.api_key = OPENAI_API_KEY
embed_model = "text-embedding-ada-002"

  
    

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
        resp = get_response_v2(ticker, sentence, OPENAI_API_KEY)
        print(resp)
