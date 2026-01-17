# Moonlight Server

Moonlight Server is a virtual filesystem and HTTP layer for “living” Markdown. It lets you treat a tree of `.md` and `.py.md` files as both:

- **Readable documentation** (Markdown-first, like Moon Notebook)
- **Executable Python code** (via extracted code blocks, using Mistune as the parser)

The core idea: a `.py.md` file behaves like a Python module—its code blocks are stitched together into a virtual `.py` file that tools and servers can use.

---

## Concept overview

### Virtual filesystem for Markdown and Python

**Idea:** You mount a directory as a “Moonlight filesystem”:

- **Normal files:**  
  - `.md` → served as Markdown (HTML in browser, raw in API).  
  - `.py` → served and executed as regular Python modules.
- **Hybrid files:**  
  - `.py.md` → treated as Markdown for humans, but also exposed as a virtual `.py` file for machines.

The virtual `.py` file is not necessarily written to disk. Instead, Moonlight Server:

1. Parses the `.py.md` with Mistune.
2. Extracts all Python code blocks.
3. Concatenates them into a single Python source string.
4. Exposes that string as if it were a file in a filesystem.

This lets you keep **all knowledge and code in Markdown**, but still run and import it like normal Python.

### Mistune as the Markdown engine

Mistune is a fast, extensible Markdown parser with plugin and renderer support, ideal for custom handling of code blocks.

- You feed it the `.md` content.
- You walk the parsed AST or use a custom renderer to capture:
  - **Code blocks with language `python`**
  - **Unlabelled code blocks** (optionally treated as Python)
- You then build a linear Python script from those blocks.

Because Mistune is pure Python and highly configurable, it fits well as the “compiler” from `.py.md` → virtual `.py` module.

### Coding Python inside Markdown

In a `.py.md` file, you write:

```markdown
# My experiment

Some explanation here.

```python
x = 2 + 2
print("x =", x)
```

More text.

```python
def square(n):
    return n * n
```
```

Moonlight Server will see this as a single Python program:

```python
# Block 1
x = 2 + 2
print("x =", x)

# Block 2
def square(n):
    return n * n
```

You can choose policies like:

- **Linear execution:** run blocks in order, sharing a single global namespace (like a notebook).
- **Module compilation:** treat the concatenated code as a module that can be imported.

---

## Using Moonlight Server as a base filesystem for Flask

### Virtual filesystem as a backend

You can design Moonlight Server as a Python object that implements a minimal filesystem-like API:

- **List directories:** return both real and virtual entries.
- **Read file:**  
  - If `path.endswith(".py.md")` and user asks for `.py` → generate Python source from Markdown.  
  - If `path.endswith(".md")` → return Markdown.  
  - If `path.endswith(".py")` → read from disk.

This virtual filesystem becomes the **backend** for:

- A Flask app that serves:
  - HTML-rendered Markdown.
  - Raw `.py` source (virtual or real).
  - JSON metadata about files, code blocks, etc.
- A CLI tool that:
  - Runs `.py.md` files.
  - Exports `.py` files.
  - Validates and lints code extracted from Markdown.

### Mixed `.py` and `.py.md` in one project

You can mix:

- `app.py` — regular Python.
- `notebooks/intro.py.md` — documented code.
- `services/user_service.py.md` — API logic with inline docs.
- `docs/architecture.md` — pure documentation.

The Flask server can:

- Serve `/docs/...` as rendered Markdown.
- Serve `/code/...` as `.py` (real or virtual).
- Import virtual modules from `.py.md` when running the app.

This way, **documentation and implementation live in the same tree**, but you don’t lose the ability to run, test, or deploy.

---

## Implementation guide

### Emulating a filesystem in Python

You don’t need a kernel-level filesystem. A **virtual filesystem layer** in Python is enough for most use cases:

- **Core abstraction:**

```python
class MoonlightFS:
    def listdir(self, path): ...
    def isfile(self, path): ...
    def read(self, path): ...
```

- **Behavior:**
  - For real files, delegate to `os` / `pathlib`.
  - For virtual `.py` files derived from `.py.md`, generate content on the fly.

You can then plug this into:

