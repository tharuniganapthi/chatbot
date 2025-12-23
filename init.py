
import os
import cohere


import comtypes
from langchain.chat_models import ChatOpenAI
from langchain.chains import LLMChain
from langchain.prompts import PromptTemplate
from io import BytesIO


os.environ["OPENAI_API_KEY"] = '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'



bo = cohere.Client("mZCbnBDOvBtOuJw6HeHYGBnc1b6r11839JVMhp3s")
co = cohere.Client("G73sHe2ITKfFitJHFJNJR61gWIwxWjQzOc2wqNk3")
template = """Question: {question}
Answer: """
prompt = PromptTemplate.from_template(template)
llm = ChatOpenAI(openai_api_key=os.environ["OPENAI_API_KEY"], model_name="gpt-3.5-turbo-0125",temperature=0)
llm_chain = LLMChain(prompt=prompt,llm=llm,verbose=True)
print(llm_chain.run("hello"))