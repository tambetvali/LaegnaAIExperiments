# Update method:

1. Initially, I do some experiments in files whose names are prefixed with e1, e2 etc.:
- Each file has chapters, which starts with tasks to copilot.
- We ask to write code, but in form of manual, which contains essential, simplistic code yet opening up our architecture.
- We are not going to test whether we can run the code: this is API check we are going to test, whether we have compatible API within given design.
- The resulting documentation - indeed we can execute some, but it's not very important - can be fed back to copilot, giving it the link "https://github.com/tambetvali/LaegnaAIExperiments/new/main/Drafts/AIForum" as our design essentials. Based on the url it will use compatible libraries and services to fully implement the application.

# Laegna AI Forum Experiments

This directory contains a set of evolving design and implementation notes for building an extensible, AI‑enabled Q&A forum with Markdown, threading, and pluggable extensions. The goal is to keep the core small and understandable, while leaving clear paths for growth into a serious, product‑ready system.

Below are the three main design documents and how they fit together.

---

## Design documents

### 1. [e1copilot_AIForum.md](e1copilot_AIForum.md)

**Summary:**  
This document lays out the conceptual foundation of the AI Forum: what it is, why it exists, and how AI‑assisted development fits into the workflow. It focuses on the *shape* of the system—Q&A trees, Markdown as the primary medium, and the idea of extensions that can add capabilities like file context, web browsing, or code tools.

**Explanation:**  
Here you’ll find the high‑level reasoning behind the chosen architecture:

- Why a Q&A tree instead of a flat chat  
- Why Markdown is the core format  
- How AI tools are treated as “first‑class collaborators”  
- How the system is designed to be approachable for different skill levels  

This document gives you confidence that the forum is not a one‑off experiment, but a general framework you can keep extending without painting yourself into a corner.

---

### 2. [e2connectAIAPI.md](e2connectAIAPI.md)

**Summary:**  
This document describes how the forum connects to AI services: local models, OpenAI‑compatible APIs, and potentially Copilot‑style endpoints. It defines a minimal, stateless connector interface that can be wired to different backends without changing the rest of the system.

**Explanation:**  
The focus here is on *how* and *why* the libraries and tools are chosen:

- Using HTTP/JSON and OpenAI‑style schemas as the “lingua franca”  
- Keeping the connector stateless so context is always explicit and testable  
- Allowing both free and paid services to be swapped in with minimal configuration  
- Ensuring the same connector pattern can support local, hosted, and future endpoints  

By the end of this document, you should feel comfortable that the API layer is stable, extensible, and not tied to any single provider.

---

### 3. [e3AIinferencechat.md](e3AIinferencechat.md)

**Summary:**  
This document focuses on the actual chat and inference behavior: how Q&A objects are created, how context is built from parent/previous nodes, and how extensions hook into the lifecycle of a question and answer.

**Explanation:**  
It explains:

- How a single Q&A node is structured  
- How the tree is traversed to build context  
- How extensions register lifecycle hooks  
- How the AI connector turns Markdown questions into Markdown answers  

This document ties together the conceptual forum design and the API connector into a coherent, testable chat flow.

---

# Initial functionality and behavior

At the beginning, the system implements the following core behavior:

- The user writes an initial Markdown article in a WYSIWYG‑style editor. This becomes the **seed Q&A**.  
- Before submitting, the user can **attach extensions** such as file context, web link analysis, or other toolkits.  
- When the user submits, the AI generates an answer. At this point:
  - The Q&A (question + answer) is stored  
  - The extension state is **snapshotted**  
  - Any extension activity is considered part of this checkpoint  

From there:

- New Q&As can be created as **replies**  
- Each reply can inherit or modify the extension set  
- Some aspects can be reset (e.g., removing certain extensions or ignoring certain Q&As in relation to parent/seed Q&A which is being answered)  
- Advanced context management is possible later, but not described in detail yet  

---

# Development plan

Below is a high‑level manual for how to move from the current drafts and code into a working, extensible system. This is a plan, not code.

## Step 1: Implement the Q&A tree

**Goal:**  
Each new Q&A has context only from its ancestors: the chain of `parent` and `previous` nodes back to the initial question.

**Plan:**

- Define a clear Q&A data structure  
- Implement creation, traversal, and context‑building functions  
- Decide how context is represented for the AI  
- Wire reply logic into the UI  
- Ensure the AI connector receives the correct context chain  

---

## Step 2: Add extension support with stateless checkpoints

**Goal:**  
Allow extensions to be attached to a Q&A, with lifecycle hooks and state snapshots.

**Plan:**

- Define a base extension interface  
- Implement an extension manager  
- Decide how extension state is stored  
- Define checkpoint behavior  
- Ensure extension state is cloned for child Q&As  

---

## Step 3: Add filesystem, Git, and web browsing extensions

**Goal:**  
Add concrete extensions that do useful work.

**Plan:**

- Filesystem/code mode: list files, read files, optionally write  
- Git extension: initialize repo, commit per Q&A, branch on replies  
- Web browsing extension: fetch URL, extract content, store in state  
- Integrate these into the extension lifecycle  

---

## Step 4: Develop advanced features

**Goal:**  
Grow the system beyond the basics.

**Plan:**

- Context management UI  
- Extension configuration UI  
- Multiple AI backends  
- Saved sessions and sharing  
- Export/import of threads  

---

## Step 5: Testing, design, and product readiness

**Goal:**  
Make the system robust and pleasant to use.

**Plan:**

- Unit tests for Q&A tree traversal  
- Tests for extension lifecycle  
- Integration tests for AI calls  
- Improved UI design  
- Documentation for users and extension developers  

---

# Supporting different user skill levels

This project is intentionally designed so that people with different backgrounds can still move forward:

- **Copy‑paste coders** can follow the documents and gradually tweak the system  
- **Framework thinkers** can refine the extension system and data model  
- **Intermediate developers** can use AI tools to bridge gaps and iterate  

Together, the three documents form a general framework: not just a single app, but a small, understandable platform for AI‑assisted Q&A with room to grow in any direction.
