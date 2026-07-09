from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_community.vectorstores import Chroma

from app.services.pdf_service import process_uploaded_pdf
from app.services.llm_service import get_answer_from_pdf

app = FastAPI(title="Gemini AI PDF Analyzer", version="2.0")

# Activate CORS so your frontend index.html can seamlessly talk to this backend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Global reference to hold active session vectors in memory
vector_store = None

class QueryRequest(BaseModel):
    question: str

@app.post("/upload", summary="Upload and Index a PDF")
async def upload_pdf(file: UploadFile = File(...)):
    global vector_store
    
    if not file.filename.endswith('.pdf'):
        raise HTTPException(status_code=400, detail="Only PDF files are supported.")
    
    try:
        # Extract text chunks
        splits = process_uploaded_pdf(file)
        
        # FIXED: Removed 'temperature=0' parameter to ensure clean initialization
        embeddings = GoogleGenerativeAIEmbeddings(model="gemini-embedding-001")
        vector_store = Chroma.from_documents(documents=splits, embedding=embeddings)
        
        return {"status": "Success", "message": f"'{file.filename}' processed and embedded."}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Upload processing failed: {str(e)}")

@app.post("/ask", summary="Query PDF Content")
async def ask_pdf(payload: QueryRequest):
    global vector_store
    
    if vector_store is None:
        raise HTTPException(status_code=400, detail="Please upload a PDF first.")
    
    try:
        answer = get_answer_from_pdf(vector_store, payload.question)
        return {"question": payload.question, "answer": answer}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Query resolution failed: {str(e)}")