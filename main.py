from setup import *
from self_reflection import reflection
from planner import planner
from coder import coder
from test_case_gen import test_case_generator
from tester import tester
from debugger import debugger

from langgraph.checkpoint.memory import MemorySaver
memory=MemorySaver()

class AgentState(TypedDict):
    question: str
    self_reflection: str
    test_cases:list
    plan: str
    coder_response: str
    error: str
    debugger_response: str
    iterations: int

debug_con=1
def debug(content):
    print('-'*150, content, '-'*150, sep='\n')

def reflecting_agent(state:AgentState):
    question=state["question"]
    res=reflection(question)
    if(debug_con==1):
        print("REFLECTION AGENT")
        debug(res)
    return {"self_reflection": res}

def test_generator_agent(state:AgentState):
    question=state["question"]
    tc=test_case_generator(question)
    if(debug_con==1):
        print("TC AGENT")   
        debug(tc)
    return {"test_cases": tc}
    
def planner_agent(state:AgentState):
    question=state["question"]
    reflection=state["self_reflection"]
    error=state["error"]
    code=state["coder_response"]
    db_res=state["debugger_response"]
    plan=planner(question, reflection, code, error, db_res)
    if(debug_con==1):
        print("PLANNER AGENT")
        debug(plan)
    return {"plan": plan}


def plan_debug_agent(state:AgentState):
    question=state["question"]
    reflection=state["self_reflection"]
    error=state["error"]
    code=state["coder_response"]
    db_res=state["debugger_response"]
    plan=planner(question, reflection, code, error, db_res)
    if(debug_con==1):
        print("PLANNER AGENT")
        debug(plan)
    return {"plan": plan}


def wait(state:AgentState):
    question=state["question"]
    return {"question": question}

def coder_agent(state:AgentState):
    question=state["question"]
    plan=state["plan"]
    res=coder(question, plan)
    if(debug_con==1):
        print("CODER AGENT")
        debug(res)
    return {"coder_response": res}


def tester_agent(state: AgentState):
    test_cases=state["test_cases"]
    code=state["coder_response"]
    question=state["question"]
    error=tester(question, code, test_cases)
    if(debug_con==1):
        print("TESTER AGENT")
        debug(error)
    return {"error": error, "iterations": state["iterations"]+1}

def debugger_agent(state:AgentState):
    error=state["error"]
    code=state["coder_response"]
    question=state["question"]
    response=debugger(question, code,error)
    if(debug_con==1):
        print("DEBUGGER AGENT")
        debug(response)
    return {"debugger_response": response}

def should_iterate(state:AgentState):
    if(state["error"]!="-1" and state["iterations"]<4):
        return True
    else:
        return False


workflow= StateGraph(AgentState)
workflow.add_node("self_reflection_agent", reflecting_agent)
workflow.add_node("test_generator_agent", test_generator_agent)
workflow.add_node("coder_agent", coder_agent)
workflow.add_node("planner_agent", planner_agent)
workflow.add_node("plan_debug_agent", plan_debug_agent)
workflow.add_node("tester_agent", tester_agent)
workflow.add_node("debugger_agent", debugger_agent)

workflow.add_edge("self_reflection_agent", "test_generator_agent")
workflow.add_edge("test_generator_agent","planner_agent")
workflow.add_edge("planner_agent", "coder_agent")
workflow.add_edge("coder_agent", "tester_agent")
workflow.add_edge("debugger_agent", "plan_debug_agent")
workflow.add_edge("plan_debug_agent", "coder_agent")
workflow.add_conditional_edges(
    "tester_agent",
    should_iterate,
    {True: "debugger_agent", False: END}
)
 
#workflow.add_edge("tester_agent", END)
workflow.set_entry_point("self_reflection_agent")

workflow=workflow.compile(checkpointer=memory)


def solve(question):
    thread={"configurable":{"thread_id":"1"}}

    initial_state={"question":question, "error":"-1", "iterations":0 ,"coder_response":"", "debugger_response":""}


    #for event in workflow.stream(initial_state, thread):
    #   print(event)
     #  print('-'*80)
    res=workflow.invoke(initial_state, thread)
    return res["coder_response"]

