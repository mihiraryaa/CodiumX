from setup import * 
from prompts import *

class test_case(BaseModel):
        input: str=Field(description="The input for the test case")
        output: str=Field(description="The output for the test case")

def tester(question, code, test_cases):
    '''takes code and test cases, returns the error '''
    #test case parser
    class scheme(BaseModel):
        code:str=Field(description="Assert conditions in form of python code ready to be executed")
    model=model_gpt.with_structured_output(scheme)
    sys=SystemMessage(content=test_parser_prompt)
    user=HumanMessage(content=f"#Question:\n{question}\n#Test cases:\n{test_cases}")
    prompt=[sys,user]
    tc_code=model.invoke(prompt)
    tc_code=tc_code.code
    tc_list=tc_code.split('\n')

    final_code=code+'\nerror="-1"\n'
    final_code+="try:\n"
    for line in tc_list:
        final_code+=f"    {line}\n"
    
    code_chunk='''
except AssertionError as e:
    error = str(e)  # Directly extract the string message
    error=f"Test case failed -> {error}"
except Exception as e:
    error=f"Runtime error: {type(e).__name__} - {str(e)}"

'''

    final_code+=code_chunk
    #print(final_code)
    exec_context={}
    exec(final_code, exec_context)
    error=exec_context.get("error")
    return error

