import os
from ConstitutionalAiTuning.principles_loader import load_principles
from ConstitutionalAiTuning.interaction import ModelInteractor
from ConstitutionalAiTuning.utils.data_utils import import_prompts_from_csv

HF_API_KEY = os.getenv('HF_API_KEY')

# Load a constitutional principles file
constitution = load_principles('examples/principles/educational_assistant_short.json')

# Initialize the ModelInteractor with a Hugging Face model on a dedicated server
interactor = ModelInteractor(hf_model="HuggingFaceH4/zephyr-7b-beta", hf_api_key=HF_API_KEY, endpoint_url="https://m07124gncoa31nmm.eu-west-1.aws.endpoints.huggingface.cloud")
# To use the ModelInteractor with the free (but contrained) Hugging Face Inference API, use the following line instead:
# interactor = ModelInteractor(hf_model="HuggingFaceH4/zephyr-7b-beta", hf_api_key=HF_API_KEY)
# To run the ModelInteractor on a local machine, use the following line instead:
# interactor = ModelInteractor(hf_model="HuggingFaceH4/zephyr-7b-beta")

# Import prompts from a CSV file
prompts = import_prompts_from_csv('examples/prompts/physics_and_history_questions_5-12.csv')

# Run a single answer improvement with a selected prompt in the list to test the generation of revised answers
single_interaction_response = interactor.run_single_answer_improvement(prompts, constitution, 13)
single_interaction_response

# Run a loop to get revised answers for all prompts
responses = interactor.run_answer_improvement_loop(prompts, constitution)
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