- Flask routes (e.g. `/fs/<path:subpath>`).
- A custom import hook (so `import my_notebook` loads from `.py.md`).
- A CLI runner.

#### Platform effects: Linux, Windows, macOS

Because this is **user-space emulation**, not a real mounted filesystem:

- **Linux / macOS / Windows:**
  - No special privileges needed.
  - Works anywhere Python runs.
  - Paths and separators differ, but you can normalize with `pathlib`.

If you want a real mount (e.g. FUSE):

- **Linux/macOS:** You can use FUSE-based libraries (like `fusepy`) to expose a real filesystem that shows `.py` files generated from `.py.md`.
- **Windows:** You’d need WinFSP or similar; more setup and permissions.

For many servers (especially shared or managed hosting), FUSE is not available. In that case:

- Keep the filesystem **virtual inside the app**.
- Expose files via HTTP endpoints or a download API.
- Let clients download the generated `.py` files if they need them.

#### Online servers (free/paid)

On platforms like:

- Free hosting (e.g. some PaaS, serverless functions).
- Paid managed servers.

You often can’t mount custom filesystems, but you can:

- Run Python.
- Serve HTTP responses.

So the pattern is:

- **Server-side:** Virtual filesystem in Python only.
- **Client-side:**  
  - A web UI that shows the virtual tree.  
  - “Download as `.py`” buttons that call an endpoint which returns the generated Python source.  
  - Optional ZIP export of the whole virtual tree.

This gives you the benefits of a virtual filesystem without needing OS-level integration.

---

## Detecting Python code blocks with Mistune

### Parsing code blocks

Mistune lets you parse Markdown into a structured representation and customize how code blocks are handled.

You can:

- Use a custom renderer that overrides `block_code(code, info)` (v0.x style) or the equivalent in v3.
- Or walk the AST and look for nodes representing fenced code blocks.

For each code block:

- **Labelled Python:**
  - `info` (or `lang`) is `"python"` or starts with `"python"`.
- **Unlabelled:**
  - `info` is `None` or empty.

### Heuristics for unlabelled blocks

You can choose a policy:

