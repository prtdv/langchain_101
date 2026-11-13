from dotenv import load_dotenv
from langchain.agents import create_agent
from langchain_google_genai import ChatGoogleGenerativeAI
from langgraph.checkpoint.sqlite import SqliteSaver

load_dotenv()

model = ChatGoogleGenerativeAI(model="gemini-3.5-flash-lite")

config = {"configurable": {"thread_id": "pratyush-session-001"}}

# SQLite database stores conversation checkpoints on disk
with SqliteSaver.from_conn_string("checkpoints.sqlite") as checkpointer:
    agent = create_agent(
        model=model,
        tools=[],
        system_prompt="You are a helpful conversational assistant.",
        checkpointer=checkpointer,
    )

    print("Conversational assistant ready.")
    print("Type /exit to quit.\n")

    while True:
        user_input = input("You: ")

        if user_input == "/exit":
            break

        if not user_input:
            continue

        result = agent.invoke(
            {"messages": [{"role": "user", "content": user_input}]}, config
        )

        print("\nAssistant:", result["messages"][-1].content[0]["text"])
        print()
