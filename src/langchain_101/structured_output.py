from typing import Literal

from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from pydantic import BaseModel, Field

load_dotenv()


class ReviewAnalysis(BaseModel):
    sentiment: Literal["postive", "negative", "neutral"]
    rating: int = Field(ge=1, le=5, description="Customer rating between 1 and 5.")
    key_points: list[str] = Field(
        description="Important points extracted from the review."
    )
    summary: str = Field(description="A short summary of the review.")


model = ChatGoogleGenerativeAI(model="gemini-3.5-flash-lite")
structured_model = model.with_structured_output(
    ReviewAnalysis
)  # Whenever this model generates a response, structure it according to the ReviewAnalysis schema.

review = """
The delivery was incredibly fast and the product quality
is excellent. Customer support was also very helpful.
Definitely worth buying!
"""

response = structured_model.invoke(f"Analyze this customer review: {review}")
print(response)

# it's a pydantic class object, abuse it.
print(response.sentiment)
print(response.rating)
print(response.key_points)
print(response.summary)

# convert pydantic object to dict
data = response.model_dump()
print(data)
print(type(data))

# convert pydantic object to json
json_output = response.model_dump_json(indent=2)
print(json_output)
