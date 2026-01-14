# AI inference / chat

Given that we have the API from previous task, and we can see it's designed to be extensible to support the AI systems given in the list of it's beginning:
- We now design an AI Q&A class, which can use that class to connect.

Our modulus:
- Each user, who logs into forum, will choose their service and model on their own, which are used for all their replies.
  - Akin to normal chat session, where you choose your model, but it does not depend which models you used for the discussion in same chat before this.

# Task

```
Now, in the same format, you need to design this:

- It's a Q&A box: very simple open source, with online available service API we are going to use, WYSIWYG editor for markdown appears on left side, and the right side assigns key waiting an AI response to this.
- It has "parent" or "previous" variable assigning the previous Q&A: one or another of those two is NULL, and the other one is set to a Q&A in the same form.
- It has extension support and you write extension manual: Extension supports the following feature: extension can be instantiated to this Q&A box, and it might contain browsed link information, files, or any active toolkit; it's variables will be initialized.
- Q&A is initialized with another Q&A as input, and extension instances are inherit, their variables copied, and before-question, after-question, before-answer and after-answer calls are triggered to let it do it's work, additionally it can provide free set of functions, methods, variables.
- You create an example implementation, which uses the simplest Git access from Python to provide Git repo, for each new thread with "previous" set, it will create new version before_queswtion and commit after_answer; with each one which has "parent" set, it will create a new branch in Git; it always knows the current version and is able to serve main folder file list.
- Q&A uses this given functionality for these functions: either new Q&A is added in the end of the list if "reply" button of the parent is used, "previous" linking to the last existing answer to the parent; new branch appears to child comment if "reply" of any of those is used - this functionality extends to nested loop.
```

## Extensible Q&A Box with Markdown WYSIWYG, Threading, and Git-Backed Extension

This design builds on the previous minimal Flask setup, but focuses on:

- A **Q&A box** with:
  - Left: WYSIWYG-style Markdown editor.
  - Right: AI answer panel.
- **Threading model** with `parent` and `previous` links.
- An **extension system** with lifecycle hooks.
- A **Git-backed extension** that:
  - Creates commits for each Q&A.
  - Creates branches for replies.
  - Tracks current version and lists files.

All code is shown as conceptual, minimal, and extensible.

---

### 1. Data model: Q&A with `parent` and `previous`

We’ll use an in-memory store for simplicity; you can replace it with a database later.

- **Fields**:
  - `id`: unique identifier.
  - `question`: Markdown text.
  - `answer`: Markdown text.
  - `parent_id`: ID of the parent Q&A (for branching), or `None`.
  - `previous_id`: ID of the previous Q&A in the same linear chain, or `None`.
  - `extension_state`: arbitrary dict for extension data.

```python
# Simplified in-memory store
QAS = {}
NEXT_ID = 1

def create_qa(question, answer="", parent_id=None, previous_id=None, extension_state=None):
    global NEXT_ID
    qa_id = NEXT_ID
    NEXT_ID += 1
    QAS[qa_id] = {
        "id": qa_id,
        "question": question,
        "answer": answer,
        "parent_id": parent_id,
        "previous_id": previous_id,
        "extension_state": extension_state or {},
    }
    return QAS[qa_id]

def get_qa(qa_id):
    return QAS.get(qa_id)

def get_thread_root():
    # For demo: return the first Q&A or None
    return QAS.get(1)

def get_children(parent_id):
    return [qa for qa in QAS.values() if qa["parent_id"] == parent_id]

def get_chain_from_root(root_id):
    # Follow previous_id links to build a linear chain
    chain = []
    current = QAS.get(root_id)
    while current:
        chain.append(current)
        next_qa = next((qa for qa in QAS.values() if qa["previous_id"] == current["id"]), None)
        current = next_qa
    return chain
```

---

### 2. Extension system: lifecycle hooks and inheritance

Extensions are small objects with well-defined hooks:

- `before_question(qa, context)`
- `after_question(qa, context)`
- `before_answer(qa, context)`
- `after_answer(qa, context)`

They can:

- Maintain internal state.
- Expose helper methods.
- Store data in `extension_state`.

#### 2.1. Base extension interface

```python
class QAExtension:
    """
    Base class for Q&A extensions.
    """

    def __init__(self, state=None):
        self.state = state or {}

    def clone_for_child(self):
        # Inherit state for new Q&A
        return self.__class__(state=self.state.copy())

    def before_question(self, qa, context):
        pass

    def after_question(self, qa, context):
        pass

    def before_answer(self, qa, context):
        pass

    def after_answer(self, qa, context):
        pass
```

#### 2.2. Extension manager

```python
class ExtensionManager:
    """
    Manages extension instances for a given Q&A.
    """

    def __init__(self, extensions=None):
        self.extensions = extensions or []

    def clone_for_child(self):
        return ExtensionManager(
            extensions=[ext.clone_for_child() for ext in self.extensions]
        )

    def run_before_question(self, qa, context):
        for ext in self.extensions:
            ext.before_question(qa, context)

    def run_after_question(self, qa, context):
        for ext in self.extensions:
            ext.after_question(qa, context)

    def run_before_answer(self, qa, context):
        for ext in self.extensions:
            ext.before_answer(qa, context)

    def run_after_answer(self, qa, context):
        for ext in self.extensions:
            ext.after_answer(qa, context)
```

---

### 3. Git-backed extension example

This extension:

- Initializes a Git repo (if not present).
- For each new Q&A in a **linear chain** (`previous` set), it:
  - Runs `before_question`: ensure working tree is clean / ready.
  - Runs `after_answer`: commit changes.
- For each Q&A with a **parent** (branching), it:
  - Creates a new branch.
  - Tracks current branch and commit.

This is intentionally minimal and conceptual.

```python
import os
import subprocess
from pathlib import Path

class GitQAExtension(QAExtension):
    def __init__(self, repo_path="qa_repo", state=None):
        super().__init__(state=state)
        self.repo_path = Path(repo_path)
        self._ensure_repo()

    def _ensure_repo(self):
        if not self.repo_path.exists():
            self.repo_path.mkdir(parents=True)
            subprocess.run(["git", "init"], cwd=self.repo_path, check=True)

    def _run(self, *args):
        subprocess.run(args, cwd=self.repo_path, check=True)

    def _write_qa_file(self, qa):
        # Simple: one file per Q&A
        filename = self.repo_path / f"qa_{qa['id']}.md"
        content = f"# Q{qa['id']}\n\n## Question\n\n{qa['question']}\n\n## Answer\n\n{qa['answer']}\n"
        filename.write_text(content, encoding="utf-8")

    def before_question(self, qa, context):
        # Decide branch based on parent/previous
        parent_id = qa.get("parent_id")
        previous_id = qa.get("previous_id")

        if parent_id:
            # New branch from parent
            branch_name = f"branch_{qa['id']}"
            base_branch = self.state.get(f"branch_for_{parent_id}", "main")
            self._run("git", "checkout", base_branch)
            self._run("git", "checkout", "-b", branch_name)
            self.state[f"branch_for_{qa['id']}"] = branch_name
        elif previous_id:
            # Continue same branch as previous
            branch_name = self.state.get(f"branch_for_{previous_id}", "main")
            self._run("git", "checkout", branch_name)
            self.state[f"branch_for_{qa['id']}"] = branch_name
        else:
            # Root Q&A on main
            self._run("git", "checkout", "-B", "main")
            self.state[f"branch_for_{qa['id']}"] = "main"

    def after_answer(self, qa, context):
        # Write file and commit
        self._write_qa_file(qa)
        self._run("git", "add", ".")
        msg = f"Q{qa['id']}: {qa['question'][:40]}"
        self._run("git", "commit", "-m", msg)

    def list_files(self):
        return [p.name for p in self.repo_path.iterdir() if p.is_file()]
```

