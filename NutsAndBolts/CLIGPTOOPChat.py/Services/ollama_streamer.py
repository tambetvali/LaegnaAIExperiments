import json
from ollama import Client
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
# STREAMING OLLAMA CLIENT CLASS
# ------------------------------------------------------------
class OllamaBasicStreamer(AIService):
    def __init__(self, config_json: str, parent=None):
        self.cfg = config_json
        self.lazy = True # If asked for response, it would be lazy answer, thus it's kind of a "draft"

        self.model = self.cfg["model"]
        self.host = self.cfg.get("host", "http://localhost:11434")
        self.stream = self.cfg.get("stream", True)

        # Connect to local Ollama server
        self.client = Client(host=self.host)
        super().__init__(parent)

    def ask(self, question: str):
        """
        Streams the model's response using Python `yield`.
        Each yield returns a substring (token or chunk).
        """

        newstreamer = OllamaBasicStreamer(self.cfg, self)
        newstreamer.asked(question)

        return newstreamer

    # It should simply return the existing answer if called again, and add all the pieces coming before
    #   the call to start with a solid string. Currently, maybe it generates the answer again. TODO:
    def __call__(self):
        if not self.lazy:
            # Notice: thread management is nearly non-existing here, but it's not a big deal if it generates twice,
            #   because string has one or another value.
            return self.answer
        
        answer = ""

        # Stream the response
        for chunk in self.client.chat(
            model=self.model,
            messages=self.messagelist(),
            stream=self.stream
        ):
            if "message" in chunk and "content" in chunk["message"]:
                answer = answer + chunk["message"]["content"]
                yield chunk["message"]["content"]
        
        self.answer = answer
        self.answered(answer)
        self.lazy = False # Answer is registered and the function will not be lazy

class OllamaModelList:
    # Init with default config (your main models)
    def __init__(self):
        with open(filename("ollama_models.json"), 'r') as file:
            self.ollama_models_config_json = json.load(file)

    def models(self, verbose = False):
        client = Client(host=self.ollama_models_config_json.get("host"))

        models = client.list()

        if verbose:
            print("Installed Ollama models:")
            for m in models.get("models", []):
                print("-", m["model"])

        return models.get("models", [])

# ------------------------------------------------------------
# EXAMPLE USAGE (Q&A)
# ------------------------------------------------------------
if __name__ == "__main__":
    models = OllamaModelList()
    models.models(True)

    streamer = OllamaBasicStreamer(config_json)

    question = "Explain quantum entanglement in simple terms."

    print("Q:", question)
    print("A: ", end="", flush=True)

    # Stream the answer chunk-by-chunk
    for part in streamer.ask(question)():
        print(part, end="", flush=True)

    print()  # final newline
