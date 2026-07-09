# 📄 AI PDF Analyzer

An AI-powered PDF Analyzer that allows users to upload PDF documents and ask questions in natural language. The application extracts text from uploaded PDFs, converts it into vector embeddings, retrieves the most relevant content using semantic search, and generates accurate answers using Google Gemini.

---

## 🚀 Features

* 📄 Upload PDF documents through a simple web interface
* 🤖 AI-powered question answering using Google Gemini
* 🔍 Semantic search with vector embeddings
* ⚡ FastAPI REST API backend
* 📚 Automatic PDF text extraction and chunking
* 🧠 Retrieval-Augmented Generation (RAG)
* 💾 In-memory Chroma vector database
* 🌐 Responsive HTML, CSS, and JavaScript frontend

---

## 🛠️ Tech Stack

### Frontend

* HTML5
* CSS3
* JavaScript

### Backend

* FastAPI
* Python

### AI & Machine Learning

* Google Gemini
* LangChain
* Gemini Embeddings
* ChromaDB

### Libraries

* PyPDF
* Python-dotenv
* Uvicorn

---

## 📁 Project Structure

```text
AI_PDF_ANALYZER/
│
├── app/
│   ├── services/
│   │   ├── pdf_service.py
│   │   └── llm_service.py
│   │
│   └── main.py
│
├── templates/
│   └── index.html
│
├── static/
│   ├── style.css
│   └── script.js
│
├── .env
├── requirements.txt
└── README.md
```

---

## ⚙️ Installation

### 1. Clone the Repository

```bash
git clone https://github.com/your-username/AI_PDF_ANALYZER.git
cd AI_PDF_ANALYZER
```

### 2. Create a Virtual Environment

Windows

```bash
python -m venv venv
venv\Scripts\activate
```

Linux/macOS

```bash
python3 -m venv venv
source venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure Environment Variables

Create a `.env` file in the project root.

```env
GEMINI_API_KEY=YOUR_API_KEY
```

---

## ▶️ Run the Application

Start the FastAPI server:

```bash
uvicorn app.main:app --reload
```

Open your browser and visit:

```
http://127.0.0.1:8000
```

Interactive API documentation:

```
http://127.0.0.1:8000/docs
```

---

## 📤 API Endpoints

### Upload PDF

**POST** `/upload`

Upload a PDF document for processing and indexing.

**Form Data**

```
file: document.pdf
```

---

### Ask Questions

**POST** `/ask`

**Request**

```json
{
  "question": "Summarize the document."
}
```

**Response**

```json
{
  "question": "Summarize the document.",
  "answer": "..."
}
```

---

## 🔄 How It Works

1. Upload a PDF document.
2. Extract text from the PDF.
3. Split the extracted text into smaller chunks.
4. Generate vector embeddings using Gemini Embeddings.
5. Store embeddings in ChromaDB.
6. Retrieve the most relevant chunks based on the user's query.
7. Pass the retrieved context to Google Gemini.
8. Return an accurate, context-aware response.

---

## 📦 Requirements

* Python 3.10+
* FastAPI
* Uvicorn
* LangChain
* langchain-google-genai
* ChromaDB
* PyPDF
* Python-dotenv

Install all dependencies using:

```bash
pip install -r requirements.txt
```

---

## 🔮 Future Improvements

* Multiple PDF uploads
* Persistent vector database
* Chat history
* Source references
* Authentication
* OCR support for scanned PDFs
* Docker deployment
* Cloud deployment

---

## 👨‍💻 Author

**Akmal Faraz**

B.Tech Computer Science Engineering

---

## 📄 License

This project is licensed under the MIT License.
