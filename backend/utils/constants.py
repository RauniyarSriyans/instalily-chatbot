import os

# Parameters for OpenAI
openai_model = "gpt-3.5-turbo"
openai_temperature = float(os.environ.get("OPENAI_TEMPERATURE", "1"))
# openai_max_responses = 1
# open_ai_max_tokens = 512

models_dir = f"./out/models/"
parts_dir = f"./out/parts/"
