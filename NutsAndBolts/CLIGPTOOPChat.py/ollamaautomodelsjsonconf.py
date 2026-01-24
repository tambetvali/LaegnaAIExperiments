# Ask ollama for it's full list of models: provide an example configuration file; if you want exactly
#   this list, rename the resulting ollama_models_gen.json into models_config.json, then run the model
#   selector to make one active default model selection into model_select.json. Then, run chat.py.

from Services.ollama_streamer import OllamaModelList
from Services.filename import filename

# Models is model list class
models = OllamaModelList()

# Models becomes it's output
models = models.models()

import json

# Data to be written as JSON
data = {
    "models": [
        
    ]
}

for m in models:
    data["models"].append({"localname": m["model"] + " with Ollama", "model": m["model"], "size": m["size"], "provider": "ollama", "internalprovider": "ollama", "stream": True})

# Open the model file and create an example for user, how to list all ollama's avaiable models.
with open(filename('ollama_models_gen.json'), 'w') as json_file:
    # Write data to the JSON file
    json.dump(data, json_file, indent=4)
