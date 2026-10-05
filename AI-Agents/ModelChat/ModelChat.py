from langchain_openai import ChatOpenAI
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

model = ChatOpenAI(model='gpt-4.1', temperature=0.7, max_tokens=10)

result = model.invoke("What is the capital of France?")

print(result)
