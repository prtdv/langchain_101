from importlib.metadata import metadata

from langchain_core.documents import Document

documents = [
    Document(
        page_content="""
                Employees are entitled to 20 days of annual leave.

                Employees may carry forward a maximum of
                10 unused days to the next calendar year.

                Sick leave is limited to 12 days annually.
                """,
        metadata={"source": "employee_handbook.md"},
    )
]

from langchain_text_splitters import RecursiveCharacterTextSplitter

splitter = RecursiveCharacterTextSplitter(
    chunk_size=100, chunk_overlap=20, add_start_index=True
)

chunks = splitter.split_documents(documents)

for i, chunk in enumerate(chunks):
    print(f"\nChunk {i + 1}:")
    print(chunk.page_content)
    print(chunk.metadata)
