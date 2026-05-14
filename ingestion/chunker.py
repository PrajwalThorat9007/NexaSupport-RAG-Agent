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


import os
import pandas as pd
from langchain.text_splitter import RecursiveCharacterTextSplitter


def chunk_text(text: str, source: str, chunk_size: int = 500, overlap: int = 50) -> list[dict]:
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size,
        chunk_overlap=overlap,
        separators=["\n\n", "\n", ".", " "]
    )
    chunks = splitter.split_text(text)
    return [
        {
            "text": chunk,
            "source": source,
            "chunk_index": i
        }
        for i, chunk in enumerate(chunks)
    ]


def load_csv(filepath: str) -> list[dict]:
    df = pd.read_csv(filepath)
    all_chunks = []
    for _, row in df.iterrows():
        combined = (
            f"Issue: {row.get('issue_description', '')}\n"
            f"Product Area: {row.get('product_area', '')}\n"
            f"Tags: {row.get('tags', '')}\n"
            f"Resolution: {row.get('resolution', '')}"
        )
        chunks = chunk_text(
            text=combined,
            source=f"tickets:{row.get('ticket_id', 'unknown')}"
        )
        all_chunks.extend(chunks)
    return all_chunks


def load_markdown(filepath: str, source_name: str) -> list[dict]:
    with open(filepath, "r", encoding="utf-8") as f:
        content = f.read()

    # Split by ## headings first, then chunk each section
    sections = content.split("\n## ")
    all_chunks = []
    for section in sections:
        if not section.strip():
            continue
        # Restore heading marker for all but first
        section_text = section if section.startswith("#") else "## " + section
        heading = section_text.split("\n")[0].replace("#", "").strip()
        chunks = chunk_text(
            text=section_text,
            source=f"{source_name}:{heading}"
        )
        all_chunks.extend(chunks)
    return all_chunks


def load_json_profiles(filepath: str) -> list[dict]:
    import json
    with open(filepath, "r", encoding="utf-8") as f:
        profiles = json.load(f)

    all_chunks = []
    for profile in profiles:
        text = (
            f"Customer: {profile.get('company_name', '')} "
            f"({profile.get('customer_tier', '')})\n"
            f"Health Status: {profile.get('health_status', '')}\n"
            f"NPS Score: {profile.get('nps_score', '')}\n"
            f"Usage Drop: {profile.get('usage_drop_pct', '')}%\n"
            f"Days to Renewal: {profile.get('days_to_renewal', '')}\n"
            f"Open Tickets: {profile.get('open_tickets', '')}\n"
            f"Billing Events: {', '.join(profile.get('billing_events', []))}\n"
            f"Notes: {profile.get('notes', '')}"
        )
        chunks = chunk_text(
            text=text,
            source=f"customer_health:{profile.get('customer_id', 'unknown')}"
        )
        all_chunks.extend(chunks)
    return all_chunks
