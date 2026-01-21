For installation manual, open [TUTORIAL.md](TUTORIAL.md). This is free code, which will create you markdown-aware WYSIWYG editor, which still runs on HTML itself: it will convert the result to Markdown *after* you edit it, on server side.
- **Notice**: this is initial version and we have to get through parsing all tags, because code blocks are not yet parsed; headers, bold, italic - general formatting already works.
- It's Creative Commons free code for everybody; sensibly, I can easily give more rights for my code if you lack ones.

# AI API — TipTap–Flask Markdown Workbench

This AI API defines the behaviour and structure of a **TipTap‑based WYSIWYG Markdown editor** embedded in a **Python Flask** application, using **Mistune** for Markdown parsing, **Pygments** for syntax highlighting, and **Backbone.js** for client‑side real‑time behaviour. The system follows a **model–view–controller (MVC)** paradigm and is designed so that the **API + Spec alone are sufficient for an AI to recreate or update the implementation**.

The application is a **single‑page workbench** served at the root path `/`, with:
- a **TipTap editor pane on the left** (WYSIWYG),
- a **rendered HTML preview pane on the right** (Mistune + HTML),
- a **visible intermediate Markdown pane below** (syntax highlighted with Pygments),
- and a **central “submit” button** (UTF‑8 arrow icon, styled via CSS, implemented as `<button>`).

The system supports:
- **round‑trip conversion**: TipTap HTML → Markdown (client) → Mistune HTML (server),
- **feature toggling** via a controller: enabling/disabling editor features,
- **content lifecycle**: user edits → submits → server responds with parsed content → right pane updates independently.

The AI must implement and maintain the following API surface and behaviours.

---

## AI API — 3B Model

This subsection defines a **simplified but fully functional** version of the system, suitable for a ~3B parameter model. The focus is on **clarity, minimal dependencies, and straightforward logic**, while still respecting the overall architecture.

### 1. Routes and Endpoints

**1.1. `GET /` — Main Page**

- **Purpose:** Serve the main HTML page containing:
  - Left TipTap editor pane.
  - Right HTML preview pane.
  - Lower Markdown pane.
  - Central submit button.
- **Response:** A single HTML template with:
  - Linked JS/CSS for TipTap, Backbone.js, and custom logic.
  - Inline or linked CSS for layout (two columns + lower pane).
  - A small example Markdown snippet preloaded into the editor.

**1.2. `POST /parse` — Parse WYSIWYG Content**

- **Input:** JSON body:
  - `{"html": "<p>...</p>"}` — the current HTML content from TipTap.
- **Processing:**
  - Convert HTML to Markdown (simple, deterministic mapping).
  - Parse Markdown with Mistune to HTML.
  - Highlight Markdown using Pygments (server‑side).
- **Output:** JSON:
  - `{"markdown": "...", "html": "...", "highlighted_markdown": "..."}`

---

### 2. MVC Structure

**2.1. Model**

- Represents the **current document state**:
  - `raw_html` — last HTML from TipTap.
  - `markdown` — intermediate Markdown.
  - `rendered_html` — Mistune‑generated HTML.
- Stored in memory per request; no persistence required for the 3B version.

**2.2. View**

- Single HTML template with:
  - **Left pane:** TipTap editor container.
  - **Right pane:** `<div id="rendered-output">` for Mistune HTML.
  - **Lower pane:** `<pre><code id="markdown-output">` for Markdown (Pygments‑styled).
  - **Submit button:** `<button id="submit-button">` with UTF‑8 arrow icon.
- Layout:
  - Left and right panes share a common vertical height.
  - The **taller of the two** determines the height of the shared area.
  - The lower Markdown pane is always visible below, expanding as needed.

**2.3. Controller**

- JavaScript controller (Backbone.js) responsible for:
  - Initializing TipTap with a **Markdown‑like schema** (bold, italic, code, headings, lists, blockquotes, code blocks with language).
  - Providing methods:
    - `setMarkdown(markdownString)`
    - `getMarkdown()`
    - `enableFeature(featureName)`
    - `disableFeature(featureName)`
  - Handling:
    - Click on submit button:
      - Get current HTML from TipTap.
      - Send `POST /parse` with `{html: ...}`.
      - Clear editor content after sending.
    - Receiving server response:
      - Update right pane with `html`.
      - Update lower pane with `highlighted_markdown`.

---

### 3. Editor Behaviour

**3.1. Feature Set**

- Bold, italic, headings, inline code, code blocks with language, lists, blockquotes.
- Syntax highlighting in code blocks (client‑side or via CSS classes).
- Free‑form writing: no enforced structure beyond Markdown semantics.

**3.2. Height Synchronization**

- On each update:
  - Measure left and right pane heights.
  - Set both to the **max height**.
  - Allow the lower pane to expand naturally below.

---

## AI API — Full‑Fledged Model

This subsection defines an **extended, more robust version** suitable for a larger, more capable model. It adds **extensibility, configuration, and future‑proofing** while remaining compatible with the 3B version.

### 1. Extended Routes

