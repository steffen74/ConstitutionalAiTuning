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
constitution = load_constitution('examples/constitutions/educational_assistant_short.json')

# Initialize the ModelInteractor with a Hugging Face model
interactor = ModelInteractor(hf_model="HuggingFaceH4/zephyr-7b-beta", hf_api_key=HF_API_KEY)

# Import prompts from a CSV file
prompts = import_prompts_from_csv('examples/prompts/physics_and_history_questions_5-12.csv')

# # Run a single interaction with the first prompt in the list
# single_interaction_response = interactor.run_single_interaction(prompts, constitution, 13)
# single_interaction_response

# Run the interaction loop to get responses for each prompt
responses = interactor.run_interaction_loop(prompts[0:10], constitution)

# Display each initial user prompt, the texts of the randomly selected critique and revision pairs
# as well as the generated intitial answer, critique, and revision
for response in responses:
    print("\n#############################################")
    print("user_prompt:\n", response["user_prompt"])
    print("initial_answer:\n", response["initial_answer"])
    print("critique_request:\n", response["critique_request"])
    print("critique:\n", response["critique"])
    print("revision_request:\n", response["revision_request"])
    print("revision:\n", response["revision"])

