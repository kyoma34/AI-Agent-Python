# 🤖 AI Agent — Python & Ollama

A local AI chat agent and RAG (Retrieval-Augmented Generation) system built with Python and Ollama, allowing users to chat with a local LLM and query their own documents.

## 🚀 Features

- 💬 Interactive chat interface with a local LLM via Ollama
- 📄 RAG pipeline — feed your own documents and ask questions about them
- 🔒 Fully local — no API keys, no data sent to the cloud
- 🧠 Context-aware responses using document embeddings
- ⚡ Fast responses using locally hosted models (Llama, Mistral, etc.)

## 🛠️ Tech Stack

**Language:** Python  
**LLM Runtime:** Ollama  
**RAG / Embeddings:** LangChain / ChromaDB  
**Interface:** CLI / Terminal  

## 📋 Requirements

- Python 3.10+
- [Ollama](https://ollama.ai) installed and running
- A model pulled in Ollama (e.g. `ollama pull llama3`)

## ⚙️ Installation

```bash
# Clone the repository
git clone https://github.com/kyoma34/AI-Agent-Python.git
cd AI-Agent-Python

# Create a virtual environment
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

## ▶️ Running the Agent

```bash
# Make sure Ollama is running
ollama serve

# Start the chat agent
python main.py
```

## 📁 Project Structure

```
AI-Agent-Python/
├── main.py              # Entry point
├── agent.py             # Chat agent logic
├── rag.py               # RAG pipeline
├── documents/           # Drop your docs here (.pdf, .txt)
├── requirements.txt
└── README.md
```

## 💡 How RAG Works

1. Place your documents in the `/documents` folder
2. The app chunks and embeds them into a local vector store
3. When you ask a question, the agent retrieves the most relevant chunks
4. The LLM generates a response grounded in your documents

---
> Powered by Ollama 🦙 — 100% local, 100% private
