# Before running this script:
# - Run modelselector to select a model from your configured list.
# - If you can not set up configured list, but have ollama running, run ollamaautomodelsjsonconf.py
#   to get a config file list template.
#
# This keeps this script rather simple to understand: basically, you can setup your model manually
# with model_select.json, which would be overwritten if you use model lists:
#
# Here is an example selection of model:
# {
#   "localname": "Run with Litellm", // convenient name for this instance
#   "provider": "ollama", // server type
#   "internalprovider": "litellm", // basically driver
#   "model": "llama3.2:1b", // model type
#   "host": "http://localhost:11434" // server / provider url
# }

from Services.service import AIService, initAIService
from Services.filename import filename
import json

# ------------------------------------------------------------
# JSON CONFIGURATION (stored in a json configuration file)
# ------------------------------------------------------------
with open(filename("model_select.json"), 'r') as file:
    config_json = json.load(file)

streamer = initAIService(config_json)

question = "I am a person who is sitting here."

print("Q:", question)
print("A: ", end="", flush=True)

streamer = streamer.ask(question)

for a in streamer():
    print(a, end="", flush=True)

print()  # final newline
