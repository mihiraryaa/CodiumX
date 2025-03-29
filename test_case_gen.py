from setup import *
from prompts import *

def test_case_generator(question):

    class test_case(BaseModel):
        input: str=Field(description="The input for the test case")
        output: str=Field(description="The output for the test case")
    
    test_cases=list()
    for i in range(5):
        model=model_gpt.with_structured_output(test_case)
        sys=SystemMessage(content=test_case_prompt)
        user=HumanMessage(content=f"# Question\n{question}\n# List of already generated test cases\n{test_cases}")
        prompt=[sys, user]
        tc=model.invoke(prompt)
        #print(tc.content)
        sys=SystemMessage(content=test_rev_prompt)
        user=HumanMessage(content=f"# Question\n{question}\n# Test case: {tc}")
        prompt=[sys,user]
        tc=model_gpt.invoke(prompt)
        tc=model.invoke(tc.content)
        test_cases.append(tc)
    
    return test_cases

   


