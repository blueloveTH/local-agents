from langchain.chat_models import init_chat_model
from langchain_huggingface import ChatHuggingFace, HuggingFacePipeline

model_path = './models/Qwen3-30B-A3B-Thinking-2507-FP8'

llm = HuggingFacePipeline.from_model_id(
    model_id=model_path,
    task="text-generation",
    device_map='cuda',
)
model = ChatHuggingFace(llm=llm)

messages = []
while True:
	prompt = input("User: ")
	messages.append({"role": "user", "content": prompt})
	print("AI: ", end='', flush=True)
	for chunk in model.stream(messages):
		print(chunk.content, end='', flush=True)
	messages.append({"role": "ai", "content": chunk.content})
	print()

# Use a pipeline as a high-level helper
# from transformers import pipeline, TextGenerationPipeline

# 

# pipe: TextGenerationPipeline = pipeline("text-generation", model=model_path, device_map='cuda')
# messages = [
#     {"role": "user", "content": "Who are you?"},
# ]
# pipe(messages)


# Load model directly
# from transformers import AutoTokenizer, AutoModelForCausalLM

# tokenizer = AutoTokenizer.from_pretrained(model_path)
# model = AutoModelForCausalLM.from_pretrained(model_path, device_map='cuda')
# messages = [
#     {"role": "user", "content": "Who are you?"},
# ]
# inputs = tokenizer.apply_chat_template(
# 	messages,
# 	add_generation_prompt=True,
# 	tokenize=True,
# 	return_dict=True,
# 	return_tensors="pt",
# ).to(model.device)

# outputs = model.generate(**inputs)
# print(tokenizer.decode(outputs[0][inputs["input_ids"].shape[-1]:]))


# set HF_ENDPOINT=https://hf-mirror.com
# huggingface-cli download --resume-download Qwen/Qwen3-30B-A3B-Thinking-2507-FP8 --local-dir models/Qwen3-30B-A3B-Thinking-2507-FP8
