from dotenv import load_dotenv
from langchain_core.messages import AIMessage, HumanMessage, SystemMessage
from langchain_google_genai import ChatGoogleGenerativeAI

load_dotenv()

model = ChatGoogleGenerativeAI(model="gemini-3.5-flash-lite")

input_chat = "Hi"

messages = [
    SystemMessage(
        content="you know nothing about python but you are a friend. stick to the rp."
    ),
    HumanMessage(content=input_chat),
]

while input_chat != "/end":
    response = model.invoke(messages)
    print("Gemini: ", response.content[0]["text"], "\n")
    messages.append(response)
    input_chat = input("You: ")
    messages.append(HumanMessage(content=input_chat))
