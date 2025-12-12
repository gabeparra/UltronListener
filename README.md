# Caption AI

Meeting caption listener + summarizer with pluggable LLM backends.

## Overview

Caption AI is a Python application that listens to meeting captions (or generates fake transcript segments for testing) and produces rolling summaries using configurable LLM backends. It supports OpenAI/ChatGPT, Grok, Gemini, and local models via Ollama.

## Architecture

```
┌─────────────┐
│   Capture   │──┐
│  (Whisper/  │  │
│   Browser)  │  │
└─────────────┘  │
                 ▼
            ┌─────────┐
            │   Bus   │──┐
            │ (Queue) │  │
            └─────────┘  │
                         │
            ┌─────────┐  │
            │ Storage │◄─┘
            │(SQLite) │
            └─────────┘
                 │
                 ▼
            ┌─────────────┐
            │ Summarizer  │──┐
            │   (Loop)    │  │
            └─────────────┘  │
                             │
            ┌─────────────┐  │
            │ LLM Router  │◄─┘
            └─────────────┘
                 │
        ┌────────┼────────┐
        ▼        ▼        ▼
    OpenAI   Gemini   Ollama
     Grok
```

## Installation

### Prerequisites

- Python 3.11+
- [uv](https://github.com/astral-sh/uv) package manager

### Setup

1. Clone the repository:
```bash
git clone https://github.com/gabeparra/UltronListener.git
cd UltronListener
```

2. Install dependencies with uv:
```bash
uv sync
```

3. Activate the virtual environment:
```bash
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
```

## Configuration

Create a `.env` file in the project root:

```env
# LLM Provider (openai, grok, gemini, local)
LLM_PROVIDER=local

# OpenAI (if using OpenAI)
OPENAI_API_KEY=sk-...

# Grok (if using Grok)
GROK_API_KEY=xai-...

# Gemini (if using Gemini)
GEMINI_API_KEY=...

# Local Ollama (if using local)
OLLAMA_BASE_URL=http://localhost:11434
OLLAMA_MODEL=llama2

# Storage (optional, defaults to ~/.caption_ai/segments.db)
STORAGE_PATH=~/.caption_ai/segments.db
```

## Usage

### Running with Fake Data

The simplest way to test is with fake transcript segments:

```bash
python -m caption_ai
```

or

```bash
python -m caption_ai.main
```

This will:
1. Generate fake meeting transcript segments
2. Store them in SQLite
3. Produce rolling summaries every 15 seconds using the configured LLM

### Using Local Ollama

1. Install and start Ollama:
```bash
# Install Ollama from https://ollama.ai
ollama serve
```

2. Pull a model:
```bash
ollama pull llama2
```

3. Set `LLM_PROVIDER=local` in `.env` and run:
```bash
python -m caption_ai
```

## Development

### Setup

```bash
# Install with dev dependencies
uv sync --dev

# Run linting
make lint

# Run tests
make test

# Run the application
make run
```

### Project Structure

```
caption-ai/
├── src/
│   └── caption_ai/
│       ├── __init__.py
│       ├── config.py          # Configuration management
│       ├── bus.py              # Segment queue
│       ├── storage.py          # SQLite storage
│       ├── prompts.py          # Prompt templates
│       ├── summarizer.py       # Rolling summarizer loop
│       ├── main.py             # CLI entrypoint
│       ├── capture/            # Audio capture (future)
│       └── llm/                # LLM clients
│           ├── base.py         # LLM interface
│           ├── router.py       # Provider router
│           ├── openai_api.py
│           ├── gemini_api.py
│           ├── grok_api.py
│           └── local_ollama.py
├── tests/                      # Test suite
├── scripts/                    # Utility scripts
├── pyproject.toml              # Project metadata
├── Makefile                    # Development commands
└── README.md
```

## Roadmap

- [ ] **Whisper Audio Capture**: Real-time audio transcription using faster-whisper
- [ ] **Teams UI Captions**: Extract captions from Microsoft Teams UI
- [ ] **Browser Automation**: Use Playwright to capture captions from web meetings
- [ ] **Full LLM Implementations**: Complete OpenAI, Gemini, and Grok API integrations
- [ ] **Speaker Diarization**: Identify and label speakers
- [ ] **Export Formats**: Export summaries to Markdown, PDF, etc.

## Contributing

Contributions are welcome! Please:

1. Fork the repository
2. Create a feature branch
3. Make your changes with proper type hints and async patterns
4. Run `make lint` and `make test`
5. Submit a pull request

### Dev Setup

```bash
# Clone and setup
git clone https://github.com/gabeparra/UltronListener.git
cd UltronListener
uv sync --dev

# Run tests
pytest

# Format and lint
ruff check .
ruff format .
```

## License

MIT License - see LICENSE file for details.

