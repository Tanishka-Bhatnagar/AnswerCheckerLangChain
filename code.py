# usning RunnableSequence instead of LLMChain as LLMChain is outdated not compatible with ChatGroq

import os
from langchain_groq import ChatGroq
from langchain.prompts import PromptTemplate
# from langchain.chains import LLMChain
from langchain.schema import BaseOutputParser
from langchain_core.runnables import RunnableSequence

# API Key
os.environ["GROQ_API_KEY"]="api_key"

class CodeOutputParser(BaseOutputParser):
    def parse(self,text : str)->bool:
        return "wrong" not in text.lower()

prompt_template_text="""You are a high school history teacher grading \
    homework assignments. Based on the homework question indicated by '**Q:**' 
    and the correct answer indicated by '**A:**', your task is to determine \
         whether the student's answer is correct. Grading is binary; therefore, \
             student answers can be correct or wrong. Simple misspellings are okay. 
              **Q:** {question}
              **A:** {correct_answer}
               
              **Student's Answer:** {student_answer}
                 """
prompt=PromptTemplate(
    input_variables=["question","correct_answer","student_answer"],\
    template=prompt_template_text)

llm=ChatGroq(model_name="llama3-8b-8192",
             temperature=0.3
             )
chain=prompt | llm | CodeOutputParser()

# single answer by student
question="who is prime minister of india?"
correct_answer="Narendra Modi"
student_answer="tanis"

result=chain.invoke({'question':question,'correct_answer':correct_answer,'student_answer':student_answer})
print(result)
