from dotenv import load_dotenv
from langchain.agents import create_agent
from langchain.tools import tool
from langchain_google_genai import ChatGoogleGenerativeAI

load_dotenv()

model = ChatGoogleGenerativeAI(model="gemini-3.5-flash-lite")


@tool
def divide(a: int, b: int) -> int:
    "take 2 input ints. return the division of the given 2 inputs"
    return a // b


@tool
def multiply(a: int, b: int) -> int:
    "take 2 input ints. return the multiple of the given 2 inputs"
    return a * b


@tool
def add(a: int, b: int) -> int:
    "take 2 input ints. return the sum of the given 2 inputs"
    return a + b


@tool
def subtract(a: int, b: int) -> int:
    "take 2 input ints. return the difference of the given 2 inputs"
    return b - a


agent = create_agent(
    model=model,
    tools=[divide, multiply, add, subtract],
    system_prompt=(
        "You are a mathematical assistant."
        "Use the available tools for calculations."
        "For multi-step calculations, execute each required "
        "operation using the appropriate tool."
        "Explain the result clearly."
    ),
)

result = agent.invoke(
    {"messages": [{"role": "user", "content": "what is (14 + 9) * 3?"}]}
)

print(result["messages"][-1].content[0]["text"])

# internal
for message in result["messages"]:
    print("\n", type(message).__name__)
    print(message.content)

    if getattr(message, "tool_calls", None):
        print("Tool calls:", message.tool_calls)
