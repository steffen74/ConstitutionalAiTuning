# Install transformers from source - only needed for versions <= v4.34
# pip install git+https://github.com/steffen74/principlesalAiTuning.git
# pip install git+https://github.com/huggingface/transformers.git
# pip install accelerate

import os
from ConstitutionalAiTuning.principles_loader import load_principles
from ConstitutionalAiTuning.interaction import ModelInteractor
from ConstitutionalAiTuning.utils.data_utils import import_prompts_from_csv

HF_API_KEY = os.getenv('HF_API_KEY')

# Load constitutional principles file
principles = load_principles('examples/principles/educational_assistant_short.json')

# Initialize the ModelInteractor with a Hugging Face model on a dedicated server
interactor = ModelInteractor(hf_model="HuggingFaceH4/zephyr-7b-beta", hf_api_key=HF_API_KEY, endpoint_url="https://m07124gncoa31nmm.eu-west-1.aws.endpoints.huggingface.cloud")
# To use the ModelInteractor with the free (but contrained) Hugging Face Inference API, use the following line instead:
# interactor = ModelInteractor(hf_model="HuggingFaceH4/zephyr-7b-beta", hf_api_key=HF_API_KEY)
# To run the ModelInteractor on a local machine, use the following line instead:
# interactor = ModelInteractor(hf_model="HuggingFaceH4/zephyr-7b-beta")

# Import prompts from a CSV file
prompts = import_prompts_from_csv('examples/prompts/physics_and_history_questions_5-12.csv')

# # Run a single comparison of generated answers for a selected prompt in the list
# single_comparison_response = interactor.run_single_comparison(prompts, principles, 13, verbose=True)
# single_comparison_response

# Run a loop to get answer comparisons data for alls prompts
responses = interactor.run_comparison_loop(prompts, principles)
interactor.save_comparison_data_to_csv(responses, 'examples/training_data/educational_assistant_dpo.csv')

# Display each initial user prompt, the texts of the randomly selected critique and revision pairs
# as well as the generated intitial answer, critique, and revision
for response in responses:
    print("\n#############################################")
    print("### user_prompt:\n", response["user_prompt"])
    print("### comparison_answer_1:\n", response["comparison_answer_1"])
    print("### comparison_answer_2:\n", response["comparison_answer_2"])
    print("### comparison_principle:\n", response["comparison_principle"])
    print("### chain_of_thought:\n", response["chain_of_thought"])
    print("### selected_answer:\n", response["selected_answer"])
