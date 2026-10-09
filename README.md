Python commonly uses a virtual environment (venv) 
so each project can have its own dependencies.
python3 -m venv .venv

activate virtual env
source .venv/bin/activate

python version upgrade
brew --version
brew install python@3.11

recreate after upgrading
deactivate
rm -rf .venv
python3.11 -m venv .venv
source .venv/bin/activate

LLM SDK
pip install openai
pip show openai

SDK — the Python library you just installed
API client — OpenAI()
API request — responses.create(...)
Model — which LLM processes the request
Input/prompt — what we ask the LLM
Response object — what comes back
Tokens — how LLMs process text
Context — information available to the model

set openAI key
export OPENAI_API_KEY="YOUR_API_KEY_HERE"

don't have an OpenAI API key, so using a local embedding model.
pip install sentence-transformers

pip install numpy

FAISS - for vector indexing
pip install faiss-cpu
pip show faiss-cpu

Quadrant - vector DB
pip install qdrant-client
python app/qdrant_demo.py

ollama list
download ollama
https://ollama.com/download?utm_source=chatgpt.com
ollama --version

download model
ollama pull llama3
ollama run llama3 

pip install langchain-community
pip show langchain-community

pip install -U langchain-ollama

pip install -U langchain-qdrant

pip install -U langchain-huggingface


