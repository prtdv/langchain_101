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


# - load() loads the documents and returns a list.
# - lazy_load() yields documents one at a time, which is useful for larger datasets.
# - ExportType.MARKDOWN gives us document-level Markdown output, which is convenient because we'll handle chunking ourselves in the next lesson.
