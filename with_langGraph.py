from typing_extensions import TypedDict
from langgraph.graph import StateGraph, START, END
from langchain.chat_models import init_chat_model
from ddgs import DDGS
from dotenv import load_dotenv

load_dotenv()


class State(TypedDict):
    question: str
    search_results: list
    results_good: bool
    answer: str
    
    
#defining LLM
llm = init_chat_model(
    model="openai/gpt-oss-20b",
    model_provider="groq"
)


#defining search function
def search_web_node(state:State):
    results = DDGS().text(
        state["question"]
    )
    return {"search_results":results}


def check_results_node(state:State):

    prompt = f"""
    Question:
    {state["question"]}

    Search results:
    {state["search_results"]}

    Do these search results contain enough relevant
    information to answer the question?

    Answer only YES or NO.
    """

    response = llm.invoke(prompt)
    print(response.content)

    return {
        "results_good": response.content.strip().upper() == "YES"
    }


def generate_answer(state:State):

    question = state["question"]
    search_results = state["search_results"]
    prompt = f"""
    Answer the question using the search results.

    QUESTION:
    {question}

    SEARCH RESULTS:
    {search_results}

    Give a clear and concise answer.
    """

    response = llm.invoke(prompt)

    return {
        "answer": response.content
    }


#decide where to go
def route(state:State):
    if state["results_good"]:
        return "generate_answer"
    else:
        return "search_web"

#Building Graph

graph_builder = StateGraph(State)

#Registering nodes
graph_builder.add_node("search_web",search_web_node)
graph_builder.add_node("check_results",check_results_node)
graph_builder.add_node("generate_answer",generate_answer)

#Defining Workflow
graph_builder.add_edge(START,"search_web")
graph_builder.add_edge("search_web","check_results")

#Checking conditional edge instead of if/else
graph_builder.add_conditional_edges(
    "check_results",
    route,
    {
        "generate_answer": "generate_answer",
        "search_web": "search_web"
    }
    
)

graph_builder.add_edge("generate_answer",END)


#compiling graph
graph = graph_builder.compile()

#Run
result = graph.invoke({
    "question":"What is the price of Jaguar?",
    "search_results":[],
    "answer":"",
    "results_good":False
})

print(result["answer"])