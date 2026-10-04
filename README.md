# ClaimPilot

A production-grade **multi-agent insurance claims processor** built with LangChain and LangGraph.
Simple claims are settled automatically; risky or high-value claims go to a human adjuster.

This repository accompanies the **ClaimPilot video course**. Every lesson is a tagged commit:

```bash
git checkout v05   # the project exactly as it was at the end of lesson 5
```

## Quick start

Requirements: Python 3.12, [uv](https://docs.astral.sh/uv/), Git, Docker.

```bash
git clone https://github.com/<your-username>/claimpilot.git
cd claimpilot
uv sync                                   # create .venv and install dependencies
uv run python scripts/check_env.py        # verify your tools
uv run claimpilot                         # prints: ClaimPilot 0.1.0 is ready.
```

## Project layout

```
claimpilot/
├── docs/requirements.md      # what we are building
├── scripts/check_env.py      # development environment check
├── src/claimpilot/           # application code
├── pyproject.toml            # project metadata and dependencies
└── .python-version           # Python 3.12
```

## Documentation

- [Requirements](docs/requirements.md)
