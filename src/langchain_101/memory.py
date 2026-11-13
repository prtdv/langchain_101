from anyio.lowlevel import checkpoint
from dotenv import load_dotenv
from langchain.agents import create_agent
from langchain_google_genai import ChatGoogleGenerativeAI
from langgraph.checkpoint.memory import InMemorySaver  # stores checkpoint in RAM

# uv add langgraph-checkpoint-sqlite for persistent sqlite state storage

load_dotenv()

model = ChatGoogleGenerativeAI(model="gemini-3.5-flash-lite")

checkpointer = InMemorySaver()

agent = create_agent(
    model=model,
    tools=[],
    system_prompt="You are a helpful conversational assistant.",
    checkpointer=checkpointer,  # our agent now has short term memory support
)

# define thread id, this thread id identifies our conversation. Same thread ID = Same conversation state.
config = {"configurable": {"thread_id": "prtdv-session-1"}}

# first invocation.
response = agent.invoke(
    {
        "messages": [
            {
                "role": "user",
                "content": "My name is Pratyush Dev. I am studying langchain.",
            }
        ]
    },
    config,
)
print(response["messages"][-1].content[0]["text"], "\n")

# second invocation
response = agent.invoke(
    {"messages": [{"role": "user", "content": "what's my name?"}]},
    config,
)
print(response["messages"][-1].content[0]["text"], "\n")

response = agent.invoke(
    {"messages": [{"role": "user", "content": "what am I doing here?"}]},
    config,
)
print(response["messages"][-1].content[0]["text"], "\n")


# let's change the config and see
new_config = {"configurable": {"thread_id": "some_new_id"}}

response = agent.invoke(
    {"messages": [{"role": "user", "content": "what's my name? count=1"}]},
    new_config,
)
print(
    response["messages"][-1].content[0]["text"], "\n"
)  # it won't know my name, memory state checkpoints are saved against it's respective thread_id. there here is a new thread


response = agent.invoke(
    {
        "messages": [
            {
                "role": "user",
                "content": "count+=1. what's the count?",
            }
        ]
    },
    new_config,
)
print(response["messages"][-1].content[0]["text"], "\n")


# inspect saved state for config
snapshot = agent.get_state(config)
print(snapshot.values)

messages = snapshot.values["messages"]
for message in messages:
    print(type(message).__name__)
    print(message.content)
    print("-" * 40)
