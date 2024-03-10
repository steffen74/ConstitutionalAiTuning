import time
import random
import requests
import torch
import transformers
from transformers import pipeline
from transformers import AutoTokenizer
import openai
from typing import List, Dict, Any
from ConstitutionalAiTuning.prompting.prompt_template import PromptTemplate
from tqdm import tqdm

class ModelInteractor:
    def __init__(self, hf_model: str = None, hf_api_key: str = None, use_mock: bool = False):
        """
        Initialize the ModelInteractor with either a text generation pipeline, OpenAI API key and model, or API credentials, and an option to use mock responses.

        Args:
            hf_model (str): The name of the Hugging Face model.
            hf_api_key (str, optional): The token for the API authentication on the Hugging Face Hub. Defaults to None.
            use_mock (bool): If True, uses a mock function instead of the actual LLM for responses.
        """

        if hf_model is None :
            raise ValueError("hf_model must be provided")
        
        if hf_api_key is not None:
            self.hf_api_url = f"https://api-inference.huggingface.co/models/{hf_model}" 
            self.tokenizer = AutoTokenizer.from_pretrained(hf_model)
            self.text_gen_pipeline = None
        else:
            self.hf_api_url = None
            self.tokenizer = None
            self.text_gen_pipeline = pipeline(
                "text-generation",
                model=self.hf_model,
                torch_dtype=torch.bfloat16,
                device_map="auto",
            )

        self.hf_api_key = hf_api_key
        self.use_mock = use_mock

    def mock_execute_llm_request(self, prompt: str, **kwargs) -> str:
        """
        Mock method to simulate LLM responses.

        Args:
            prompt (str): The prompt to be sent to the mock LLM.

        Returns:
            str: A mock output.
        """
        prompt_str = str(prompt)
        if len(prompt_str) > 210:
            return f"Mock response for prompt: {prompt_str[:100]}...{prompt_str[-100:]}"
        else:
            return f"Mock response for prompt: {prompt_str}"

    def execute_llm_request(
        self,
        prompt: str,
        max_new_tokens: int = 256,
        do_sample: bool = True,
        temperature: float = 0.7,
        top_k: int = 50,
        top_p: float = 0.95
    ) -> str:
        """
        Executes a request to the LLM using the provided pipeline, OpenAI API, API, or a mock function based on the use_mock flag.

        Args:
            prompt (str): The prompt to be sent to the LLM.
            max_new_tokens (int): The maximum number of new tokens to generate. Default is 256.
            do_sample (bool): Whether to sample the output. Default is True.
            temperature (float): Sampling temperature. Default is 0.7.
            top_k (int): The number of highest probability vocabulary tokens to keep for top-k-filtering. Default is 50.
            top_p (float): Nucleus filtering (top-p) cumulative probability. Default is 0.95.

        Returns:
            str: The output generated by the LLM, OpenAI API, API, or the mock function.
        """
        if self.use_mock:
            return self.mock_execute_llm_request(prompt)

        if self.hf_api_key is None:
            chat_prompt = self.tokenizer.apply_chat_template(
                prompt, tokenize=False, add_generation_prompt=True
            )
            response = self.pipeline(
                chat_prompt,
                max_new_tokens=max_new_tokens,
                do_sample=do_sample,
                temperature=temperature,
                top_k=top_k,
                top_p=top_p,
            )
            generated_text = response.json()[0]["generated_text"]
            # remove the chat prompt from the generated text
            return generated_text[len(chat_prompt):]

        elif self.hf_api_key is not None:
            chat_prompt = self.tokenizer.apply_chat_template(
                prompt, tokenize=False, add_generation_prompt=True
            )
            payload = {
                "inputs": chat_prompt,
                "max_new_tokens": max_new_tokens,
                "do_sample": do_sample,
                "temperature": temperature,
                "top_k": top_k,
                "top_p": top_p,
            }
            headers = {"Authorization": f"Bearer {self.hf_api_key}"}
            response = requests.post(self.hf_api_url, headers=headers, json=payload)
            response.raise_for_status()
            generated_text = response.json()[0]["generated_text"]
            # remove the chat prompt from the generated text
            return generated_text[len(chat_prompt):]

        else:
            raise ValueError("Either pipeline, openai_api_key, or api_url and api_headers must be provided")


    def run_single_interaction(
        self, 
        prompts: List[Dict[str, Any]], 
        constitution_instructions: Dict[str, Any],
        prompt_index: int = None,
        verbose: bool = False
    ) -> Dict[str, Any]:
        """
        Runs a single interaction cycle (initial answer, critique, revision) 
        for a specified or randomly selected input prompt, with control over verbosity.
        Returns a dictionary with the interaction history.

        Args:
            prompts (list): A list of prompts.
            constitution_instructions (dict): Instructions for generating the prompts loaded from the constitution.
            prompt_index (int, optional): Index of the specific prompt to be used. If None, a random prompt is selected.
            verbose (bool): If True, prints the results and execution time. Defaults to True.

        Returns:
            dict: Dictionary containing the selected prompt and interaction history (initial answer, critique, revision).
        """
        # Select a specific or random prompt
        if prompt_index is not None and prompt_index < len(prompts):
            prompt = prompts[prompt_index]
        else:
            prompt = random.choice(prompts)

        cai_prompts = PromptTemplate(
            user_prompt=prompt["prompt"],
            constitution_instructions=constitution_instructions
        )

        # Process each stage (initial answer, critique, revision) and print if verbose is True
        for stage in ['initial_answer', 'critique', 'revision']:
            start_time = time.time()
            generated_prompt = getattr(cai_prompts, f'generate_{stage}_prompt')()
            response = self.execute_llm_request(generated_prompt)
            end_time = time.time()

            # Remove "Revision: " or "Critique: " from the beginning of the response
            response = response.replace("Revision: ", "").replace("Critique: ", "")

            setattr(cai_prompts, stage, response)

            if verbose:
                print("#############################################")
                print(f"{stage.replace('_', ' ').title()}:\n {response}")
                print("Time Taken:", end_time - start_time, "seconds\n")

        return cai_prompts.get_history()

    def run_interaction_loop(
        self, 
        prompts: List[Dict[str, Any]], 
        constitution_instructions: Dict[str, Any]
    ) -> List[Dict[str, Any]]:
        """
        Loops over prompts for generating answers, critiques, and revisions.
        Uses the run_single_interaction method for each prompt.

        Args:
            prompts (list): A list of prompts.
            constitution_instructions (dict): Instructions for generating the prompts loaded from the constitution.

        Returns:
            list: A list of dictionaries, each containing the prompt and interaction history (initial answer,     critique, revision).
        """
        sft_data = []

        for index, prompt in tqdm(enumerate(prompts), total=len(prompts)):
            # Use run_single_interaction for each prompt
            interaction_result = self.run_single_interaction(
                prompts, 
                constitution_instructions, 
                prompt_index=index, 
                verbose=False  # Set verbose to False to avoid printing during loop
            )
            sft_data.append(interaction_result)

        return sft_data
