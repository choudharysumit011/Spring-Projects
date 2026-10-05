
from langchain_nvidia_ai_endpoints import ChatNVIDIA
from dotenv import load_dotenv

# Load environment variables
load_dotenv()


model = ChatNVIDIA(model='meta/llama-4-maverick-17b-128e-instruct', temperature=0.7, max_tokens=1000)
result = model.invoke("What is your capability, what can you do?")
print(result.content)