- **Strict:** Only treat ```python blocks as Python.
- **Lenient:** Treat unlabelled blocks as Python if:
  - They contain typical Python syntax (`def`, `class`, `import`, `:` at end of lines, etc.).
  - They don’t look like other languages (e.g. `console.log`, `<div>`, etc.).

This is heuristic, but good enough for many notebooks.

### Linear concatenation of code blocks

Once you’ve identified Python blocks:

1. Preserve their order in the document.
2. Optionally insert comments indicating origin:

```python
# --- Block 1 from intro.py.md: line 42 ---
x = 2 + 2
```

3. Concatenate them into a single string.

This gives you a **linear program** that reflects the narrative order of the Markdown file.

---

## Documentation + code: using Moonlight Server in practice

### Better documentation habits

With `.py.md`:

- **Narrative first:** You explain concepts in Markdown.
- **Code second:** You embed code blocks where they make sense.
- **Execution third:** Moonlight Server turns those blocks into runnable code.

This encourages:

- Clear explanations.
- Inline examples.
- Literate programming style.

### Simple APIs and shared context

Because all code blocks share a session (if you choose that model):

- You can define helper functions early.
- Reuse them in later blocks.
- Document each step in between.

Both the **Markdown browser** and the **Flask server** can operate on the same tree:

- Browser: renders `.md` and `.py.md` as HTML.
- Server: imports or executes the virtual `.py` modules extracted from `.py.md`.

This makes it easy to:

- Build small APIs where the implementation is fully documented.
- Share notebooks that are also deployable services.

### Git integration and collaboration

Markdown is:

- Diff-friendly.
- Merge-friendly.
- Easy to review.

Compared to JSON notebooks (like Jupyter), Markdown-based Moon Notebooks are much easier to version control and review.

With Moonlight Server:

- The **source of truth** is the `.md` / `.py.md` files.
- The generated `.py` files can be:
  - Ignored in Git (if they’re purely derived).
  - Or committed if you want reproducible builds.

Teams can:

- Review both documentation and code in one place.
- Comment on specific code blocks in PRs.
- Use standard Git workflows.

---

## Running `.py.md` files with a helper utility

### A simple runner

You can provide a CLI tool, e.g. `moonlight-run`:

1. Read `file.py.md`.
2. Use Mistune to extract Python code blocks.
3. Concatenate them into a script.
4. Execute with `exec` in a controlled namespace.

Example flow:

```bash
moonlight-run notebooks/experiment.py.md
```

Options:

- `--export experiment.py` — write the generated Python to disk.
- `--module` — run as if it were a module (set `__name__`, etc.).
- `--no-exec` — just validate and show the generated code.

### Import hook

You can also implement a custom import hook:

- When Python tries `import experiment`, your hook:
  - Looks for `experiment.py` and `experiment.py.md`.
  - If `.py.md` exists, parse and generate a module on the fly.
  - Cache the compiled code.

This makes `.py.md` feel like a first-class module type.

---

## Tracking which code block is running

This is where it gets interesting—and powerful.

### Static instrumentation

When generating the Python code from blocks, you can inject instrumentation:

- Before each block:

```python
__moonlight_enter_block(block_id=3)
```

- After each block:

```python
__moonlight_leave_block(block_id=3)
```

You define `__moonlight_enter_block` and `__moonlight_leave_block` in a runtime helper module.

This lets you:

- Track which block is currently executing.
- Build a **code traversal tree** (which blocks ran, in what order).
- Associate logs and outputs with specific blocks.

### Line-level debug points

You can go further and instrument lines:

- Insert calls like `__moonlight_line(block_id, line_no)` at strategic points.
- Or use `sys.settrace` to track line execution.

This gives you:

- A mapping from runtime behavior back to Markdown blocks and line numbers.
- The ability to show “live” execution markers in a web UI.

### Routing output to the current block

You can override `sys.stdout` and `sys.stderr` with a custom object that:

- Knows the current `block_id` (from `__moonlight_enter_block`).
- Buffers output per block.
- Sends output to:
  - The console.
  - A web socket.
  - A log store.

Then, in the browser:

- Each code block can show its own output area.
- When you re-run a block, its output updates.

This is very close to notebook behavior, but with Markdown as the source.

---

## Putting it all together

Here’s the full picture of Moonlight Server:

1. **Filesystem abstraction:**
   - A Python class that exposes a tree of files, including virtual `.py` files derived from `.py.md`.
2. **Markdown parsing:**
   - Mistune parses `.md` and `.py.md` files.
   - Python code blocks (labelled or inferred) are extracted and concatenated.
3. **Execution and import:**
   - A runner executes `.py.md` files.
   - An import hook lets you `import` them as modules.
4. **Flask integration:**
   - Flask serves:
     - Rendered Markdown.
     - Virtual `.py` files.
     - Metadata about blocks and execution.
5. **Instrumentation:**
   - Generated code is instrumented to:
     - Track which block is running.
     - Capture output per block.
     - Build a traversal tree.
6. **User experience:**
   - Users organize everything in a Markdown tree:
     - Docs, tasks, hints, code, experiments.
   - They get:
     - A notebook-like experience.
     - A real Python codebase.
     - Clean Git history.
     - Easy sharing and open-sourcing.

---

## Benefits and bottlenecks

### Benefits

- **Single source of truth:** Docs and code live together.
- **Readable forever:** Markdown is simple, durable, and tool-agnostic.
- **Git-friendly:** Clean diffs, easy reviews.
- **AI-friendly:** Markdown is great for feeding into AI tools for refactoring, explanation, and search.
- **Flexible deployment:** Works as:
  - A local tool.
  - A Flask-based web app.
  - A backend for other services.

### Bottlenecks and trade-offs

- **Parsing overhead:** Large `.py.md` files require parsing and concatenation; caching is important.
- **Heuristics for unlabelled blocks:** Misclassification can happen; you may need conventions or linting.
- **Debugging complexity:** Instrumented code is more complex than raw Python; stack traces need mapping back to Markdown.
- **Tooling integration:** IDEs and linters don’t natively understand `.py.md`; you’ll need export or language server tricks.
- **Security:** Executing arbitrary Markdown-embedded code requires trust models and sandboxing.

---

If you want, I can now generate a **MoonlightServer.md** file structure, a **starter implementation**, or a **folder layout** for the repo.
