# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project

ComfyOllama — a custom ComfyUI node package that provides a **Prompt Queue** node. It serves prompts sequentially from a multiline list, parking indefinitely on the last entry.

## Project Structure

```
ComfyOllama/
├── __init__.py          # PromptQueueNode implementation + NODE_CLASS_MAPPINGS
├── pyproject.toml       # Registry/package metadata
├── queue_state.json     # Runtime state (auto-created, gitignore this)
└── CLAUDE.md            # This file
```

## Key Design Notes

- **Node key:** `"PromptQueue"` / display name `"Prompt Queue"` / category `"ComfyOllama"`
- **Outputs:** `prompt (STRING)`, `queue_index (INT, 1-based)`, `history (STRING)`
- **State** is persisted to `queue_state.json` (same directory as `__init__.py`) keyed by ComfyUI `UNIQUE_ID`
- `IS_CHANGED` returns `float("nan")` so the node always re-executes (no caching)
- Last prompt parks: index never advances past `len(lines) - 1`
- `external_prompt` input appends to `extra_prompts`; consumed after the base list
- `reset_queue=True` clears index, history, and extra_prompts

## Installation

Copy this directory into `ComfyUI/custom_nodes/` and restart ComfyUI.