**1.1. `GET /config` — Editor Configuration**

- Returns JSON describing:
  - Enabled features.
  - Default Markdown content.
  - Theme (CSS class names).
  - Any custom Markdown tags or extensions.

**1.2. `POST /parse` — Same as 3B, plus:**

- Optional fields:
  - `{"html": "...", "options": {...}}`
- Options may include:
  - `strict_mode` (boolean).
  - `extensions` (list of enabled Mistune extensions).
  - `highlight_style` (Pygments style name).

---

### 2. Extended MVC

**2.1. Model**

- May include:
  - Session‑based document states.
  - Versioning (simple history).
  - Optional persistence (e.g., in memory or lightweight DB).

**2.2. View**

- Supports:
  - Multiple themes (dark/light).
  - Optional toolbar customization (show/hide buttons).
  - Optional status bar (e.g., word count, mode indicator).

**2.3. Controller**

- Adds:
  - Dynamic feature toggling based on `/config`.
  - Ability to load/save content via additional endpoints (e.g., `/load`, `/save`).
  - Hooks for AI‑assisted transformations (e.g., “rewrite section,” “summarize,” etc.) — not implemented here but reserved in API.

---

# AI API Exp — Intent and Compatibility

The intent of this API is:

- To define a **stable contract** between:
  - The Flask backend,
  - The TipTap editor frontend,
  - The Markdown/HTML transformation pipeline.
- To ensure that:
  - **Any future implementation** that respects this API can be dropped in without breaking existing workflows.
  - **Code can be regenerated** by an AI using only this API + Spec, even if the original code files are lost.
- To support:
  - **Backwards compatibility**: new features must not break existing routes or change response formats in incompatible ways.
  - **Minimal coupling**: the editor, parser, and controller are loosely coupled via JSON and DOM contracts.

The 3B model version focuses on **simplicity and determinism**, while the full‑fledged version focuses on **extensibility and configurability**. Both share the same core API shape.

---

# AI Spec — Implementation Details

This section provides the **implementation‑level description** that an AI (or human) can follow to recreate the system.

---

## AI Spec — 3B Model

### 1. Flask Backend

**1.1. Dependencies**

- `Flask` — web framework.
- `Mistune` — Markdown parser.
- `Pygments` — syntax highlighting.
- `Pygments.formatters.HtmlFormatter` — HTML formatter for code.
- Standard Python libraries.

**1.2. `GET /` Implementation**

- Render a template `index.html` with:
  - A `<div id="editor"></div>` for TipTap.
  - A `<div id="rendered-output"></div>` for Mistune HTML.
  - A `<pre><code id="markdown-output"></code></pre>` for Markdown.
  - A `<button id="submit-button">➜</button>` (UTF‑8 arrow).
- Inject an example Markdown string into the page (e.g., via a `<script>` tag or data attribute) to initialize the editor.

**1.3. `POST /parse` Implementation**

- Read JSON body: `data = request.get_json()`.
- Extract `html = data["html"]`.
- Convert HTML to Markdown:
  - Use a simple, deterministic mapping (e.g., a small HTML→Markdown converter or a custom function).
  - Ensure only standard tags are used: `<p>`, `<strong>`, `<em>`, `<code>`, `<pre><code class="language-x">`, `<ul>`, `<ol>`, `<li>`, `<blockquote>`, `<h1>`–`<h6>`.
- Parse Markdown with Mistune:
  - `markdown_html = mistune.markdown(markdown_text)`.
- Highlight Markdown with Pygments:
  - Use `HtmlFormatter` with a basic style.
  - Wrap the Markdown in `<pre><code>` with appropriate classes.
- Return JSON with:
  - `markdown`
  - `html` (from Mistune)
  - `highlighted_markdown`

---

### 2. Frontend — TipTap + Backbone.js

**2.1. TipTap Initialization**

- Create a TipTap editor instance bound to `#editor`.
- Enable:
  - Bold, italic, headings, lists, blockquotes, code, code blocks with language.
- Configure TipTap to:
  - Use a schema that maps directly to standard HTML tags.
  - Provide a method to get current HTML: `editor.getHTML()`.

**2.2. Backbone.js Controller**

- Define a Backbone view or controller that:
  - Binds to the main container.
  - On `click` of `#submit-button`:
    - Reads HTML from TipTap.
    - Sends `POST /parse` with JSON body.
    - Clears the editor content.
  - On server response:
    - Updates `#rendered-output` with `response.html`.
    - Updates `#markdown-output` with `response.highlighted_markdown`.
  - On each update:
    - Measures heights of left and right panes.
    - Sets both to the maximum height.

---

## AI Spec — Full‑Fledged Model

The full‑fledged model extends the 3B implementation with more structure and configurability.

### 1. Configuration

**1.1. `/config` Endpoint**

- Returns JSON like:
  ```json
  {
    "features": ["bold", "italic", "heading", "code", "code_block", "list", "blockquote"],
    "default_markdown": "# Hello\n\nThis is an example.",
    "theme": "light",
    "custom_tags": [],
    "highlight_style": "default"
  }
