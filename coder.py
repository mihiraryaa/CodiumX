from setup import *
from prompts import *

def coder(question, plan):

    class coder_scheme(BaseModel):
        code:str=Field(description="Python code that can be executed directly")
    model=model_gpt.with_structured_output(coder_scheme)
    sys=SystemMessage(content=coder_prompt)
    user=HumanMessage(content=f"## Question:\n{question} ## Plan\n{plan}")    
    prompt=[sys, user]
    code=model_gpt.invoke(prompt)
    code=model.invoke(code.content)
    
    return code.code

