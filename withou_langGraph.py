# User Question
#       ↓
#    Web Search
#       ↓
# LLM evaluates results
#       ↓
#  ┌──────────────┐
#  │ Are results  │
#  │ sufficient?  │
#  └──────┬───────┘
#     YES │ NO
#         │
#    ┌────┴─────┐
#    ↓          ↓
# Answer    Search Again
#               ↓
#             Answer

#Without langGraph we manually do everything.

from langchain.chat_models import init_chat_model
from ddgs import DDGS
from dotenv import load_dotenv

load_dotenv()

#defining LLM
llm = init_chat_model(
    model="openai/gpt-oss-20b",
    model_provider="groq"
)


#defining search function
def search_web(query):
    results = DDGS().text(query)
    return results


def check_results(question, results):

    prompt = f"""
    Question:
    {question}

    Search results:
    {results}

    Do these search results contain enough relevant
    information to answer the question?

    Answer only YES or NO.
    """

    response = llm.invoke(prompt)
    print(response.content)

    return response.content.strip().upper() == "YES"


def generate_answer(question, search_results):

    prompt = f"""
    Answer the question using the search results.

    QUESTION:
    {question}

    SEARCH RESULTS:
    {search_results}

    Give a clear and concise answer.
    """

    response = llm.invoke(prompt)

    return response.content


#Workflow starts without langGraph
question = "What is the price of Jaguar?"

#Search web
search_results = search_web(question)


# 2. Check whether we got results
if check_results(question, search_results):

    # 3. Send results to LLM
    answer = generate_answer(
        question,
        search_results
    )

else:
    print("SEARCHING AGIAN")
    # 4. Search again
    new_query = question + " official source"

    search_results = search_web(new_query)

    # 5. Ask LLM again
    answer = generate_answer(
        question,
        search_results
    )

print(answer)