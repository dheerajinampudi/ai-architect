from typing import Optional
from langchain.embeddings import OpenAIEmbeddings
from langchain import LLMChain, PromptTemplate
from langchain.vectorstores import FAISS
from langchain.docstore import InMemoryDocstore
from src.baby_agi import BabyAGI
from langchain.agents import ZeroShotAgent, Tool
from langchain import OpenAI, LLMChain
from langchain.utilities import GoogleSearchAPIWrapper
from constants import (
    EMBEDDING_MODEL_NAME,
    EMBEDDING_SIZE, 
    TODO_CHAIN_MODEL_NAME,
    BABY_AGI_MODEL_NAME
)


def run_agent(
        user_input, 
        num_iterations,
        baby_agi_model=BABY_AGI_MODEL_NAME,
        todo_chaining_model=TODO_CHAIN_MODEL_NAME,
        embedding_model=EMBEDDING_MODEL_NAME
    ):

    # Define your embedding model
    embeddings_model = OpenAIEmbeddings(model=embedding_model)
    # Initialize the vectorstore as empty
    import faiss

    embedding_size = EMBEDDING_SIZE
    index = faiss.IndexFlatL2(embedding_size)
    vectorstore = FAISS(embeddings_model.embed_query, index, InMemoryDocstore({}), {})

    todo_prompt = PromptTemplate.from_template(
        "You are a planner who is an expert at coming up with a todo list for a given objective. Come up with a todo list for this objective: {objective}"
    )
    todo_chain = LLMChain(
        llm=OpenAI(temperature=0, model_name=todo_chaining_model), 
        prompt=todo_prompt
    )
    search = GoogleSearchAPIWrapper()#SerpAPIWrapper() replaces SERPAPI with google for SERP use https://serper.dev/
    tools = [
        Tool(
            name="Search",
            func=search.run,
            description="useful for when you need to answer questions about current events",
        ),
        Tool(
            name="TODO",
            func=todo_chain.run,
            description="useful for when you need to come up with todo lists. Input: an objective to create a todo list for. Output: a todo list for that objective. Please be very clear what the objective is!",
        ),
    ]

    prefix = """You are an AI who performs one task based on the following objective: {objective}. Take into account these previously completed tasks: {context}."""
    suffix = """Question: {task}
    {agent_scratchpad}"""

    prompt = ZeroShotAgent.create_prompt(
        tools,
        prefix=prefix,
        suffix=suffix,
        input_variables=["objective", "task", "context", "agent_scratchpad"],
    )

    OBJECTIVE = user_input
    llm = OpenAI(temperature=0, model_name=baby_agi_model)
    # Logging of LLMChains
    verbose = False
    # If None, will keep on going forever. Customize the number of loops you want it to go through.
    max_iterations: Optional[int] = num_iterations
    baby_agi = BabyAGI.from_llm(
        prompt=prompt,
        tools=tools,
        llm=llm, 
        vectorstore=vectorstore, 
        verbose=verbose, 
        max_iterations=max_iterations
    )
    if (user_input):
        baby_agi({"objective": OBJECTIVE})
