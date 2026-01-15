# 🧾 Program User Guide: Local AI with RAG & Python Interface

This guide builds on the previous chapter (**Training Guide**) and explains **how to use your trained AI locally**, manage multiple models, integrate RAG memory for focus, and serve a Python/Flask interface with real-time capabilities.

---

## 🔗 Reference to Training Guide

> Before using this guide, see the **Training Guide** for:
> - LitGPT training & LoRA
> - Dataset preparation from cards
> - GGUF export
> - Ollama deployment  
> This chapter assumes you already have a working **personal AI model**.

---

## 🧠 RAG Memory Overview

- **RAG (Retrieval-Augmented Generation)** can work **without training**, but its main power comes when linked to your **focus elements**.
- In practice, RAG:
  - Provides context for specific cards or knowledge
  - Is **not used to overwrite training** — it is supplemental
  - Allows the AI to respond with **particular thoughts** rather than expected patterns

> Think of RAG as “reminding the AI about your key ideas” rather than teaching it new patterns.

---

## 🖥 Supported Models

Your system can handle up to **five models simultaneously**, or download additional inference-only models:

| Model | RAM / GPU | Training Capability | Notes |
|-------|-----------|-------------------|-------|
| Tiny-LLaMA / Phi-2 | 4 GB | LoRA only | Lightweight, symbolic |
| Mistral-7B | 16 GB | LoRA | Practical researcher |
| LLaMA-3 8B | 32 GB | Full finetuning | Opus-class, professional |
| Codellama | 16–32 GB | Inference only | Coding assistant |
| Spiritual/Philosophy | 16–32 GB | Inference only | Personal reflection |

> Inference-only models **cannot be fine-tuned** but can supplement the training models.

---

## ⚙ Python Interface: Serving Q&A with RAG

We provide a **real-time interface** using:

- **Python**
- **Flask** (backend server)
- **Mistune** (Markdown rendering)
- **Backbone.js** (frontend, real-time updates)

### Folder Structure Example

```
program_interface/
├─ app.py
├─ models/
├─ templates/
│ └─ index.html
├─ static/
│ └─ app.js
└─ tools/
```


- `models/` → trained models or inference-only models
- `tools/` → optional Python tools that augment responses

---

### 1️⃣ Flask Backend Example

\`\`\`python
from flask import Flask, request, jsonify
from ollama import OllamaClient  # Python wrapper for local Ollama service
import json

app = Flask(__name__)
client = OllamaClient()

# Load RAG context per tool
tools = {}
with open("tools/tool_contexts.json") as f:
    tools = json.load(f)

@app.route("/ask", methods=["POST"])
def ask_model():
    prompt = request.json.get("prompt", "")
    tool_tag = request.json.get("tool", None)

    # Include tool context if any
    if tool_tag and tool_tag in tools:
        context = tools[tool_tag]
        prompt = context + "\n" + prompt

    # Ask the AI
    response = client.ask(model="personal_ai", prompt=prompt)
    return jsonify({"response": response})

if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000)
\`\`\`

> Each **tool** provides additional context; the AI merges it with the prompt.

---

### 2️⃣ Adding Tools

- Add a JSON file in `tools/tool_contexts.json`:

\`\`\`json
{
    "code_debugger": "You are a code debugging assistant. Only explain errors in code.",
    "philosophy_tutor": "You are a philosophy tutor. Provide concise reasoning."
}
\`\`\`

- In Flask, send `"tool": "code_debugger"` along with the question
- The AI uses this context automatically

> Previous fine-tuning applies: the model already learned your cards, LoRA weights, and attention patterns.  
> Tools **just provide tags and context**, without retraining unless needed.

---

## 📝 Command-Line Inference Example

If you prefer **CLI only**, you can query Ollama models using their clients:

```bash
# Install Ollama CLI
# For Linux / Windows / MacOS: download from official repository

# Run a query to your local model
ollama generate personal_ai "Explain why RAG preserves identity"

# With inference-only model
ollama generate codellama "Write a Python function to sort a list"
```

> CLI inference works without Flask, real-time frontend, or RAG tools.  
> This is useful for quick checks or automated scripts.

---

## 🔄 Keeping Models Updated

1. Add new cards or tools
2. Call your **update pipeline** (from Training Guide / AdaptiveAI)
3. Ollama will use the updated GGUF snapshot
4. RAG memory automatically supplements **new focus elements**

> This allows your system to **evolve incrementally**, both in knowledge (cards) and in contextual behavior (tools/RAG).

---

## ✅ Summary

- **RAG is optional but recommended for focus elements**
- Python + Flask + Mistune + Backbone.js allows **interactive Q&A**
- Tools augment context with tags
- CLI inference is always available
- Previous fine-tuning works for all new cards and tools

> You now have a **multi-model, locally served, evolving AI** system, capable of combining **training, RAG memory, and tool-based context**.

---

> Next steps: Customize your tools, add more focus elements, and serve multiple models in parallel.
