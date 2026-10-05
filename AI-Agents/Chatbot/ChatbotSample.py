from langchain_openai import ChatOpenAI
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
model = ChatOpenAI(model='gpt-5.2', temperature=0.7, max_tokens=100)

while True:
    user_input = input("You: ")
    if user_input.lower() in ['exit', 'quit']:
        print("Exiting the chatbot. Goodbye!")
        break
    response = model.invoke(user_input)
    print("Chatbot: " + response.content)