---

### 4. Flask UI: WYSIWYG-style Markdown editor and threaded replies

We’ll create:

- A single page showing:
  - Left: editor for the current question.
  - Right: AI answer.
  - Below: thread view with “Reply” buttons.
- When you click “Reply”:
  - If replying to the **last answer** in a chain → new Q&A with `previous` set.
  - If replying to any other Q&A → new Q&A with `parent` set (branch).

#### 4.1. Flask setup and global extension manager

```python
from flask import Flask, render_template_string, request, jsonify

app = Flask(__name__)

# Single global extension manager with Git extension
ext_manager = ExtensionManager(extensions=[GitQAExtension(repo_path="qa_repo")])

# Initialize a root Q&A
root_qa = create_qa("Welcome! Ask your first question here.")
```

#### 4.2. Template with inline CSS and simple JS

```python
TEMPLATE = r"""
<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <title>Q&A Box with Extensions</title>
  <style>
    body { font-family: system-ui, sans-serif; margin: 0; padding: 0; background: #f5f5f7; }
    .page { max-width: 1000px; margin: 0 auto; padding: 1rem; }
    h1 { font-size: 1.3rem; margin-bottom: 0.5rem; }
    .layout { display: flex; gap: 1rem; }
    .col { flex: 1; }
    textarea { width: 100%; min-height: 150px; padding: 0.5rem; border-radius: 4px; border: 1px solid #ccc; resize: vertical; box-sizing: border-box; }
    .answer-box { padding: 0.5rem; border-radius: 4px; border: 1px solid #ddd; background: #fff; min-height: 150px; white-space: pre-wrap; }
    .bar { margin-top: 0.5rem; display: flex; justify-content: flex-end; gap: 0.5rem; }
    button { padding: 0.3rem 0.6rem; border-radius: 4px; border: none; background: #222; color: #fff; cursor: pointer; }
    button:hover { background: #444; }
    .thread { margin-top: 1rem; padding: 0.5rem; background: #fff; border-radius: 4px; border: 1px solid #ddd; }
    .qa-item { border-bottom: 1px solid #eee; padding: 0.4rem 0; }
    .qa-item:last-child { border-bottom: none; }
    .qa-meta { font-size: 0.8rem; color: #666; }
    .qa-question { font-weight: 600; }
    .qa-answer { margin-top: 0.2rem; }
  </style>
</head>
<body>
  <div class="page">
    <h1>Q&A Box with Markdown and Git Extension</h1>
    <div class="layout">
      <div class="col">
        <h2>Question</h2>
        <textarea id="question" placeholder="Write your question in Markdown..."></textarea>
      </div>
      <div class="col">
        <h2>Answer</h2>
        <div class="answer-box" id="answer"></div>
      </div>
    </div>
    <div class="bar">
      <input type="hidden" id="reply_to_id" value="{{ current_id }}">
      <button id="send">Ask</button>
    </div>

    <div class="thread">
      <h2>Thread</h2>
      {% for qa in chain %}
      <div class="qa-item">
        <div class="qa-meta">Q{{ qa.id }} {% if qa.parent_id %}(parent: {{ qa.parent_id }}){% endif %} {% if qa.previous_id %}(previous: {{ qa.previous_id }}){% endif %}</div>
        <div class="qa-question">{{ qa.question }}</div>
        <div class="qa-answer">{{ qa.answer }}</div>
        <button onclick="replyTo({{ qa.id }})">Reply</button>
      </div>
      {% endfor %}
    </div>
  </div>

  <script>
    async function askQuestion() {
      const question = document.getElementById('question').value.trim();
      const replyToId = document.getElementById('reply_to_id').value || null;
      if (!question) return;
      const resp = await fetch("/", {
        method: "POST",
        headers: {"Content-Type": "application/json"},
        body: JSON.stringify({ question: question, reply_to_id: replyToId })
      });
      const data = await resp.json();
      document.getElementById('answer').textContent = data.answer || "(no answer)";
      if (data.redirect) {
        window.location = data.redirect;
      }
    }

    function replyTo(id) {
      document.getElementById('reply_to_id').value = id;
      document.getElementById('question').value = "";
      document.getElementById('answer').textContent = "";
    }

    document.getElementById('send').addEventListener('click', askQuestion);
  </script>
</body>
</html>
"""
```

