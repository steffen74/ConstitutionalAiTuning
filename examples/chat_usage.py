import os
from ConstitutionalAiTuning.interaction import ModelInteractor

HF_API_KEY = os.getenv('HF_API_KEY')

system_message = "You are a tutor that always responds in the Socratic style. You *never* give the student the answer, but try to ask just the right question to help them learn to think for themselves. You should always tune your question to the interest & knowledge of the student, breaking down the problem into simpler parts until it's at just the right level for them.\nAlways ask just ONE question for each user message. DO NOT ask multiple questions at once."

# Initialize the ModelInteractor with a Hugging Face model and poyyibly a system message
# interactor = ModelInteractor(hf_model="HuggingFaceH4/zephyr-7b-beta", hf_api_key=HF_API_KEY, system_message=system_message)

interactor = ModelInteractor(hf_model="HuggingFaceH4/zephyr-7b-beta", hf_api_key=HF_API_KEY, endpoint_url="https://dl6sir63fshnm5rr.eu-west-1.aws.endpoints.huggingface.cloud", system_message=None)


# Start a new chat
user_prompt = "How come that rainbows exist?"
assistant_response = interactor.chat_with_model(user_prompt)
print(f"Assistant: {assistant_response}")

# Continue the chat
user_prompt = "Yes, I have seen it before. It has different colors."
assistant_response = interactor.chat_with_model(user_prompt)
print(f"Assistant: {assistant_response}")

