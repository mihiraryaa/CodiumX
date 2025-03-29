from setup import *
from prompts import *


def debugger(question, code, error):
    '''returns why the code is failing'''
    sys=SystemMessage(content=debugger_prompt)
    user=HumanMessage(content=f"# Question:\n{question}\n# Code:\n{code}\n# error:\n{error}")
    prompt=[sys, user]
    res=model_gpt.invoke(prompt)

    return res.content