# Helpdesk RAG Assistant

A local retrieval-augmented support assistant that searches verified organizational documentation before answering IT-support questions.

[Research notes](docs/RESEARCH.md) · [Architecture](docs/ARCHITECTURE.md) · [Execution record](docs/RESULTS.md) · [Project site](docs/index.html)

---

## Research context

Can evidence retrieval reduce unsupported claims in common helpdesk answers?

The repository provides an inspectable implementation of **evidence-backed it support retrieval**. It is an exploratory engineering project; broader effectiveness and practical deployment require further study.

## Implemented capabilities

- PDF, Markdown and TXT ingestion
- chunked indexing
- TF-IDF retrieval by default
- source-linked evidence
- confidence thresholding
- no external API required

## Architecture

```mermaid
flowchart LR
    A["vpn.md"] --> B["helpdesk_rag.py"]
    B --> C["Console / application output"]
```

The diagram is a simplified view of the supplied implementation. Detailed modules and interface assumptions are in [architecture notes](docs/ARCHITECTURE.md).

## Run locally

**Environment:** Python 3.11+ is the documented baseline. Install optional services or hardware drivers when required. Dependencies: pypdf, scikit-learn, numpy.

```bash
python -m venv .venv
source .venv/bin/activate       # Windows: .venv\Scripts\activate
python -m pip install -r requirements.txt
```

Run the following commands from the repository root:

```bash
python src/helpdesk_rag.py index sample_docs --index-dir outputs/index
python src/helpdesk_rag.py ask outputs/index "How do I reset my VPN profile?"
```

**Input:** `sample_docs/vpn.md`

## Results

**Executed locally** with the included input files. This is an implementation check, not an independently validated benchmark.

![Output from the local execution](assets/result.svg)


**Execution evidence:** [Full command transcript](results/execution.txt) · [Inputs and checksums](results/execution.json)

**Saved outputs**

- The command writes its results to standard output. See the transcript.

The values above come from the bundled fixtures. Model scores, simulated costs, and resource-use estimates should not be interpreted as real-world deployment results.

## Source structure

- [`src/helpdesk_rag.py`](src/helpdesk_rag.py)

Documentation is in [`docs/`](docs/). Bundled inputs remain in their original folders. The original project instructions are archived in [`docs/ORIGINAL_README.md`](docs/ORIGINAL_README.md).

## Limits and next research steps

- Results shown here are from local bundled inputs; they are not published research findings or evidence of external deployment.
- Validate domain assumptions and compare against a documented baseline before making performance or reliability claims.
- Extend testing to larger, independently sourced datasets and report reproducibility, failures and relevant ethical risks.

For the methodology and evaluation design, see [the research brief](docs/RESEARCH.md).

## License

See [`LICENSE`](LICENSE). No affiliation, patent, publication, production deployment or independent endorsement is implied.
