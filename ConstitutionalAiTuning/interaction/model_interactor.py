import transformers
from typing import List, Dict, Any
from ConstitutionalAiTuning.prompting.prompt_template import PromptTemplate

class ModelInteractor:
    def __init__(self, pipeline: transformers.pipelines.text_generation.TextGenerationPipeline):
        """
        Initialize the ModelInteractor with a text generation pipeline.

        Args:
            pipeline (transformers.pipelines.text_generation.TextGenerationPipeline): 
                A pipeline for text generation.
        """
        if not isinstance(pipeline, transformers.pipelines.text_generation.TextGenerationPipeline):
            raise TypeError("pipeline must be an instance of transformers.pipelines.text_generation.TextGenerationPipeline")
        self.pipeline = pipeline

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
        Executes a request to the LLM using the provided pipeline.

        Args:
            prompt (str): The prompt to be sent to the LLM.
            max_new_tokens (int): The maximum number of new tokens to generate. Default is 256.
            do_sample (bool): Whether to sample the output. Default is True.
            temperature (float): Sampling temperature. Default is 0.7.
            top_k (int): The number of highest probability vocabulary tokens to keep for top-k-filtering. Default is 50.
            top_p (float): Nucleus filtering (top-p) cumulative probability. Default is 0.95.

        Returns:
            str: The output generated by the LLM.
        """
        chat_prompt = self.pipeline.tokenizer.apply_chat_template(
            prompt, tokenize=False, add_generation_prompt=True
        )

        outputs = self.pipeline(
            chat_prompt,
            max_new_tokens=max_new_tokens,
            do_sample=do_sample,
            temperature=temperature,
            top_k=top_k,
            top_p=top_p,
            return_full_text=False
        )
        return outputs[0]["generated_text"]

    def run_interaction_loop(
        self, 
        input_prompts: List[Dict[str, Any]], 
        constitution_settings: Dict[str, Any]
    ) -> List[Dict[str, Any]]:
        """
        Loops over prompts for generating answers, critiques, and revisions.

        Args:
            input_prompts (list): A list of input prompts.
            constitution_settings (dict): Settings loaded from the constitution.

        Returns:
            list: A list of prompts with given input prompts, generated initial answers, selected critique request, critiques, selected revision request, and revisions.
        """
        sft_data = []

        for prompt in input_prompts:
            cai_prompts = PromptTemplate(
                input=prompt["input_prompt"],
                prompt_instructions=constitution_settings
            )

            # Generate and execute prompts
            initial_answer_prompt = cai_prompts.generate_initial_answer_prompt()
            cai_prompts.initial_answer = self.execute_llm_request(initial_answer_prompt)

            critique_prompt = cai_prompts.generate_critique_prompt()
            cai_prompts.critique = self.execute_llm_request(critique_prompt)

            revision_prompt = cai_prompts.generate_revision_prompt()
            cai_prompts.revision = self.execute_llm_request(revision_prompt)

            sft_data.append(cai_prompts.get_history())

        return sft_data