import json
from litellm import completion
if __name__ == "__main__" or "servicesrelative" not in globals(): servicesrelative = __name__ == "__main__"
if servicesrelative:
    # If you run the script directly, services are in the same folder.
    from service import AIService
    from filename import filename
else:
    # If you run the parent script, this folder forms a subpackage.
    from Services.service import AIService
    from Services.filename import filename

# ------------------------------------------------------------
# JSON CONFIGURATION (stored in a json configuration file)
# ------------------------------------------------------------
with open(filename("model_select.json"), 'r') as file:
    config_json = json.load(file)

# ------------------------------------------------------------
# STREAMING LITELLM CLIENT CLASS
# ------------------------------------------------------------
class LitellmBasicStreamer(AIService):
    def __init__(self, config_json: str, parent=None):
        self.cfg = config_json
        self.lazy = True # If asked for response, it would be lazy answer, thus it's kind of a "draft"

        self.model = self.cfg["model"]
        self.host = self.cfg.get("host", "http://localhost:11434")
        self.stream = self.cfg.get("stream", True)
        super().__init__(parent)

    def ask(self, question: str):
        """
        Streams the model's response using Python `yield`.
        Each yield returns a substring (token or chunk).
        """

        newstreamer = LitellmBasicStreamer(self.cfg, self)
        newstreamer.asked(question)

        return newstreamer

    def __call__(self):
        if not self.lazy:
            # Notice: thread management is nearly non-existing here, but it's not a big deal if it generates twice,
            #   because string has one or another value.
            return self.answer

        answer = ""
        
        response = completion(
            model="ollama/"+self.model, 
            messages=self.messagelist(), 
            api_base=self.host,
            stream=True
        )

        for chunk in response:
            content = chunk['choices'][0]['delta']['content']

            if content is None:
                continue

            answer = answer + content
            yield content

        self.answer = answer
        self.answered(answer)
        self.lazy = False # Answer is registered and the function will not be lazy

# ------------------------------------------------------------
# EXAMPLE USAGE (Q&A)
# ------------------------------------------------------------
if __name__ == "__main__":
    streamer = LitellmBasicStreamer(config_json)

    question = "Explain quantum entanglement in simple terms."

    print("Q:", question)
    print("A: ", end="", flush=True)

    # Stream the answer chunk-by-chunk
    for part in streamer.ask(question)():
        print(part, end="", flush=True)

    print()  # final newline
