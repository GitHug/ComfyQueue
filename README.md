# ComfyQueue

A custom [ComfyUI](https://github.com/comfyanonymous/ComfyUI) node that serves prompts sequentially from a list — one per workflow run. The last prompt is never consumed and repeats indefinitely, making it easy to run a batch of prompts hands-free.

## Installation

Copy this directory into your ComfyUI custom nodes folder and restart ComfyUI:

```bash
cp -r ComfyQueue/ /path/to/ComfyUI/custom_nodes/
```

The **Prompt Queue** node will appear under the `ComfyOllama` category in the node menu.

## Usage

1. Add a **Prompt Queue** node to your workflow.
2. Enter your prompts in the `prompts` field — one per line.
3. Queue up runs. Each run receives the next prompt in the list.
4. Once the last prompt is reached, it repeats on every subsequent run until you reset or change the list.

### Inputs

| Input | Type | Description |
|-------|------|-------------|
| `prompts` | STRING (multiline) | One prompt per line — the base queue |
| `external_prompt` | STRING (optional) | When connected and non-empty, appends to the queue for future runs |
| `reset_queue` | BOOLEAN (optional) | Resets the index, history, and any appended prompts |

### Outputs

| Output | Type | Description |
|--------|------|-------------|
| `prompt` | STRING | The current prompt text |
| `queue_index` | INT | 1-based position in the queue |
| `history` | STRING | All prompts served so far, prefixed with run number |

### Example

With `prompts` set to:
```
a red apple
a blue banana
a green cherry
```

| Run | `prompt` | `queue_index` |
|-----|----------|---------------|
| 1 | a red apple | 1 |
| 2 | a blue banana | 2 |
| 3 | a green cherry | 3 |
| 4+ | a green cherry | 3 (parked) |

## State Persistence

Queue state (current index, history, appended prompts) is saved to `queue_state.json` in the node directory after every run. State is keyed per node instance, so multiple **Prompt Queue** nodes in the same workflow are independent.
