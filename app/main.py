from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_community.vectorstores import Chroma

from app.services.pdf_service import process_uploaded_pdf
from app.services.llm_service import get_answer_from_pdf

app = FastAPI(
    title="Gemini AI PDF Analyzer",
    version="2.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Stores the currently uploaded PDF
vector_store = None


class QueryRequest(BaseModel):
    question: str


def clear_vector_store():
    """
    Deletes the current Chroma collection and clears memory.
    """
    global vector_store

    if vector_store is not None:
        try:
            vector_store.delete_collection()
        except Exception:
            pass

    vector_store = None


@app.post("/new-chat", summary="Start New Conversation")
async def new_chat():
    clear_vector_store()

    return {
        "status": "Success",
        "message": "Conversation cleared successfully."
    }


@app.post("/upload", summary="Upload and Index PDF")
async def upload_pdf(file: UploadFile = File(...)):
    global vector_store

    if not file.filename.lower().endswith(".pdf"):
        raise HTTPException(
            status_code=400,
            detail="Only PDF files are supported."
        )

    try:
        # Remove previous PDF completely
        clear_vector_store()

        # Read and split PDF
        splits = process_uploaded_pdf(file)

        # Create embeddings
        embeddings = GoogleGenerativeAIEmbeddings(
            model="models/gemini-embedding-001"
        )

        # Create a fresh vector database
        vector_store = Chroma.from_documents(
            documents=splits,
            embedding=embeddings,
        )

        return {
            "status": "Success",
            "message": f"'{file.filename}' processed successfully."
        }

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Upload processing failed: {str(e)}"
        )


@app.post("/ask", summary="Ask Questions")
async def ask_pdf(payload: QueryRequest):
    global vector_store

    if vector_store is None:
        raise HTTPException(
            status_code=400,
            detail="Please upload a PDF first."
        )

    try:
        answer = get_answer_from_pdf(
            vector_store,
            payload.question
        )

        return {
            "question": payload.question,
            "answer": answer
        }

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Query resolution failed: {str(e)}"
        )