# Streamers basically stream the content from underlying AI, kind of token by token, and use
# python-convenient "yield" to pass the function output as if it was a stream. You catch this
# with "for" or "while" cycle, adding the string pieces together. "service.py" is a general
# streamer from which those specific streamers are deriven, so you mostly think you work with
# an AIService class instance as your server connection. This turns some typical uses into abstract
# terms and enables object oriented / imperative use.

class AIService:
    def __init__(self, parent=None):
        self.parent = parent
        self.messages = []

    # This gives all the indexed messages from parent Q&A until this one, in historic order of
    # creation of new messages.
    def inheritmessagelist(self):
        # Send all the messages of parent cue
        if self.parent != None:
            for msg in self.parent.inheritmessagelist():
                yield msg
        
        # Send all the messages for this request
        for msg in self.messages:
            yield msg

    def messagelist(self):
        # All the questions asked from the parents, with answers
        messages = list(self.inheritmessagelist())

        return messages

    # Message is registered either to list or dictionary of special positions
    #   "local" can be used to show the message only if it's part of the current Q&A, not if it's
    #   the history - I added this stub because there are several ways to implement this, but it's
    #   hard to understand context without placeholder. I removed more advanced functionality.
    def register_message(self, role, content, local = False):
        if content == None:
            return
        
        appendix = {"role": role, "content": content}

        self.messages.append(appendix)
    
    def asked(self, question, local = False):
        self.register_message("user", question, local)

    def answered(self, answer, local = False):
        self.register_message("assistant", answer, local)

    def commanded(self, answer, local = False):
        self.register_message("system", answer, local)
    
# TODO: here you need to register your models, to use the engironment variable, by their internal
#       provider: framework which is locally used.
#
# MAYDO: make Requirements.txt somehow depend on model selection, because these are large libraries,
#        and emulate Ollama's "run" behaviour to install model; altough this is not fully offline mode
#        and you can handle most of it by installer or packager, since hacker has at least some space
#        for non-production tools. I personally like offline mode and not depending on additional factor.

def initAIService(modelconf):
    # We must not call these imports from inside the initialization cycle, but this already
    # initializes an AI. We can not run litellm_streamer.py directly, for example, if we place
    # these imports into the header.

    # This is best connection to your local ollama interface, handling the specifics.
    if __name__ == "__main__" or "servicesrelative" not in globals(): servicesrelative = __name__ == "__main__"
    if servicesrelative: from ollama_streamer import OllamaBasicStreamer
    else: from Services.ollama_streamer import OllamaBasicStreamer

    # This is general connector, for example you can use it for CoPilot, ChatGPT or even still Ollama.
    if servicesrelative: from litellm_streamer import LitellmBasicStreamer
    else: from Services.litellm_streamer import LitellmBasicStreamer

    if modelconf["internalprovider"] == "ollama":
        environment = "ollama"
        return OllamaBasicStreamer(modelconf)
    elif modelconf["internalprovider"] == "litellm":
        environment = "litllm"
        return LitellmBasicStreamer(modelconf)