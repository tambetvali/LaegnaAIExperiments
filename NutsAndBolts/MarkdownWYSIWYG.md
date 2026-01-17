# Guide to Markdown‑friendly WYSIWYG Editors

This guide explains how to choose, implement, and style WYSIWYG editors that work cleanly with Markdown. It also shows how to integrate AI‑generated Markdown, how to keep conversions stable, and where Mistune or Pygments can optionally run on the client or server.

---

# Finding Markdown‑aware WYSIWYG editors

There are two broad categories of editors that work well with Markdown workflows:

## 1. Editors that edit Markdown directly
These editors:

- Expose raw Markdown mode.
- Provide a visual mode that still maps cleanly to Markdown.
- Avoid hidden formatting.
- Support callbacks for syncing Markdown to your app.

They typically support headings, lists, links, images, and code blocks in a way that round‑trips cleanly.

## 2. Editors that edit HTML but map cleanly to Markdown
Many WYSIWYG editors are HTML‑first, but you can still use them if:

- They produce clean HTML.
- You restrict the toolbar to Markdown‑compatible features.
- You have a reliable HTML→Markdown converter.

This gives you a visual editor while still storing Markdown as the canonical format.

---

# Implementing WYSIWYG editors with live Markdown output

The core pattern:

1. User edits visually.
2. Editor fires a `change` event.
3. Your code converts the editor’s content to Markdown.
4. Markdown is stored as the canonical representation.
5. A preview pane renders Markdown → HTML.

You can do the conversion:

- **Client‑side** using JS libraries.
- **Server‑side** using Flask endpoints that call Mistune.

Backbone.js can act as the glue layer: models store Markdown, views wrap the editor, and events keep everything synchronized.

## Example flow (HTML‑based editor)

1. User edits in WYSIWYG (HTML).
2. Editor triggers `change`.
3. Backbone view:
   - Reads HTML.
   - Converts HTML→Markdown (client or server).
   - Updates the model’s `markdown`.
4. Preview updates automatically.

## Minimizing information loss

To keep conversions stable:

- Restrict features to those that map cleanly to Markdown:
  - Bold, italic, headings, lists, links, images, code.
- Avoid arbitrary fonts, colors, nested spans.
- Use a consistent Markdown dialect.
- Test round‑trips:
  - Markdown → HTML → Markdown should remain stable.

Mistune on the server can normalize Markdown and ensure consistent rendering.

---

# Implementing a Markdown text‑only box

A simple alternative is a plain Markdown textarea with a live preview.

### Pattern

1. Textarea for Markdown.
2. On input:
   - Client‑side: use a JS Markdown parser.
   - Or server‑side: send Markdown to Flask + Mistune.
3. Preview pane shows rendered HTML.

This avoids HTML→Markdown conversion entirely and guarantees no hidden formatting.

You can still use Pygments (server‑side or via Pyodide) to highlight fenced code blocks.

---

# Integrating AI answers as Markdown

AI responses are assumed to be Markdown. You can treat them as another content source.

### Flow

1. AI returns Markdown.
2. Backbone.js receives an event (e.g., `ai:answer`).
3. It updates:
   - An existing Markdown textarea, or
   - A new message model.

### Updating WYSIWYG editors

- For Markdown‑native editors:
  - Set the editor’s content directly to the AI Markdown.
- For HTML‑based editors:
  - Convert Markdown→HTML.
  - Insert into the editor.

Backbone keeps the model and views in sync.

---

# Making the WYSIWYG editor look like Markdown

You can style the editor so it visually resembles rendered Markdown—or make Markdown look like a simple comment box.

## Matching Markdown’s look

- Use CSS that mimics Markdown rendering.
- Keep heading sizes modest.
- Use simple list and blockquote styles.
- Use monospace fonts for code.

You can reuse the same CSS used for Mistune‑rendered HTML.

## Making it look like a comment/chat box

- Reduce heading sizes.
- Use subtle colors and minimal margins.
- Keep the toolbar small (bold, italic, code, links).

## Making it look like an article

- Larger headings.
- More spacing.
- Serif fonts.
- Optional table of contents.

The underlying Markdown/HTML can be identical; only CSS changes.

---

# Supporting skins, themes, and user‑defined styles

To support themes:

- Use CSS variables for colors, fonts, spacing.
- Let the surrounding page define:
  - `--editor-bg`, `--editor-fg`, `--editor-accent`, etc.
- Make the editor reference those variables.

This allows:

- Dark/light mode.
- User themes.
- Consistent styling between:
  - WYSIWYG editor
  - Markdown preview
  - Mistune‑rendered HTML

You can also provide built‑in themes (“chat”, “article”, “notebook”) and allow users to override them.

---

# Where Mistune and Pygments fit in

Even if the user hasn’t read the previous articles, you can still use these tools:

## Mistune
- Server‑side Markdown parser.
- Normalizes Markdown.
- Renders HTML.
- Can optionally run client‑side via Pyodide.

## Pygments
- Server‑side syntax highlighter.
- Can optionally run client‑side via Pyodide.
- Or replaced with JS highlighters (Prism.js, Highlight.js, Shiki) for live editing.

### Typical architecture

**Client:**
- WYSIWYG editor (HTML or Markdown).
- Optional JS Markdown parser.
- Optional JS syntax highlighter.

**Server (Flask + Python):**
- Mistune for canonical Markdown→HTML.
- Pygments for high‑quality code highlighting.
- Backbone.js communicates with Flask endpoints.

This gives you a Markdown‑centric WYSIWYG experience where:

- Users can edit visually or in raw Markdown.
- AI answers drop in as Markdown.
- The visual look can be tuned from “chatty textbox” to “full article”.
- Themes flow naturally from the surrounding page.

---

If you want, I can now generate:
- A version of this guide tailored for Moonlight Server  
- A combined architecture diagram  
- Or a starter implementation using Backbone.js + Flask  
