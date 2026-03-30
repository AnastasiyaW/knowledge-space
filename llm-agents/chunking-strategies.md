---
title: Chunking Strategies
category: llm-agents/retrieval
tags: [chunking, text-splitting, document-processing, chunk-size, chunk-overlap, data-preparation]
---

# Chunking Strategies

## Key Facts

- Chunking splits documents into smaller pieces for [[embeddings]] and [[vector-databases]] in [[rag-pipeline]]
- Chunk quality directly determines retrieval quality - garbage chunks = garbage retrieval
- Key parameters: **chunk_size** (characters/tokens per chunk) and **chunk_overlap** (shared content between adjacent chunks)
- Recommended starting point: 500-1000 characters with 10-20% overlap
- Too small chunks lose context. Too large chunks dilute the embedding with noise
- Document parsing is the hardest part: PDFs with tables, images, multi-column layouts need specialized tools
- Tools: `unstructured` (general), `PyMuPDF` (PDFs), `LlamaParse` (complex documents), Vision models (scanned/image-heavy)

## Patterns

```python
# LangChain recursive text splitter (most common)
from langchain.text_splitter import RecursiveCharacterTextSplitter

splitter = RecursiveCharacterTextSplitter(
    chunk_size=1000,
    chunk_overlap=200,
    separators=["\n\n", "\n", ". ", " ", ""],  # try each in order
    length_function=len
)
chunks = splitter.split_text(document_text)
```

```python
# Token-based splitting (more accurate for LLMs)
from langchain.text_splitter import TokenTextSplitter

splitter = TokenTextSplitter(
    encoding_name="cl100k_base",  # GPT-4 tokenizer
    chunk_size=500,    # in tokens, not characters
    chunk_overlap=50
)
```

```python
# Semantic chunking (split at meaning boundaries)
from langchain_experimental.text_splitter import SemanticChunker
from langchain_openai import OpenAIEmbeddings

chunker = SemanticChunker(
    OpenAIEmbeddings(),
    breakpoint_threshold_type="percentile",
    breakpoint_threshold_amount=95
)
chunks = chunker.split_text(document_text)
```

```python
# Document parsing with unstructured
from unstructured.partition.pdf import partition_pdf

elements = partition_pdf(
    filename="document.pdf",
    strategy="hi_res",          # OCR + layout detection
    extract_images_in_pdf=True,
    infer_table_structure=True
)

# Elements include: Title, NarrativeText, Table, Image, ListItem
for element in elements:
    print(f"{element.category}: {element.text[:100]}")
```

## Gotchas

- **Chunk size is task-dependent**: Q&A needs smaller chunks (focused answers), summarization needs larger (broad context)
- **Overlap prevents boundary loss**: without overlap, information at chunk boundaries gets split and lost
- **PDF parsing is hard**: tables, multi-column layouts, headers/footers all confuse simple parsers
- **Metadata preservation**: always attach source filename, page number, section title to chunks for citation
- **Pre-processing matters**: remove navigation text, headers, footers, boilerplate before chunking
- **Testing chunk quality**: manually inspect 20-30 chunks to verify they contain coherent, complete thoughts
- **Re-chunking is expensive**: changing strategy requires re-embedding everything. Get it right early

## See Also

- [[rag-pipeline]] - the pipeline that consumes chunks
- [[embeddings]] - vectors generated from chunks
- [[vector-databases]] - where chunk embeddings are stored
- [[structured-output]] - extracting structured data from document chunks
- https://docs.llamaindex.ai/en/stable/module_guides/loading/node_parsers/ - LlamaIndex node parsers
- https://docs.unstructured.io/ - Unstructured library for document parsing
