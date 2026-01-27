# DIAGRAMS.md — TipTap–Flask Markdown Workbench Architecture & UML

This document provides an architectural overview of the TipTap–Flask Markdown Workbench.  
All diagrams use **Mermaid**, compatible with GitHub’s renderer.

---

# 1. Introduction

## 1.1 Purpose
This document explains the structure, behavior, and intent of the system using diagrams and short narrative explanations.

## 1.2 Audience
- Architects  
- Programmers  
- Frontend engineers  
- Backend engineers  
- Non‑technical readers  

---

# 2. High‑Level Overview

The system is a **browser‑based Markdown workbench** backed by Flask:

- Left pane → TipTap rich‑text editor  
- Right pane → rendered HTML  
- Bottom pane → syntax‑highlighted Markdown  
- Backbone.js view coordinates UI and AJAX  
- Vite bundles frontend into `static/js/assets/main.js`  
- Flask serves UI and parses Markdown  

---

# 3. Project Structure Diagram

### Explanation
A map of the project’s folders and key files.

```mermaid
flowchart TD
  subgraph Root["project-root"]
    APP[app.py]
    REQ[requirements.txt]
    VITECFG[vite.config.js]

    subgraph Frontend["frontend"]
      MAINJS[main.js]
    end

    subgraph Static["static"]
      subgraph CSS["css"]
        STYLE[style.css]
      end
      subgraph JS["js"]
        subgraph Assets["assets"]
          BUNDLE[main.js - Vite bundle]
        end
      end
    end

    subgraph Templates["templates"]
      INDEX[index.html]
    end
  end

  VITECFG --> MAINJS
  MAINJS --> BUNDLE
  APP --> INDEX
  APP --> BUNDLE
  INDEX --> STYLE
```

---

# 4. Core Component Architecture

### Explanation
Shows the main runtime components and how they relate.

```mermaid
classDiagram
  class FlaskApp {
    +index()
    +parse()
    -markdown_parser
    -formatter
  }

  class IndexTemplate {
    +TipTap mount point
    +Pane layout
    +Loads JS bundle
    +Loads CSS
  }

  class AppView {
    -editor
    +initialize()
    +getMarkdown()
    +setMarkdown(md)
    +onSubmit()
    +localRender()
    +updateRightPane(html)
    +updateMarkdownPane(md)
    +syncHeights()
  }

  class TipTapEditor {
    -content
    +getHTML()
    +setContent()
  }

  class HtmlToMarkdown {
    +htmlToMarkdown(html)
  }

  class FlaskParser {
    +POST /parse
    -markdown_parser
    -highlight()
  }

  FlaskApp --> IndexTemplate : renders
  IndexTemplate --> AppView : instantiated
  AppView --> TipTapEditor : controls
  AppView --> HtmlToMarkdown : converts
  AppView --> FlaskParser : AJAX calls
  FlaskParser --> FlaskApp : internal
```

---

# 5. Behavioral Diagram

## 5.1 Sequence: Editing → Submitting → Rendering

```mermaid
sequenceDiagram
  actor User
  participant Browser as Browser - AppView and TipTap
  participant Editor as TipTap Editor
  participant Converter as HtmlToMarkdown
  participant Flask as Flask parse endpoint
  participant Parser as Markdown Parser

  User->>Editor: Type rich text
  Editor-->>Browser: getHTML()
  User->>Browser: Click Submit
  Browser->>Editor: getHTML()
  Editor-->>Browser: HTML content
  Browser->>Converter: htmlToMarkdown(HTML)
  Converter-->>Browser: Markdown
  Browser->>Flask: POST /parse
  Flask->>Parser: parse(markdown)
  Parser-->>Flask: html + highlighted md
  Flask-->>Browser: JSON response
  Browser->>Browser: update panes
  Browser-->>User: Updated HTML + Markdown
```

---

# 6. Deployment Diagram

```mermaid
flowchart LR
  subgraph UserMachine["User Machine"]
    BROWSER[Web Browser - TipTap and Backbone]
  end

  subgraph Server["Flask Server"]
    APP[app.py]
    TEMPLATE[index.html]
    STATICJS[main.js bundle]
    STATICCSS[style.css]
  end

  BROWSER -->|GET /| APP
  APP --> TEMPLATE
  APP --> STATICJS
  APP --> STATICCSS

  BROWSER -->|POST /parse| APP
  APP --> BROWSER
```

---

# 7. Summary

## 7.1 What This Architecture Achieves
- Clear separation of frontend and backend  
- Single‑page workbench with synchronized panes  
- Simple deployment  
- Extensible Markdown + HTML pipeline  

## 7.2 Why It Matters
A clean example of integrating TipTap, Backbone, Vite, and Flask into a cohesive editing environment.

---

# End of DIAGRAMS.md

# 🧠📐 TipTap–Flask Markdown Workbench  
## System Flow, Internals & Conceptual Model (with Diagrams)

This section explains **how the entire system thinks and moves** — not just how it runs.

