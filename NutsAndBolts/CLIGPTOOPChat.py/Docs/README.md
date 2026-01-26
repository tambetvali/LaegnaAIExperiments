# Documentation for `CLIGPTOOPChat.py`

This directory contains the documentation set for the **CLIGPTOOPChat** architecture — a minimal, readable, and extensible framework for building command‑line chat interfaces across multiple model backends (Ollama, LiteLLM, LitGPT).  
The documents here explain the philosophy, structure, and usage patterns behind the system, and guide both beginners and advanced users through the architecture.

---

## ⭐ Central Document: *Session Memory and General Considerations*

The most important conceptual overview lives here:

👉 **[sessionandconsideration.md](sessionandconsideration.md)**

This document explains:

- Why the architecture is intentionally simple  
- How session memory works and why it is not hidden behind abstractions  
- How different drivers (Ollama, LiteLLM, LitGPT) interpret message history  
- How initial prompts, templates, and system messages shape model behavior  
- How complexity grows in a controlled way  
- How the OOP structure supports extension without forcing it  
- How to think about the system in UML terms  

If you read only one document in this folder, read this one.

---

## Documentation Index  
Below is the space reserved for links to explanations of each file in the `CLIGPTOOPChat.py` folder.  
Each document will describe the purpose, structure, and usage of its corresponding file.

(***Warning***: this documentation index contains stub, and it will be used when I add documentation files for each separate code file. Currently, you only
find the one-line summaries for each file here)

### Core Architecture  
- *[service.py](service.py.md)* — Explanation of `AIService`, parent/child chaining, message history, and the unified interface  
- *[filename.py](filename.py.md)* — How configuration discovery works and why the “modelselector root” matters  
- *[modelselector.py](modelselector.py.md)* — How model lists are generated and how the active model is chosen  

### Drivers  
- *[ollama_streamer.py](ollama_streamer.py.md)* — Ollama driver, chat schema, streaming behavior  
- *[litellm_streamer.py](litellm_streamer.py.md)* — LiteLLM driver, OpenAI‑style messages, cloud/local flexibility  
- *[litgpt_streamer.py](litgpt_streamer.py.md)* — LitGPT driver, templates, fine‑tuning workflows, non‑streaming behavior  

### Tools & Utilities  
- *[ollamaautomodelsjsonconf.py](ollamaautomodelsjsonconf.py.md)* — Auto‑generation of Ollama model lists  
- *[models_config.py](models_config.py.md)* — Structure of model configuration files  
- *[chat.py](chat.py.md)* — The minimal example chat client and how to extend it  

---

## What You Will Learn From This Documentation

### 1. The Philosophy of Simplicity  
The project is intentionally minimal.  
Every file is short enough to read in one sitting.  
Every class is small enough to draw as a UML diagram.  
Every architectural choice is made to keep the system teachable and adaptable.

### 2. The OOP Structure  
You will understand:

- Why `AIService` is the single base class  
- How drivers inherit from it  
- How parent/child instances form a conversation chain  
- How to extend the system without rewriting it  

This is OOP used as a tool, not a burden.

### 3. Session Memory and Prompting  
You will learn:

- How message history is stored  
- How recursive reconstruction works  
- Why system prompts matter  
- How different backends interpret history  
- How to add templates, initial prompts, or custom tags  

This is the conceptual heart of the system.

### 4. Driver Differences and Their Roles  
Each backend has a different purpose:

- **Ollama** — precise, local, predictable  
- **LiteLLM** — general, cloud‑friendly, multi‑provider  
- **LitGPT** — administrative, fine‑tuning oriented, template‑driven  

The documentation explains how each driver formats prompts, handles history, and streams (or does not stream) output.

### 5. How to Grow the System  
The documents show how to:

- Add new drivers  
- Add new configuration layers  
- Add system‑level behaviors (logging, tools, etc.)  
- Keep complexity under control as the system evolves  

The architecture is intentionally open-ended.

---

## Conclusion

The `Docs/` folder is the conceptual backbone of the **CLIGPTOOPChat** project.  
It explains not only *how* the system works, but *why* it is built this way — with clarity, minimalism, and extensibility as guiding principles.

Whether you are:

- a beginner learning how chat architectures work,  
- an administrator managing models and fine‑tuning workflows,  
- or an advanced programmer extending the system,  

these documents give you the mental model you need to understand the codebase and build confidently on top of it.

As you explore the rest of the project, return to these documents whenever you want to reconnect with the architectural intent or understand how the pieces fit together.

