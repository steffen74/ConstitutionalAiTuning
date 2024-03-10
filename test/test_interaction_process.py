import os
import torch
from transformers import pipeline
from ConstitutionalAiTuning.prompting import PromptTemplate
from ConstitutionalAiTuning.constitution_loader import load_constitution
from ConstitutionalAiTuning.interaction import ModelInteractor

from unittest.mock import Mock, patch

def test_interaction_process(questions):    
    # Setting the root directory of the project
    project_root = '/home/steffen/00_code/ConstitutionalAiTuning'

    # Initialize a mock text generation pipeline
    text_gen_pipeline = pipeline(
        "text-generation",
        model="HuggingFaceH4/zephyr-7b-beta",
        torch_dtype=torch.bfloat16,
        device_map="auto",
    )

    # Build the path to the constitution file
    constitution_file_path = os.path.join(project_root, 'examples/educational_assistant.json')

    # Load the constitution file
    constitution = load_constitution(constitution_file_path)

    # Initialize the ModelInteractor with the pipeline
    interactor = ModelInteractor(text_gen_pipeline, use_mock=True)

    # Run the interaction loop to get responses for each prompt
    for question in questions:
        # Create a PromptTemplate instance
        template = PromptTemplate(question=question["question"], constitution_instructions=constitution)

        # Generate initial answer
        question_prompt = template.generate_initial_answer_prompt()
        print("Generated Question Prompt:\n", question_prompt)
        initial_answer = interactor.execute_llm_request(question_prompt)
        print("\nInitial Answer:\n", initial_answer, "\n")

        # Generate critique
        critique_prompt = template.generate_critique_prompt()
        print("Generated Critique Prompt:\n", critique_prompt)
        critique = interactor.execute_llm_request(critique_prompt)
        print("\nCritique:\n", critique, "\n")

        # Generate revision
        revision_prompt = template.generate_revision_prompt()
        print("Generated Revision Prompt:\n", revision_prompt)
        revision = interactor.execute_llm_request(revision_prompt)
        print("\nRevision:", revision, "\n")

# Test input prompts
questions = [
    {
        "question": "This is a training question?",
    },
]

# Run the test function
test_interaction_process(questions)
