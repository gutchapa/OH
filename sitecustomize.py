import openai
from backend.app.services.openai_utils import acreate_with_summary_and_cache

# global patch: all ChatCompletion.acreate calls go through our wrapper
openai.ChatCompletion.acreate = acreate_with_summary_and_cache

# --- Persistent Token Audit Initialization ---
from sdk.auditor import TokenAuditor
# Instantiate to load existing audit data
TokenAuditor()

# --- CrewAI Default Task Configuration ---
import os
from crewai import Task as _OrigTask
# Read defaults from environment, fallback to timeouts we use in code
_CHA_TASK_TIMEOUT = int(os.getenv("CREWAI_TASK_TIMEOUT", 60))
_CHA_MAX_RETRIES = int(os.getenv("CREWAI_MAX_RETRIES", 2))

class Task(_OrigTask):
    def __init__(self, *args, timeout=None, max_retries=None, **kwargs):
        # Apply defaults if not specified
        if timeout is None:
            timeout = _CHA_TASK_TIMEOUT
        if max_retries is None:
            max_retries = _CHA_MAX_RETRIES
        super().__init__(*args, timeout=timeout, max_retries=max_retries, **kwargs)

# Monkey-patch CrewAI Task class for all imports
import crewai
crewai.Task = Task
openai.ChatCompletion.acreate = acreate_with_summary_and_cache