It combines:
- Execution flow
- Framework internals (Flask, Backbone.js)
- UI cognition (TipTap)
- A *TikTok-style analogy* for understanding data flow & attention

---

## 1️⃣ Whole Process Flow (End-to-End)

```mermaid
flowchart LR
    User[User Types in TipTap]
    TipTap[TipTap Editor<br/>ProseMirror State]
    BB[Backbone View]
    MD[HTML → Markdown<br/>Converter]
    AJAX[AJAX POST /parse]
    Flask[Flask App]
    Mistune[Mistune Markdown Parser]
    Pygments[Pygments Highlighter]
    Response[JSON Response]
    UI[Update UI Panes]

    User --> TipTap
    TipTap --> BB
    BB --> MD
    MD --> AJAX
    AJAX --> Flask
    Flask --> Mistune
    Flask --> Pygments
    Mistune --> Response
    Pygments --> Response
    Response --> UI
```

**Key insight**  
This is a **round-trip cognitive loop**:
- TipTap holds *semantic intent*
- Markdown is the *canonical intermediate*
- Flask is the *authoritative interpreter*

---

## 2️⃣ Frontend Cognitive Stack (TipTap + Backbone.js)

```mermaid
flowchart TD
    DOM[DOM]
    Editor[TipTap Editor<br/>ProseMirror]
    State[Document State Tree]
    BBView[Backbone View]
    Events[DOM Events]
    Render[Manual Render Sync]

    DOM --> Editor
    Editor --> State
    State --> BBView
    Events --> BBView
    BBView --> Render
```

### Why Backbone.js still works beautifully here

Backbone acts as a **manual nervous system**:

- It does **not virtualize the DOM**
- It explicitly binds:
  ```js
  events: {
    'click #submit-button': 'onSubmit'
  }
  ```
- It coordinates *when* cognition happens

💡 This makes the system **debuggable, observable, and teachable** — ideal for AI-assisted reconstruction.

---

## 3️⃣ Flask Internal Processing Pipeline

```mermaid
sequenceDiagram
    participant C as Client (Browser)
    participant F as Flask
    participant M as Mistune
    participant P as Pygments

    C->>F: POST /parse {html, markdown}
    F->>M: parse(markdown)
    F->>P: highlight(markdown)
    M-->>F: rendered HTML
    P-->>F: highlighted markdown
    F-->>C: JSON {html, markdown, highlighted_markdown}
```

### Critical Flask lines (authority boundary)

```python
markdown_parser = mistune.create_markdown()

rendered_html = markdown_parser(markdown_text)

highlighted_markdown = highlight(
    markdown_text,
    MarkdownLexer(),
    formatter
)
```

🧠 **Interpretation**  
Flask is not just a server — it is the **semantic judge**.  
Frontend guesses; backend *decides*.

---

## 4️⃣ TipTap → Markdown Conversion (Lossy but Intent-Preserving)

```mermaid
flowchart LR
    ProseMirror[ProseMirror JSON Tree]
    HTML[Editor.getHTML()]
    Regex[Regex Rules]
    Markdown[Intermediate Markdown]

    ProseMirror --> HTML
    HTML --> Regex
    Regex --> Markdown
```

### Critical conversion line

```js
const html = this.editor.getHTML()
const markdown = htmlToMarkdown(html)
```

⚠️ This conversion is **intentionally simple**:
- Not a full AST transform
- Designed for *clarity over completeness*
- Ideal for inspection, learning, and extension

---

## 5️⃣ TikTok Analogy (Why This Architecture Works)

```mermaid
flowchart TB
    Creator[User / Creator]
    Draft[Draft Video<br/>(TipTap State)]
    Caption[Caption Text<br/>(Markdown)]
    Algorithm[TikTok Algorithm<br/>(Flask Parser)]
    Feed[Rendered Feed<br/>(HTML Output)]

    Creator --> Draft
    Draft --> Caption
    Caption --> Algorithm
    Algorithm --> Feed
```

**Mapping**:
- TipTap = recording studio
- Markdown = captions + metadata
- Flask = recommendation algorithm
- Rendered HTML = what the world sees

🎯 TikTok works because:
- Drafts are editable
- Interpretation is centralized
- Output is consistent

So does this system.

---

## 6️⃣ System Philosophy (Why This Is AI-Friendly)

- **One canonical format** (Markdown)
- **Explicit state transitions**
- **No hidden magic**
- **Rebuildable from text alone**

This document itself can:
- Recreate the filesystem
- Explain execution order
- Train an AI on system intent

---

## 🧩 Final Mental Model

```mermaid
graph LR
    Intent[Human Intent]
    Structure[Structured Editing]
    Text[Markdown Canon]
    Meaning[Parsed Meaning]
    Perception[Rendered View]

    Intent --> Structure
    Structure --> Text
    Text --> Meaning
    Meaning --> Perception
```

> *Markdown is not a format here — it is a **boundary of understanding***.

---

**End of system diagrams & explanation**
