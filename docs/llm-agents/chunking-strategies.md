---
title: Chunking Strategies
category: techniques
tags: [llm-agents, chunking, text-splitting, document-processing, rag, data-preparation]
---

# Chunking Strategies

Chunking is the process of splitting documents into smaller pieces for embedding and retrieval in RAG systems. Chunk quality directly determines retrieval quality, which determines answer quality.

## Key Facts
- Chunk size is the most impactful RAG parameter - too small loses context, too large dilutes relevance
- Chunk overlap prevents cutting important context at boundaries
- Semantic chunking (split on natural boundaries) preserves meaning better than fixed-size splits
- Documents should be cleaned before chunking: remove headers/footers, page numbers, watermarks
- Tables should be extracted as structured data, not as text chunks

## Chunk Size Guidelines

| Chunk Size | Use Case | Tradeoff |
|------------|----------|----------|
| 256-512 chars | Precise Q&A, specific facts | More chunks, more retrieval noise |
| 512-1000 chars | General purpose, balanced | Good default for most use cases |
| 1000-2000 chars | Summarization, broader context | Fewer chunks, may dilute relevance |
| Full document | Single-document Q&A | Only with large context windows |

## Patterns

### Recursive Character Text Splitter

Most common approach. Recursively splits by separators until chunks are within size limit:

```python
from langchain.text_splitter import RecursiveCharacterTextSplitter

splitter = RecursiveCharacterTextSplitter(
    chunk_size=1000,
    chunk_overlap=200,
    separators=["\n\n", "\n", ".", " ", ""]
)
chunks = splitter.split_documents(documents)
```

Tries `\n\n` first (paragraph breaks), falls back to `\n`, then `.`, then space, then character-level as last resort.

### Token-Based Splitting

Split by token count rather than character count. More accurate for LLM context management since LLMs have token limits:

```python
from langchain.text_splitter import TokenTextSplitter

splitter = TokenTextSplitter(
    chunk_size=500,    # tokens, not chars
    chunk_overlap=50
)
```

### Semantic Chunking

Split on natural boundaries (paragraphs, sections, headers) rather than arbitrary counts. Better preserves meaning units.

### Hierarchical Chunking

Parent chunks (full sections) + child chunks (paragraphs). Retrieve child for precision, return parent for context. Gives both precise matching and sufficient surrounding context.

## Chunk Overlap

- **Purpose**: prevent cutting important context at chunk boundaries
- **Typical**: 10-20% of chunk size (e.g., 100-200 chars for 1000-char chunks)
- **Too much**: duplicate information, increased storage and cost
- **Too little**: lost context at boundaries

## Document Loaders

| Loader | Format | Notes |
|--------|--------|-------|
| **PyPDF / PyPDF2** | PDF | Simple. Struggles with tables and complex layouts |
| **LlamaParse** | PDF, DOCX | Best PDF extraction - handles tables, images, complex layouts. Cloud service |
| **Unstructured** | PDF, DOCX, HTML, images | Multi-format, extracts structured elements |
| **BeautifulSoup** | HTML | Web scraping, HTML parsing |
| **Firecrawl** | Web pages | Crawls websites, converts to clean markdown |
| **Cheerio** | HTML (Node.js) | Web scraping for FlowWise/Node.js |

## Data Preparation Checklist

1. **Clean documents**: remove headers/footers, page numbers, watermarks
2. **Preserve structure**: keep headings, table formatting, list structures
3. **Add metadata**: source file, page number, section title, date
4. **Handle tables separately**: extract as structured data, not text chunks
5. **Test chunk quality**: manually review chunks - do they contain meaningful units?
6. **Verify indexing**: confirm documents were actually indexed in vector store

## Gotchas
- The #1 mistake in FlowWise: not clicking "Upsert" after connecting documents - RAG retrieves nothing
- PDF extraction quality varies wildly - always inspect extracted text before chunking
- Tables in PDFs often turn into garbage text with simple extractors - use LlamaParse or manual extraction
- Chunk size should be tuned per use case - 1000 chars is just a starting point
- Very small chunks (< 200 chars) often lack enough context for meaningful embedding
- Overlapping chunks increase storage costs but significantly reduce boundary-related retrieval failures

## See Also
- [[rag-pipeline]] - How chunks flow through the RAG system
- [[vector-databases]] - Where chunks are stored and searched
- [[embeddings]] - How chunks become searchable vectors
- [[production-patterns]] - Knowledge base patterns that bypass chunking
