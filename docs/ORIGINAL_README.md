# Helpdesk RAG Assistant

A local retrieval-augmented support assistant that searches verified organizational documentation before answering IT-support questions.

## Features
- PDF, Markdown and TXT ingestion
- chunked indexing
- TF-IDF retrieval by default
- source-linked evidence
- confidence thresholding
- no external API required

## Quick start
```bash
pip install -r requirements.txt
python src/helpdesk_rag.py index sample_docs --index-dir outputs/index
python src/helpdesk_rag.py ask outputs/index "How do I reset my VPN profile?"
```

For production use, index only current, approved documentation and define a document ownership/update process.
