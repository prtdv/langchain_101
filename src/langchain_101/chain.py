from dotenv import load_dotenv
from langchain_core.output_parsers import StrOutputParser  # AIMessage to str
from langchain_core.prompts import ChatPromptTemplate
from langchain_google_genai import ChatGoogleGenerativeAI

load_dotenv()

model = ChatGoogleGenerativeAI(model="gemini-3.5-flash-lite")

prompt = ChatPromptTemplate.from_messages(
    [
        ("system", "You are an experienced Python instructor."),
        ("human", "Explain {topic} in simple terms with an example"),
    ]
)

parser = StrOutputParser()


chain = prompt | model | parser

result = chain.invoke({"topic": "recursion"})

print(result)
print(type(result))

# results = chain.batch(
#     [{"topic": "recursion"}, {"topic": "decorators"}, {"topic": "valorant calm aim"}]
# )
#
# for i in results:
#     print(i)
