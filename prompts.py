

self_ref_prompt='''
Given the python programming question you have to reflect on the problem statement and the public test cases.
## Instructions
->Reflect on the problem statement, explaining each and every phrase
->Reason on the public test cases, understanding why the input gave that specific output
## Return answer in the specified format.
'''

coder_prompt='''
Given the python programming question and the plan to solve the question
## Instructions
Go through the plan provided to you, and convert it into code.
Take care of the input and output constraints.
'''



ref_review_prompt='''
You will be given a coding question and an assertion/assumption.
You have to check whether the assertion/assumption is right or wrong according to what's given in the question.
If it's wrong, correct it.
Be very careful in analyzing, even a single word makes a lot of difference.
'''

planner_prompt='''
You will be a coding question and the self-reflection on the problem statement.
Your job is to create a step by step plan to solve the question in natural language.
Make sure you follow the insights in the self-reflection.
Only return the plan in bullet points and nothing else.
'''

planner_debug_prompt='''
Your task is to create a plan to correct the code based on the response of the debugger agent.
You will given the question,reflection on the question, code and the response of the debugger agent.
Identify what changes will correct the code and create a step by step plan to write the correct code.
Make sure to go through insights given by the debugger agent.
Return the revised plan in bullet points.
'''

test_case_prompt='''
You wil be given a coding question.
Your job is to create the test cases that the program might fail on.
Make sure that the test case follows the question logic and constraints.
Return only 1 test case(both input and output).
'''

test_rev_prompt='''
You will be givena coding question and test case for that question.
Your job is to use chain of thought reasoning to determine if that test case correct.
Return the correct case if it's wrong.
'''

test_parser_prompt='''

## Task Description
You will be given a coding question and a list of test cases. Your task is to convert the test cases into assert conditions for the given coding question. 

Your response should follow this format:
```python
assert function_name(input) == expected_output, f"Input: {input}, Expected: {expected_output}, Got: {function_name(input)}"
```
# Here are some examples:
## Example 1->
### Question
def add(a,b):
    ' takes two integers and returns their sum.'

### Test Cases
[
    {"input": "1, 2", "output": "3"},
    {"input": "5, 7", "output": "12"},
    {"input": "-3, 3", "output": "0"}
]

### Output
assert add(1, 2) == 3, f"Input: (1, 2), Expected: 3, Got: {add(1, 2)}"
assert add(5, 7) == 12, f"Input: (5, 7), Expected: 12, Got: {add(5, 7)}"
assert add(-3, 3) == 0, f"Input: (-3, 3), Expected: 0, Got: {add(-3, 3)}"


## Example 2 
### Question
def reverse_string(s: str) -> str:
    """
    Given a string s, return a new string that is the reverse of s.
    
    Example:
    reverse_string("hello") -> "olleh"
    """
### Test Cases
[
    {"input": "\"hello\"", "output": "\"olleh\""},
    {"input": "\"world\"", "output": "\"dlrow\""},
    {"input": "\"Python\"", "output": "\"nohtyP\""}
]

### Output
assert reverse_string("hello") == "olleh", f"Input: 'hello', Expected: 'olleh', Got: {reverse_string('hello')}"
assert reverse_string("world") == "dlrow", f"Input: 'world', Expected: 'dlrow', Got: {reverse_string('world')}"
assert reverse_string("Python") == "nohtyP", f"Input: 'Python', Expected: 'nohtyP', Got: {reverse_string('Python')}"


'''

debugger_prompt='''
Your job is to debug the code given the test case it is failing on or the error the code is giving.
You will be given the code, failed test case/error message and the question itself.
Analyze the code and identify the root cause and suggest a fix.
Use chain of thought reasoning to carry out your task.
Only identify the root cause and suggest a fix and nothing else.
'''


