# Enterprise AI Ops Copilot

An AI-powered operations copilot built on AWS Bedrock, LangGraph, and RAG to assist enterprise IT operations teams with incident resolution, runbook guidance, and ticket management.

## Features

- **Conversational AI** — Chat interface powered by AWS Bedrock Claude models
- **RAG Pipeline** — Retrieval-augmented generation over internal policies, runbooks, and incident reports
- **Agentic Workflows** — LangGraph-based multi-step reasoning and tool use
- **Integrations** — ServiceNow, Snowflake, and Microsoft Teams (mock + real)
- **Guardrails** — AWS Bedrock Guardrails for responsible AI enforcement
- **Evaluation** — Automated RAGAS-style evaluation of response quality

## Quick Start

```bash
cp .env.example .env
# Fill in your AWS credentials and config in .env

pip install -r requirements.txt

# Ingest documents
python scripts/ingest_documents.py

# Start the API server
uvicorn app.main:app --reload
```

Or with Docker:

```bash
docker-compose up --build
```

## Project Structure

See [docs/project_overview.md](docs/project_overview.md) for full architecture and design details.

## API Docs

Once running, visit `http://localhost:8000/docs` for the interactive Swagger UI.

## License

Apache 2.0 — see [LICENSE](LICENSE).
