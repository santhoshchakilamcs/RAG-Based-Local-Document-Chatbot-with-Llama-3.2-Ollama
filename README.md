# RAG-Based-Local-Document-Chatbot-with-Llama-3.2-Ollama

## 🚀 Overview
This project is a **local RAG-based chatbot** that allows users to upload and query **PDF, DOCX, and CSV files** using **Llama 3.2** running on **Ollama**. It supports **real-time document monitoring**, meaning any new file added to the selected folder is **automatically** indexed in the knowledge base.

## 🎯 Features
- ✅ **Supports PDFs, DOCX, and CSV files**
- ✅ **Real-time folder monitoring** (auto-updates when new files are added)
- ✅ **Local LLM execution using Ollama**
- ✅ **Conversational Q&A, summarization, and document retrieval**
- ✅ **Built-in Streamlit UI** for a seamless user experience

## 🛠️ Installation
### **1️⃣ Install Dependencies**
```bash
pip install streamlit embedchain pandas docx2txt base64
```

### **2️⃣ Download and Run Ollama**
- Install Ollama: [https://ollama.com/download](https://ollama.com/download)
- Run Ollama in the background:
```bash
ollama serve
```
- Pull Llama 3.2 model for local execution:
```bash
ollama run llama3.2
```

### **3️⃣ Run the RAG Chatbot**
```bash
streamlit run app.py
```

## 📂 How to Use
### **1️⃣ Upload different types of files**
- Users can **upload individual files** that the app will monitor.

### **2️⃣ Ask Questions**
- Use the **chat interface** to ask questions about the uploaded documents.
- The chatbot retrieves relevant document content and provides answers using **Llama 3.2**.

### **3️⃣ Clear Chat History**
- Click **Clear Chat History** to start fresh with new queries.

## 📌 Example Usage
```text
User: What are the key points in the uploaded research paper?
Assistant: Here are the main takeaways...

User: Summarize the contents of the contract document.
Assistant: This document outlines...
```

## 🔧 Future Enhancements
- ⏳ **Fine-tuning the RAG pipeline** for better retrieval.
- ⏳ **Adding multi-user support** with authentication.
- ⏳ **Expanding to additional file types (e.g., XLSX, JSON).**



## Source Citations (new)

Every assistant answer now ends with a citation line, for example:

```text
Sources: paper.pdf; contract.docx
```

- The line lists the files currently in the knowledge base, in the
  order they were uploaded.
- Page and section are shown only when a source record actually
  provides them, using `citations.format_citation`. The current
  embedchain `query()` call in `application.py` returns an answer
  string, not per-chunk page numbers, so this version cites file
  names only and does not invent page numbers.
- The helper lives in `citations.py` and is imported by
  `application.py`; uploaded file names are tracked in
  `st.session_state.source_files`.

## Ollama Setup (honest requirements)

- Install Ollama from https://ollama.com/download, then run
  `ollama serve` and `ollama pull llama3.2` (the app config uses
  model `llama3.2:latest` against `http://localhost:11434`).
- Inference stays local: the LLM, embedder, and vector store all run
  on your machine via Ollama and Chroma. No document text is sent to
  a hosted LLM by this app.
- Note: the existing run instruction in this README says
  `streamlit run app.py`, but the Streamlit file in this repo is
  `application.py`; run `streamlit run application.py` instead.
