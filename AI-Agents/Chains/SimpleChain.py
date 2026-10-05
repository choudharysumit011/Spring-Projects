from langchain_openai import ChatOpenAI
from dotenv import load_dotenv, parser
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser

# Load environment variables
load_dotenv()
model = ChatOpenAI(model='gpt-4.1', temperature=0.7, max_tokens=100)

template = PromptTemplate(
    template="What is are 5 interesting facts about {country}?",
    input_variables=["country"]
)   

parser = StrOutputParser()

chain = template | model | parser

final_output = chain.invoke({'country':'India'})
print(final_output)

chain.get_graph().print_ascii()