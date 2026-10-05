from langchain_openai import OpenAIEmbeddings
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

embedding_model = OpenAIEmbeddings(model='text-embedding-3-small')

text = "What is the capital of France?"
embedding = embedding_model.embed_query(text)
print(embedding)