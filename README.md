# ConstitutionalAiTuning

## About

`ConstitutionalAiTuning` is a Python library designed to facilitate the fine-tuning of Large Language Models (LLMs) using the constitutional AI approach. This library provides tools for generating prompts for initial answers, critiques, and revisions, and includes utilities for managing different constitutions the LLM can be trained on.

## Features

- **Prompt Template Generation**: Generate structured prompts for model training and evaluation.
- **Constitution Loader**: Load and parse JSON files representing different constitutional setups.
- **Model Interaction**: Interface with the LLM to obtain initial answers, critiques, and revisions.
- **Fine-Tuning Utilities**: Tools to streamline the process of fine-tuning your LLM.

## Installation

To install `ConstitutionalAiTuning`, you can use the following pip command:

```bash
pip install git+https://github.com/steffen74/ConstitutionalAiTuning.git

```

## Usage

Here is a basic example of how to use `ConstitutionalAiTuning`:

```python
# Install transformers from source - only needed for versions <= v4.34
# pip install git+https://github.com/steffen74/ConstitutionalAiTuning.git
# pip install git+https://github.com/huggingface/transformers.git
# pip install accelerate

import os
from ConstitutionalAiTuning.constitution_loader import load_constitution
from ConstitutionalAiTuning.interaction import ModelInteractor
from ConstitutionalAiTuning.utils.data_utils import import_prompts_from_csv

HF_API_KEY = os.getenv('HF_API_KEY')

# Load a constitution file (see examples/educational_assistant.json for an example)
# Replace with the actual path to your constitution file
constitution = load_constitution('examples/constitutions/educational_assistant.json')

# Initialize the ModelInteractor with a model
# Provide the Hugging Face API key if you want to use the Hugging Face inference API of that model (it must exist)
# If you don't provide an API key, the model will be used locally
interactor = ModelInteractor(hf_model="HuggingFaceH4/zephyr-7b-beta", hf_api_key=HF_API_KEY)

# Import prompts from a CSV file
prompts = import_prompts_from_csv('examples/prompts/physics_and_history_questions_5-12.csv')

# Run a single interaction to get a revised response for the first prompt in the list
single_interaction_response = interactor.run_single_interaction(prompts, constitution, prompt_index=0)
single_interaction_response

# Run the interaction loop to get revised responses for all prompts
responses = interactor.run_interaction_loop(input_prompts, constitution)

# Display the responses from the interaction loop
    print("\n#############################################")
    print("user_prompt:\n", response["user_prompt"])
    print("initial_answer:\n", response["initial_answer"])
    print("critique_request:\n", response["critique_request"])
    print("critique:\n", response["critique"])
    print("revision_request:\n", response["revision_request"])
    print("revision:\n", response["revision"])
```

### Explanation

- **Pipeline Initialization**: We start by initializing a text generation pipeline from Hugging Face's Transformers. You can specify any model compatible with the text generation task.

- **Constitution Loading**: We load the constitution using `load_constitution`, which contains the instructions for generating prompts.

- **Prompt Generation**: An instance of `PromptTemplate` is created, and an initial answer prompt is generated.

- **Model Interactor**: We initialize the `ModelInteractor` class with the pipeline.

- **Execute Single Interaction Run**: Using the `run_single_interaction` method of `ModelInteractor`, we pass the user prompt to generate an initial answer, a critique, and a revised answer.

- **Interaction Loop**: Demonstrates how to use the `run_interaction_loop` method to process multiple prompts and generate initial answers, critiques, and revisions.

### Notes

- Make sure to replace `'path/to/constitution.json'` and the chosen model in the pipeline defition with the actual path to your constitution file and the model you intend to use.
- This example assumes that the necessary packages (`transformers`, etc.) are installed and that `constitution.json` is correctly formatted.
- The exact output and behavior will depend on the model used and the contents of the constitution instructions.

## Contributing

We welcome contributions to `ConstitutionalAiTuning`! Please read our [Contributing Guidelines](CONTRIBUTING.md) for information on how to get involved.

## License

`ConstitutionalAiTuning` is licensed under the [MIT License](LICENSE).

## Contact

For questions and feedback, please reach out to [steffen@opencampus.sh](mailto:steffen@opencampus.sh).
