import streamlit as st 
import google.generativeai as genai 
import os 
from dotenv import load_dotenv 

# for pdf reader or writer
from PyPDF2 import PdfReader,PdfMerger,PdfWriter
# for pdf text splitter
from langchain.text_splitter import RecursiveCharacterTextSplitter 
# words embedding means convert into word vectorized 
from langchain_google_genai import GoogleGenerativeAIEmbeddings,ChatGoogleGenerativeAI
# from langchain.llms import GoogleGenerativeAI
from langchain.vectorstores import FAISS 
from langchain.chains.question_answering import load_qa_chain 
from langchain.prompts import PromptTemplate

## Load the variables environments:-
load_dotenv()
os.getenv("GOOGLE_API_SERVICE")

## configure the api key:-
genai.configure(api_key=os.getenv("GOOGLE_API_SERVICE"))

## function to load Gemini Pro model and get repsonses
#model=genai.GenerativeModel("gemini-pro") 


# PDF reader fun
def pdf_reader(pdf_file):
    text=""
    for pdf in pdf_file:
        pdf_reader = PdfReader(pdf)
        for page in pdf_reader.pages:
            text += page.extract_text()
    return text

# Chunck PDF 
def chunk_pdf(text):
    splitter = RecursiveCharacterTextSplitter(chunk_size=10000,chunk_overlap=1000)
    chunk_split = splitter.split_text(text)
    return chunk_split

# Get Vectors functions
def get_vectors(text):
    embeddings = GoogleGenerativeAIEmbeddings(model="models/embedding-001")
    vectors_store = FAISS.from_texts(text,embedding=embeddings)
    vectors_store.save_local("faiss_index") # faiss_index
    
def get_conversational_chain():
    prompt_template = """
    Answer the question as detailed as possible from the provided context, make sure to provide all the details, if the answer is not in
    provided context just say, "answer is not available in the context", don't provide the wrong answer\n\n
    Context:\n {context}?\n
    Question: \n{question}\n

    Answer:
    """
    model = ChatGoogleGenerativeAI(model="gemini-pro",
                             temperature=0.3)

    prompt = PromptTemplate(template = prompt_template, input_variables = ["context", "question"])
    chain = load_qa_chain(model, chain_type="stuff", prompt=prompt)
    return chain

def user_input(user_question):
    embedding_model = GoogleGenerativeAIEmbeddings(model = "models/embedding-001")
    
    new_db = FAISS.load_local("faiss_index", embedding_model,
                             allow_dangerous_deserialization=True  # Enable this only if you trust the source
    )
    docs = new_db.similarity_search(user_question)

    chain = get_conversational_chain()
    
    response = chain(
        {"input_documents":docs, "question": user_question}
        , return_only_outputs=False)

    print(response)
    st.write("Reply: ", response["output_text"])
    

def main():
    st.set_page_config("Chat With PDF-Summarazations!!!")
    st.header("Chat with PDF using Gemini💁")
    user_question = st.text_input("Ask a Question from the PDF Files")

    if user_question:
        user_input(user_question)

    with st.sidebar:
        st.title("Menu:")
        pdf_file = st.file_uploader("Upload your PDF Files and Click on the Submit & Process Button", accept_multiple_files=True) # True
        if st.button("Submit & Process"):
            with st.spinner("Processing..."):
                raw_text = pdf_reader(pdf_file)
                chunk_text = chunk_pdf(raw_text)
                get_vectors(chunk_text)
                st.success("Done")

if __name__ == "__main__":
    main()