from flask import Flask, render_template, request, jsonify
import mistune
from pygments import highlight
from pygments.lexers import MarkdownLexer
from pygments.formatters import HtmlFormatter

app = Flask(__name__)

markdown_parser = mistune.create_markdown()
formatter = HtmlFormatter(cssclass="codehilite", nowrap=False)


@app.route("/", methods=["GET"])
def index():
    example_markdown = """# TipTap–Flask Markdown Workbench

Type on the left, press the arrow button,
and see the parsed result on the right.

```python
def hello():
    print("Hello, world!")
```
"""
    return render_template("index.html", example_markdown=example_markdown, formatter=formatter)

@app.route("/parse", methods=["POST"])
def parse():
    data = request.get_json(force=True)
    html = data.get("html", "")

    markdown_text = data.get("markdown", "").strip()

    if not markdown_text:
        markdown_text = "_(No markdown provided by client)_"

    rendered_html = markdown_parser(markdown_text)

    highlighted_markdown = highlight(
        markdown_text,
        MarkdownLexer(),
        formatter
    )

    return jsonify(
        {
            "markdown": markdown_text,
            "html": rendered_html,
            "highlighted_markdown": highlighted_markdown,
        }
    )


if __name__ == "__main__":
    app.run(debug=True)
