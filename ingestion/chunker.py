# chunker.py
# Responsibility: Split raw text into overlapping chunks for embedding.
# Owner: Engineer A / Engineer D (shared util)
#
# TODO: Implement chunk_text(text: str, chunk_size: int, overlap: int) -> list[dict]
#   - Use LangChain RecursiveCharacterTextSplitter
#   - Each chunk dict: { "text": str, "source": str, "chunk_index": int }
#   - Default chunk_size=500, overlap=50
#
# TODO: Implement load_csv(filepath: str) -> list[dict]
#   - Load tickets_resolved.csv with pandas
#   - Combine issue_description + resolution into one text block per row
#   - Tag each chunk with source="tickets", product_area, tags
#
# TODO: Implement load_markdown(filepath: str, source_name: str) -> list[dict]
#   - Read .md file, split by ## headings first, then chunk each section
#   - Tag each chunk with source=source_name, section heading


def chunk_text(text: str, chunk_size: int = 500, overlap: int = 50) -> list:
    pass


def load_csv(filepath: str) -> list:
    pass


def load_markdown(filepath: str, source_name: str) -> list:
    pass
