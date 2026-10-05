from langchain_nvidia_ai_endpoints import ChatNVIDIA
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

model = ChatNVIDIA(model='meta/llama-4-maverick-17b-128e-instruct',max_completion_tokens=13107, temperature=0.7)

while True:
    user_input = input("User: ")
    if user_input.lower() in ['exit', 'quit']:
        print("Exiting the chat.")
        break
    result = model.invoke(user_input)
    print("NVIDIA Chatbot:", result.content)    