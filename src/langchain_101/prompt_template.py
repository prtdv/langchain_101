from dotenv import load_dotenv
from langchain_core.prompts import ChatPromptTemplate, PromptTemplate
from langchain_google_genai import ChatGoogleGenerativeAI

load_dotenv()

model = ChatGoogleGenerativeAI(model="gemini-3.5-flash-lite")

prompt = PromptTemplate.from_template(
    "Explain {topic} to {audience}. keep the explanation {length}."
)

formatted_prompt = prompt.format(
    topic="neural networks", audience="college students", length="short"
)

# print(formatted_prompt)
# response = model.invoke(formatted_prompt)
# print(response.content[0]["text"])

promptWithRoles = ChatPromptTemplate.from_messages(
    [
        ("system", "you are a {role}. Explain concepts in a {tone} manner."),
        ("human", "explain {topic} to me."),
    ]
)

prompt_values = promptWithRoles.invoke(
    {"role": "python instructor", "tone": "aggressive", "topic": "recursion"}
)  # returns messages

print(prompt_values)

response = model.invoke(prompt_values)
print(response.content[0]["text"])
