# ConstitutionalAiTuning

## About

`ConstitutionalAiTuning` is a Python library designed to facilitate the fine-tuning of Large Language Models (LLMs) using the constitutional AI approach. This library provides tools for generating prompts for initial answers, critiques, and revisions, and includes utilities for managing different constitutions the LLM can be trained on.

## Table of Contents

- [About](#about)
- [Installation](#installation)
- [Usage](#usage)
  - [Prompt Generation](#prompt-generation)
  - [ModelInteractor](#modelinteractor)
  - [Example](#example)
- [Contributing](#contributing)
- [License](#license)
- [Contact](#contact)

## Installation

You can install `ConstitutionalAiTuning` as follows:

```bash
pip install git+https://github.com/steffen74/ConstitutionalAiTuning.git

```

`ConstitutionalAiTuning` requires the following dependencies:

```bash
# Install transformers from source - only needed for versions <= v4.34
pip install git+https://github.com/huggingface/transformers.git
# Install accelerate
pip install accelerate
```

## Usage

### Prompt Generation

`ConstitutionalAiTuning` provides utilities for generating structured prompts for training data generation. The PromptTemplate class can be used to create prompts based on loaded constitutional principles.

### ModelInteractor

The `ModelInteractor` class is a central component of the library, responsible for interfacing with the LLM to obtain initial answers, critiques, and revisions for the generation of training data for instructional fine-tuning. For the generation of data for the human alignment training, it provides methods to obtain prefered answers from different generated answers.
Further, it provides methods for running single interactions as well as looping over multiple prompts.

### Example

Here's an example of how to use ConstitutionalAiTuning to generate improved answers for an intructional tuning of an LLM:

```python
# Install transformers from source - only needed for versions <= v4.34
# pip install git+https://github.com/steffen74/ConstitutionalAiTuning.git
# pip install git+https://github.com/huggingface/transformers.git
# pip install accelerate

import os
from ConstitutionalAiTuning.principles_loader import load_principles
from ConstitutionalAiTuning.interaction import ModelInteractor
from ConstitutionalAiTuning.utils.data_utils import import_prompts_from_csv

HF_API_KEY = os.getenv('HF_API_KEY')

# Import prompts from a CSV file
prompts = import_prompts_from_csv('examples/prompts/physics_and_history_questions_5-12.csv')

# Load a constitutional principles file
principles = load_principles('examples/principles/educational_assistant_short.json')

# Instatiate ModelInteractor for usage with the (free) Hugging Face Inference API:
interactor = ModelInteractor(hf_model="HuggingFaceH4/zephyr-7b-beta", hf_api_key=HF_API_KEY)

# Run loop to get improved answers for all prompts
responses = interactor.run_answer_improvement_loop(prompts, principles)

# Save training data with improved answers to a CSV file
interactor.save_prompts_and_revisions_to_csv(responses, 'examples/training_data/educational_assistant_sft.csv')

# For the first few prompts display the randomly selected critique and revision pairs,
# and the generated intitial answer, critique, and revision.
for response in responses[1:10]:
    print("\n#############################################")
    print("### user_prompt:\n", response["user_prompt"])
    print("### initial_answer:\n", response["initial_answer"])
    print("### critique_request:\n", response["critique_request"])
    print("### critique:\n", response["critique"])
    print("### revision_request:\n", response["revision_request"])
    print("### revision:\n", response["revision"])
```

This example demonstrates the following steps:

1. Import prompts from a CSV file using import_prompts_from_csv.
2. Load a constitutional principles file using load_principles.
3. Instantiate the ModelInteractor class with the desired model and Hugging Face API key.
4. Run the run_answer_improvement_loop method to generate improved answers for all prompts based on the loaded principles.
5. Save the generated training data with improved answers to a CSV file using save_prompts_and_revisions_to_csv.
6. Print the initial answer, critique, and revision for the first few prompts.

Note: This example uses the given example prompt and constititution files (`physics_and_history_questions_5-12.csv` and `educational_assistant_short.json`) that you might want to change according to your specific requirements. Additionally, you'll need to set the HF_API_KEY environment variable with your Hugging Face API key to use the free Inference API or a dedicated inference server that you setup on Hugging Face.

## Contributing

We welcome contributions to `ConstitutionalAiTuning`! Please read our [Contributing Guidelines](CONTRIBUTING.md) for information on how to get involved.

## License

`ConstitutionalAiTuning` is licensed under the [MIT License](LICENSE).

## Contact

For questions and feedback, please reach out to [steffen@opencampus.sh](mailto:steffen@opencampus.sh).
