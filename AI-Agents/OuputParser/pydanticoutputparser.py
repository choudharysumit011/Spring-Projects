from langchain_openai import ChatOpenAI
from dotenv import load_dotenv
from pydantic import BaseModel, Field
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import PydanticOutputParser

load_dotenv()
model = ChatOpenAI(model='gpt-5.2', temperature=0.7, max_tokens=1000)

class UserInfo(BaseModel):
    name: str = Field(description="The Full name of person")
    age: int = Field(description="The age of person")
    city: str = Field(description="The persons's city of residence")


parser = PydanticOutputParser(pydantic_object=UserInfo)

template = PromptTemplate(
    template="Extract this persons {input_text} information from wikipedia \n{format_instruction}",
    input_variables=["input_text"],
    partial_variables={'format_instruction': parser.get_format_instructions()}
)

chain = template | model | parser

final_output = chain.invoke({'input_text':'MS Dhoni'})
print(final_output)
                            