#### 4.3. Flask route logic: reply semantics and extension hooks

- If replying to the **last Q&A in the chain**:
  - New Q&A has `previous_id` set to that last Q&A.
- If replying to any other Q&A:
  - New Q&A has `parent_id` set to that Q&A.

```python
def find_last_in_chain(root_id):
    chain = get_chain_from_root(root_id)
    return chain[-1] if chain else None

@app.route("/", methods=["GET", "POST"])
def index():
    root = get_thread_root()
    if request.method == "GET":
        chain = get_chain_from_root(root["id"]) if root else []
        return render_template_string(
            TEMPLATE,
            chain=chain,
            current_id=root["id"] if root else "",
        )

    data = request.get_json(force=True)
    question = data.get("question", "")
    reply_to_id = data.get("reply_to_id")
    reply_to_id = int(reply_to_id) if reply_to_id else None

    parent_id = None
    previous_id = None

    if reply_to_id:
        last = find_last_in_chain(root["id"])
        if last and last["id"] == reply_to_id:
            previous_id = reply_to_id
        else:
            parent_id = reply_to_id

    # Clone extension manager for this Q&A
    local_ext_manager = ext_manager.clone_for_child()

    # Create Q&A with empty answer first
    qa = create_qa(question=question, answer="", parent_id=parent_id, previous_id=previous_id)

    context = {}
    local_ext_manager.run_before_question(qa, context)
    local_ext_manager.run_after_question(qa, context)

    # Call AI backend (placeholder)
    # Here you would use AIConnector from previous design.
    # For demo, we just echo the question.
    answer = f"Echo: {question}"
    qa["answer"] = answer

    local_ext_manager.run_before_answer(qa, context)
    local_ext_manager.run_after_answer(qa, context)

    return jsonify({
        "answer": answer,
        "redirect": "/"
    })
```

---

### 5. Extension manual: how to write your own extension

To create a new extension:

1. **Subclass `QAExtension`**:

   - Implement any of:
     - `before_question(self, qa, context)`
     - `after_question(self, qa, context)`
     - `before_answer(self, qa, context)`
     - `after_answer(self, qa, context)`

2. **Use `state` for persistent data**:

   - `self.state` is a dict that is:
     - Initialized when the extension is created.
     - Cloned for child Q&A via `clone_for_child()`.

3. **Register your extension**:

   - Add it to the global `ExtensionManager`:

```python
my_ext = MyCustomExtension()
ext_manager = ExtensionManager(extensions=[GitQAExtension(), my_ext])
```

4. **Access Q&A and context**:

   - `qa` is the current Q&A dict.
   - `context` is a free-form dict you can use to pass data between hooks.

5. **Expose helper methods**:

   - Your extension can define methods like `list_files()`, `get_current_branch()`, etc.
   - You can call them from Flask routes or other parts of your app.

---

### 6. Summary

You now have:

- A **Q&A box** with:
  - Markdown-friendly editor.
  - AI answer panel.
  - Threaded replies using `parent` and `previous`.
- An **extension system** with lifecycle hooks and state inheritance.
- A **Git-backed extension** that:
  - Creates commits per Q&A.
  - Creates branches for replies.
  - Lists files in the repo.

This design stays minimal, but is structured enough to grow into a robust, extensible system—very much in the spirit of small, well-packed libraries like Mistune or Anytree.
