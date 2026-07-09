import os
import shutil
from fastapi import UploadFile
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from app.config import settings

def process_uploaded_pdf(file: UploadFile) -> list:
    # Ensure the temp directory exists
    os.makedirs(settings.UPLOAD_DIR, exist_ok=True)
    file_path = os.path.join(settings.UPLOAD_DIR, file.filename)
    
    try:
        # Stream the uploaded file to disk
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
            
        # Load the PDF content
        loader = PyPDFLoader(file_path)
        docs = loader.load()
        
        # Split document into chunks of 1000 characters with 200 overlap
        text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
        return text_splitter.split_documents(docs)
        
    finally:
        # Always remove the temporary file from local storage
        if os.path.exists(file_path):
            os.remove(file_path)