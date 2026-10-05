from langchain_openai import OpenAI
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

llm = OpenAI(model='gpt-4.1')

result = llm.invoke("What is the capital of France?")

print(result)