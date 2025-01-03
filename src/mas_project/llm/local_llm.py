import os

from crewai import LLM


MODEL_NAME = os.getenv("MODEL_NAME", "ollama/llama3.1")
MODEL_URL = os.getenv("MODEL_URL", "http://127.0.0.1:11434")
MDX_FILE = os.getenv("MDX_FILE", "emergency_01.mdx")

localLLM = LLM(model=MODEL_NAME, base_url=MODEL_URL, set_verbose=True)
