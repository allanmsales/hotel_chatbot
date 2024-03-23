# hotel_chatbot
Chatbot for a hotel

# Ubuntu – 22.04.4
# Python version – 3.9.12

- $ git clone https://github.com/allanmsales/hotel_chatbot
- $cd hotel_chatbot
- $ python3 -m venv env
- $ source env/bin/activate

# Installation
- $ pip install -r requirements.txt

# Install Ollama (https://github.com/ollama/ollama):
- $ curl -fsSL https://ollama.com/install.sh | sh
- $ sudo systemctl start ollama
- $ ollama run llama2
- $ ollama pull llama2

# Start Chatbot:
- $ python3 main.py

# Try it out:
- http://localhost:8080/chatbot/front

# Docs:
- http://localhost:8080/docs
