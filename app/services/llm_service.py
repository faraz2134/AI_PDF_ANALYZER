# app/services/llm_service.py
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate

# Updated for modern LangChain Architecture
from langchain_classic.chains import create_retrieval_chain
from langchain_classic.chains.combine_documents import create_stuff_documents_chain

def get_answer_from_pdf(vector_store, question: str) -> str:
    # ... everything else in this file stays exactly the same
    # Retrieve top 4 most relevant text pieces
    retriever = vector_store.as_retriever(search_kwargs={"k": 4})
    
    # Initialize Google Gemini 2.5 Flash
    llm = ChatGoogleGenerativeAI(model="gemini-2.5-flash", temperature=0)
    
    # Define prompt behavior
    system_prompt = (
        "You are an expert document analysis assistant. Use the following pieces of retrieved context "
        "to answer the question. If you do not find the answer inside the context, clearly specify that "
        "the data is unavailable in the document.\n\n"
        "Context:\n{context}"
    )
    prompt = ChatPromptTemplate.from_messages([
        ("system", system_prompt),
        ("human", "{input}"),
    ])
    
    # Create the RAG execution chain
    question_answer_chain = create_stuff_documents_chain(llm, prompt)
    rag_chain = create_retrieval_chain(retriever, question_answer_chain)
    
    # Invoke and return response string
    response = rag_chain.invoke({"input": question})
    return response["answer"]