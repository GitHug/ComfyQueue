"""
ComfyOllama — PromptQueueNode
A custom ComfyUI node that serves prompts sequentially from a list.
The last prompt is never consumed and repeats indefinitely.
"""

import json
from pathlib import Path

STATE_FILE = Path(__file__).parent / "queue_state.json"


def _load_state() -> dict:
    if STATE_FILE.exists():
        try:
            return json.loads(STATE_FILE.read_text(encoding="utf-8"))
        except (json.JSONDecodeError, OSError):
            pass
    return {}


def _save_state(state: dict) -> None:
    try:
        STATE_FILE.write_text(json.dumps(state, indent=2), encoding="utf-8")
    except OSError:
        pass


class PromptQueueNode:
    _state: dict = _load_state()

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "prompts": ("STRING", {"multiline": True}),
            },
            "optional": {
                "external_prompt": ("STRING", {"forceInput": True}),
                "reset_queue": ("BOOLEAN", {"default": False}),
            },
            "hidden": {
                "unique_id": "UNIQUE_ID",
            },
        }

    RETURN_TYPES = ("STRING", "INT", "STRING")
    RETURN_NAMES = ("prompt", "queue_index", "history")
    FUNCTION = "execute"
    CATEGORY = "ComfyOllama"

    @classmethod
    def IS_CHANGED(cls, **kwargs):
        return float("nan")

    def execute(
        self,
        prompts: str,
        unique_id: str = "default",
        external_prompt: str = "",
        reset_queue: bool = False,
    ):
        # 1. Parse base lines
        base_lines = [line.strip() for line in prompts.splitlines() if line.strip()]

        state = PromptQueueNode._state

        # 2. Init state for this node instance
        if unique_id not in state:
            state[unique_id] = {
                "index": 0,
                "last_prompts_text": "",
                "history": [],
                "extra_prompts": [],
            }

        s = state[unique_id]

        # Ensure all keys exist (backward compat with older state files)
        s.setdefault("history", [])
        s.setdefault("extra_prompts", [])
        s.setdefault("last_prompts_text", "")
        s.setdefault("index", 0)

        # 3. Change detection: if prompts text changed, reset index and extra_prompts
        if prompts != s["last_prompts_text"]:
            s["index"] = 0
            s["extra_prompts"] = []
            s["last_prompts_text"] = prompts

        # 4. Apply reset_queue
        if reset_queue:
            s["index"] = 0
            s["history"] = []
            s["extra_prompts"] = []

        # 5. Append external_prompt if provided
        if external_prompt and external_prompt.strip():
            s["extra_prompts"].append(external_prompt.strip())

        # 6. Build effective list
        lines = base_lines + s["extra_prompts"]

        # 7. Guard: empty list
        if not lines:
            _save_state(state)
            return ("", 0, "")

        # 8. Clamp index
        index = min(s["index"], len(lines) - 1)

        # 9. Resolve current prompt
        current_prompt = lines[index]

        # Store index before advance for return value
        index_before_advance = index

        # 10. Advance (park at last)
        if index < len(lines) - 1:
            index += 1
        s["index"] = index

        # 11. Append to history
        s["history"].append(current_prompt)

        # 12. Save state
        _save_state(state)

        # 13. Build history string
        history_str = "\n".join(
            f"[{i + 1}] {p}" for i, p in enumerate(s["history"])
        )

        # 14. Return (1-based index = index_before_advance + 1)
        return (current_prompt, index_before_advance + 1, history_str)


NODE_CLASS_MAPPINGS = {
    "PromptQueue": PromptQueueNode,
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "PromptQueue": "Prompt Queue",
}
