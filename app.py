import os
from api_key import OPENAI_API_KEY
import streamlit as st
from langchain.text_splitter import CharacterTextSplitter
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.vectorstores import FAISS
from langchain.chains.question_answering import load_qa_chain
from langchain.llms import OpenAI
from langchain.callbacks import get_openai_callback
from langchain.agents.agent_toolkits import create_vectorstore_agent, VectorStoreToolkit, VectorStoreInfo
from langchain.prompts import PromptTemplate
import io


os.environ["OPENAI_API_KEY"] = OPENAI_API_KEY

# Reading txt file
print("Reading File...")
pdf = io.open("corpus.txt", "r", encoding="utf-8").read()


print("Splitting Text...")
# Splitting document in to Text
text_splitter = CharacterTextSplitter(separator="\n", chunk_overlap=200, chunk_size=1000, length_function=len)
document = text_splitter.split_text(pdf)

print("Calling OpenAI Embeddings...")
embeddings = OpenAIEmbeddings()

# knowledge_base = Chroma.from_texts(document, embeddings)

print("Converting from text to embedding...")
knowledge_base = FAISS.from_texts(document, embeddings)

# print("Vector Store Info...")
# vector_store_info = VectorStoreInfo(name="TaxInfo", description="Tax on businesses in UAE", vectorstore=knowledge_base)
#
# print("Vector Store Toolkit...")
# vector_store_toolkit = VectorStoreToolkit(vectorstore_info=vector_store_info)

print("Calling OpenAI model...")
llm = OpenAI(temperature=0.9)

# print("Passing to Agent Vector..")
# agent_vec = create_vectorstore_agent(
#     llm=llm,
#     toolkit=vector_store_toolkit,
#     verbose=True
# )

print("Done")


st.set_page_config(page_title="TaxBusiness-GPT")
st.header("Personal-GPT :)")
st.write("A GPT that has information of tax laws for businesses in UAE")


user_question = st.text_input("Ask query:")

if user_question:
    try:
        vec = knowledge_base.similarity_search(user_question)
        chain = load_qa_chain(llm=llm, chain_type="stuff")

        print(chain.llm_chain.prompt.template)

        with get_openai_callback() as cb:
            response = chain.run(input_documents=vec, question=user_question)
            st.write(response)

    except Exception as e:
        print(e)
        st.error(str(e))
