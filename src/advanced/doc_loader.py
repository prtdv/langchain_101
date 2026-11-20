# LangChain loaders convert different data sources into a common Document representation.

# Document(
#     page_content="The actual text...",
#     metadata={"source": "employee_handbook.pdf"}
# )

# uv add langchain-docling

from langchain_docling.loader import DoclingLoader, ExportType

loader = DoclingLoader(
    file_path="src/data/employee_handbook.pdf", export_type=ExportType.MARKDOWN
)

documents = loader.load()

print(f"documents loaded: {len(documents)}")

for doc in documents:
    print(doc.page_content)
    print(doc.metadata)
