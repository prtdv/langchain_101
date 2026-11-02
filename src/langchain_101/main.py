from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI

load_dotenv()

model = ChatGoogleGenerativeAI(model="gemini-3.5-flash-lite", temperature=0)

response = model.invoke(
    "hello gemini, what is the positives of taking creatine monohydrate while following a gym routine."
)
print(type(response))
print(response.content[0]["text"])
print(response.usage_metadata)
