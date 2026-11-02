from dotenv import load_dotenv
from langchain_core.messages import AIMessage, HumanMessage, SystemMessage
from langchain_google_genai import ChatGoogleGenerativeAI

load_dotenv()

model = ChatGoogleGenerativeAI(model="gemini-3.5-flash-lite")

messages = [
    SystemMessage(content="You are someone who doesnt know python at all. be honest"),
    HumanMessage(content="Explain decorators in python. My name is Pratyush"),
]

# first interaction
response = model.invoke(messages)
print(response.content)

# save the AI's response to conversation history.
messages.append(response)

# second interaction
messages.append(HumanMessage(content="What is my name?"))

response = model.invoke(messages)
print(response.content)
