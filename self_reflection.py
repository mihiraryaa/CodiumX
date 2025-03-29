from setup import *
from prompts import *

def reflection(question):

    class self_ref_scheme(BaseModel):
        question:List[str]=Field(description="Reflection on the question")
        test_cases:List[str]=Field(description="Reasoning of the public test cases")

    model=model_gpt.with_structured_output(self_ref_scheme)
    sys=SystemMessage(content=self_ref_prompt)
    user=HumanMessage(content=f"Coding question: \n{question}")
    prompt=[sys,user]
    self_ref=model.invoke(prompt)
     
    class review_scheme(BaseModel):
        rev:str=Field(description="revised version of the assumption/assertion")
    
    self_reflection=[]
    model=model_gpt.with_structured_output(review_scheme)
    for a in self_ref.question:
        sys=SystemMessage(content=ref_review_prompt)
        user=HumanMessage(content=f"# Coding question: \n{question}  # assumption\n{a}")
        prompt=[sys,user]
        self_ref_rev=model.invoke(prompt)
        self_reflection.append(self_ref_rev.rev)
    self_reflection+=self_ref.test_cases
    self_reflection='\n->'.join(self_reflection)

    return self_reflection