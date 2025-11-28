import openai
from backend.app.services.openai_utils import acreate_with_summary_and_cache

# global patch: all ChatCompletion.acreate calls go through our wrapper
openai.ChatCompletion.acreate = acreate_with_summary_and_cache