# Import necessary libraries
import os
import tempfile
import streamlit as st
from embedchain import App
import base64
import pandas as pd
import docx2txt
from streamlit_chat import message

# Define the embedchain_bot function
def embedchain_bot(db_path):
    return App.from_config(
        config={
            "llm": {"provider": "ollama", "config": {"model": "llama3.2:latest", "max_tokens": 250, "temperature": 0.5, "stream": True, "base_url": 'http://localhost:11434'}},
            "vectordb": {"provider": "chroma", "config": {"dir": db_path}},
            "embedder": {"provider": "ollama", "config": {"model": "llama3.2:latest", "base_url": 'http://localhost:11434'}},
        }
    )

# Function to display PDF
def display_pdf(file):
    base64_pdf = base64.b64encode(file.read()).decode('utf-8')
    pdf_display = f'<iframe src="data:application/pdf;base64,{base64_pdf}" width="100%" height="400" type="application/pdf"></iframe>'
    st.markdown(pdf_display, unsafe_allow_html=True)

# Function to process DOCX files
def display_docx(file):
    text = docx2txt.process(file)
    st.text_area("DOCX Content Preview", text, height=300)
    return text

# Function to process CSV files
def display_csv(file):
    df = pd.read_csv(file)
    st.dataframe(df)
    return df.to_string()

st.title("Chat with Your Documents using Llama 3.2")
st.caption("This app allows you to chat with PDFs, DOCX, and CSV files using Llama 3.2 running locally with Ollama!")

# Define the database path
db_path = tempfile.mkdtemp()

# Create a session state to store the app instance and chat history
if 'app' not in st.session_state:
    st.session_state.app = embedchain_bot(db_path)
if 'messages' not in st.session_state:
    st.session_state.messages = []

# Sidebar for file upload and preview
with st.sidebar:
    st.header("Upload Documents")

    # Multiple File Upload (Simulating Folder Upload)
    uploaded_files = st.file_uploader("Upload multiple files (PDF, DOCX, CSV)", type=["pdf", "docx", "csv"], accept_multiple_files=True)

    if uploaded_files:
        st.subheader("Files Preview")
        for uploaded_file in uploaded_files:
            st.write(f"📄 {uploaded_file.name}")

        if st.button("Add Files to Knowledge Base"):
            with st.spinner("Adding files to knowledge base..."):
                for uploaded_file in uploaded_files:
                    file_ext = uploaded_file.name.split('.')[-1].lower()

                    # Define data type based on file extension (String-based)
                    if file_ext == "pdf":
                        data_type = "pdf_file"
                    elif file_ext == "docx":
                        data_type = "docx"
                    elif file_ext == "csv":
                        data_type = "csv"
                    else:
                        st.warning(f"❌ Unsupported file format: {file_ext}")
                        continue  # Skip unsupported file types

                    # Save temporary file
                    with tempfile.NamedTemporaryFile(delete=False, suffix=f".{file_ext}") as f:
                        f.write(uploaded_file.getvalue())
                        file_path = f.name

                    # Add file to knowledge base and force index refresh
                    st.session_state.app.add(file_path, data_type=data_type)

                    # 🔥 Force Reloading of Knowledge Base
                    st.session_state.app = embedchain_bot(db_path)

                    # Remove temp file
                    os.remove(file_path)

                st.success(f"✅ Added {len(uploaded_files)} files to the knowledge base! Ready for queries.")

# Chat interface
for i, msg in enumerate(st.session_state.messages):
    message(msg["content"], is_user=msg["role"] == "user", key=str(i))

if prompt := st.chat_input("Ask a question about the documents"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    message(prompt, is_user=True)

    with st.spinner("Thinking..."):
        # 🔍 Debugging Step: Retrieve relevant documents before sending query to LLM
        retrieved_docs = st.session_state.app.query(prompt)

        if not retrieved_docs:
            response = "❌ No relevant information found in the uploaded documents."
        else:
            # st.write("🔍 **Debug:** Retrieved Docs Before LLM Call")
            # st.write(retrieved_docs)  # Show retrieved documents in the UI

            response = retrieved_docs  # Directly using `query()` output

        st.session_state.messages.append({"role": "assistant", "content": response})
        message(response)

# Clear chat history button
if st.button("Clear Chat History"):
    st.session_state.messages = []
