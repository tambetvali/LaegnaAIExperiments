## Running the Snippet1Editor

You can run this project either in GitHub Codespaces or locally in VS Code. The flow is intentionally similar in both cases.

### Option 1: Run in GitHub Codespaces

1. **Open the repo in Codespaces**

   - Go to  
     `https://github.com/tambetvali/LaegnaAIExperiments`
   - Create a new Codespace on the `main` branch.
   - Once it opens, you’re effectively in a cloud VS Code environment.

2. **Install frontend dependencies**

   ```bash
   cd SnippetsCode/Snippet1Editor
   npm install @tiptap/core @tiptap/pm @tiptap/starter-kit
   ```

3. **Build the frontend with Vite**

   ```bash
   npm exec vite build
   ```

4. **Run the Flask app**

   ```bash
   flask run --host 0.0.0.0 --port 5000
   ```

5. **Open the app in the browser**

   - In Codespaces, VS Code will usually prompt:  
     “A service is available on port 5000. Open in browser.”  
     Accept that, or manually open the forwarded URL.
   - If no prompt appears, use the “Ports” panel in Codespaces and click the URL for port `5000`.

---

### Option 2: Run locally in VS Code

1. **Clone the repo**

   ```bash
   git clone https://github.com/tambetvali/LaegnaAIExperiments.git
   cd LaegnaAIExperiments/SnippetsCode/Snippet1Editor
   ```

2. **Install frontend dependencies**

   ```bash
   npm install @tiptap/core @tiptap/pm @tiptap/starter-kit
   ```

3. **Build the frontend**

   ```bash
   npm exec vite build
   ```

4. **Run Flask**

   ```bash
   flask run --host 0.0.0.0 --port 5000
   ```

5. **Open the app**

   Visit `http://127.0.0.1:5000` in your browser.

---

## How the app behaves

- **Left pane:** TipTap editor (WYSIWYG). Headings, paragraphs, etc. are rendered as rich text, not Markdown.
- **Submit button:** Sends both HTML and Markdown to the Flask backend.
- **Right pane:** Shows the server‑rendered HTML (via Mistune).
- **Markdown pane:** Shows syntax‑highlighted Markdown (via Pygments).

The editor **does not clear itself** on submit — we intentionally removed the line:

```js
// this.editor.commands.clearContent()
```

so the user’s text stays in place.

---

## Debugging tools and techniques

We used several layers of debugging to get from “nothing works” to a polished pipeline.

### Frontend build & bundling

- **Vite debug logging**

  ```bash
  DEBUG=vite:* npm exec vite build
  ```

  This showed:
  - Which config file was loaded (`vite.config.js`)
  - The resolved `rollupOptions.input`
  - That `frontend/main.js` was indeed the entry

- **Inspecting the built bundle**

  Opened `static/js/assets/main.js` and searched for:
  - `initApp`
  - `createEditor`
  - `StarterKit`
  - `Backbone`

  Early on, the bundle contained only ProseMirror internals (e.g. `function V(n){this.content=n}`), which told us our app code was being tree‑shaken away.

- **Tree‑shaking diagnosis**

  Rollup removed our entire app because nothing referenced `initApp`.

  Fix:

  ```js
  window.initApp = initApp
  ```

  This created a side effect, forcing Rollup to keep the code.

---

### Flask & Jinja

- **Template context errors**

  Error:

    ```
    'formatter' is undefined
    ```


Cause: `render_template()` stopped passing `formatter` after refactoring.

Fix:

```python
return render_template(
    "index.html",
    example_html=example_html,
    formatter=formatter,
)
```

- **Inspecting Markdown sent to the backend**

Temporary debug:

```python
print("MARKDOWN RECEIVED:")
print(repr(markdown_text))
```

This helped verify how HTML → Markdown conversion behaved.

---

### Browser‑side debugging

- **DevTools Console**

```js
window.initApp
```

Confirmed whether the function existed after bundling.

- **DevTools Network tab**

Verified that `/static/js/assets/main.js` loaded without 404 and matched the latest build.

---

## Short project history

This project started as a simple idea:  
**a TipTap‑powered Markdown workbench with a Flask backend.**

But the path to a polished version involved several tricky steps:

- Initial TipTap + Flask integration.
- Vite bundling introduced tree‑shaking issues.
- The bundle contained only ProseMirror internals.
- We discovered that `initApp` was exported but unused.
- Fix: attach it to `window`.
- TipTap showed `#` instead of headings — because it was initialized with Markdown, not HTML.
- Fix: initialize with HTML (`example_html`).
- Template broke because `formatter` was removed.
- Fix: restore it.
- UX refinement: remove editor clearing on submit.

### Who did what

- **Tambet (you):**
- Designed the architecture.
- Wrote the Flask app and templates.
- Ran all real builds and validated behavior.
- Persisted through the subtle Vite/Rollup issues.

- **Assistant:**
- Diagnosed tree‑shaking.
- Identified missing global assignment.
- Explained TipTap HTML initialization.
- Helped debug Jinja context issues.
- Provided debugging strategies and commands.

It took several iterations, deep inspection of the bundle, and careful reasoning to reach the current polished state.

---

## Useful debugging command

```bash
DEBUG=vite:* npm exec vite build
```

This prints Vite’s full internal reasoning and is invaluable when diagnosing bundling issues.
