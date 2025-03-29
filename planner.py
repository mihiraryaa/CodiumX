from setup import *
from prompts import *


def planner(question, self_reflection,code,error,db_res):

    if(error=='-1'):
        sys=SystemMessage(content=planner_prompt)
        user=HumanMessage(content=f"# Question:\n{question}\n# Self-reflection\n{self_reflection}")
        prompt=[sys, user]
        plan=model_gpt.invoke(prompt)
        plan=plan.content
    else:
        sys=SystemMessage(content=planner_debug_prompt)
        user=HumanMessage(content=f"# Question\n{question}\n# Question-reflection\n{self_reflection}\n# Code\n{code}\n# Debugger agent's response:\n{db_res}")
        prompt=[sys, user]
        plan=model_gpt.invoke(prompt)
        plan=plan.content

    return plan