from dotenv import load_dotenv
from langchain.tools import tool
from langchain_core.messages import ToolMessage
from langchain_google_genai import ChatGoogleGenerativeAI

load_dotenv()

model = ChatGoogleGenerativeAI(model="gemini-3.5-flash-lite")


@tool
def multiply(a: int, b: int) -> int:
    """multiply 2 numbers and return their product"""
    return a * b


@tool
def divide(a: int, b: int) -> int:
    """divide 2 numbers and return their product"""
    return a // b


# print(multiply.name)  # multiply
# print(multiply.description)  # Multiply 2 numbers and return their product
# print(multiply.args)  # {'a': {'title': 'A', 'type': 'integer'}, 'b': {'title': 'B', 'type': 'integer'}}

# result = multiply.invoke({"a": 10, "b": 50})
# print(result) #500


model_w_tools = model.bind_tools([multiply, divide])
# bind_tools tells the model: "You have access to these functions. Call them if you need external info or math, but if you have the answer, just respond normally."
# .bind_tools() accepts LangChain tools, Python callables and supported schemas

messages = [("human", "what's 110/12?")]

response = model_w_tools.invoke(messages)
print(
    "response.tool_calls: ", response.tool_calls
)  # returns [{'name': 'multiply', 'args': {'b': 12, 'a': 11}, 'id': 'call_4157864671555035892', 'type': 'tool_call'}]. find the best tool and produces it's args.


tool_call = response.tool_calls[0]
tool = tool_call["name"]

# gemini only figures out which tool to use and which args to use from the prompt. we have to execute our function manually.

# tool calling
match tool:
    case "multiply":
        tool_result = multiply.invoke(tool_call["args"])
    case "divide":
        tool_result = divide.invoke(tool_call["args"])

print("tool result: ", tool_result)

tool_message = ToolMessage(content=str(tool_result), tool_call_id=tool_call["id"])

messages.append(response)
messages.append(tool_message)

print("\n", messages)


final_response = model_w_tools.invoke(messages)
print("\nfinal response:")
print(final_response.content)
