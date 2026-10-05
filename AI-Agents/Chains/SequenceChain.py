from langchain_openai import ChatOpenAI
from dotenv import load_dotenv, parser
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser

# Load environment variables
load_dotenv()

model = ChatOpenAI(model='gpt-4.1', temperature=0.7, max_tokens=1000)

template1 = PromptTemplate(
    template="What is are 5 interesting facts about {country}?",
    input_variables=["country"]
)

template2 = PromptTemplate(
    template="Generate a Summary of the following text: {text}",
    input_variables=["text"]
)

parser = StrOutputParser()

chain = template1 | model | parser | template2 | model | parser

result = chain.invoke({'country':'India'})
print(result)