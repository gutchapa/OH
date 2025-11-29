import json
import os

class TokenAuditor:
    _instance = None
    AUDIT_FILE = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'token_audit.json')

    # GEMINI 2.0 FLASH PRICING (Per 1 Million Tokens)
    # Adjust these based on current Google Cloud pricing
    PRICE_INPUT_1M = 0.10   # $0.10 per 1M input tokens
    PRICE_OUTPUT_1M = 0.40  # $0.40 per 1M output tokens
    PRICE_CACHE_1M = 0.02   # $0.02 per 1M cached input tokens (Cheaper!)

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(TokenAuditor, cls).__new__(cls)
            cls._instance._load()
        return cls._instance

    def _load(self):
        if os.path.isfile(self.AUDIT_FILE):
            try:
                with open(self.AUDIT_FILE, 'r') as f:
                    data = json.load(f)
                self.total_input = data.get('total_input', 0)
                self.total_output = data.get('total_output', 0)
                self.total_cached = data.get('total_cached', 0)
                self.total_calls = data.get('total_calls', 0)
            except Exception:
                self.reset()
        else:
            self.reset()

    def _save(self):
        data = {
            'total_input': self.total_input,
            'total_output': self.total_output,
            'total_cached': self.total_cached,
            'total_calls': self.total_calls
        }
        try:
            with open(self.AUDIT_FILE, 'w') as f:
                json.dump(data, f)
        except Exception:
            pass

    def reset(self):
        self.total_input = 0
        self.total_output = 0
        self.total_cached = 0
        self.total_calls = 0
        self._save()

    def log_usage(self, usage_metadata):
        """
        Parses the raw Google GenAI usage object.
        """
        if not usage_metadata:
            return

        # Extract counts (Google SDK v1.0 standard fields)
        p_tokens = usage_metadata.prompt_token_count or 0
        c_tokens = usage_metadata.candidates_token_count or 0
        # cached_content_token_count might be in different spots depending on SDK version
        # We try to fetch it safely.
        cached_tokens = getattr(usage_metadata, 'total_token_count', 0) - (p_tokens + c_tokens)
        if cached_tokens < 0: cached_tokens = 0

        self.total_input += p_tokens
        self.total_output += c_tokens
        self.total_cached += cached_tokens
        self.total_calls += 1
        self._save()

    def generate_report(self):
        # Calculate Costs
        cost_input = (self.total_input / 1_000_000) * self.PRICE_INPUT_1M
        cost_output = (self.total_output / 1_000_000) * self.PRICE_OUTPUT_1M
        cost_cache = (self.total_cached / 1_000_000) * self.PRICE_CACHE_1M
        total_cost = cost_input + cost_output + cost_cache

        print("\n" + "="*40)
        print(" 🧾  TOKEN AUDIT REPORT (GEMINI 2.0) ")
        print("="*40)
        print(f" Total API Calls : {self.total_calls}")
        print("-" * 40)
        print(f" 📥 Input Tokens  : {self.total_input:,}  \t(${cost_input:.5f})")
        print(f" 💾 Cached Tokens : {self.total_cached:,}  \t(${cost_cache:.5f})")
        print(f" 📤 Output Tokens : {self.total_output:,}  \t(${cost_output:.5f})")
        print("-" * 40)
        print(f" 💰 ESTIMATED COST: ${total_cost:.5f}")
        print("="*40 + "\n")
    _instance = None
    
    # GEMINI 2.0 FLASH PRICING (Per 1 Million Tokens)
    # Adjust these based on current Google Cloud pricing
    PRICE_INPUT_1M = 0.10   # $0.10 per 1M input tokens
    PRICE_OUTPUT_1M = 0.40  # $0.40 per 1M output tokens
    PRICE_CACHE_1M = 0.02   # $0.02 per 1M cached input tokens (Cheaper!)

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(TokenAuditor, cls).__new__(cls)
            cls._instance.reset()
        return cls._instance

    def reset(self):
        self.total_input = 0
        self.total_output = 0
        self.total_cached = 0
        self.total_calls = 0

    def log_usage(self, usage_metadata):
        """
        Parses the raw Google GenAI usage object.
        """
        if not usage_metadata:
            return

        # Extract counts (Google SDK v1.0 standard fields)
        p_tokens = usage_metadata.prompt_token_count or 0
        c_tokens = usage_metadata.candidates_token_count or 0
        # cached_content_token_count might be in different spots depending on SDK version
        # We try to fetch it safely.
        cached_tokens = getattr(usage_metadata, 'total_token_count', 0) - (p_tokens + c_tokens)
        if cached_tokens < 0: cached_tokens = 0 

        self.total_input += p_tokens
        self.total_output += c_tokens
        self.total_cached += cached_tokens
        self.total_calls += 1

    def generate_report(self):
        # Calculate Costs
        cost_input = (self.total_input / 1_000_000) * self.PRICE_INPUT_1M
        cost_output = (self.total_output / 1_000_000) * self.PRICE_OUTPUT_1M
        cost_cache = (self.total_cached / 1_000_000) * self.PRICE_CACHE_1M
        total_cost = cost_input + cost_output + cost_cache

        print("\n" + "="*40)
        print(" 🧾  TOKEN AUDIT REPORT (GEMINI 2.0) ")
        print("="*40)
        print(f" Total API Calls : {self.total_calls}")
        print("-" * 40)
        print(f" 📥 Input Tokens  : {self.total_input:,}  \t(${cost_input:.5f})")
        print(f" 💾 Cached Tokens : {self.total_cached:,}  \t(${cost_cache:.5f})")
        print(f" 📤 Output Tokens : {self.total_output:,}  \t(${cost_output:.5f})")
        print("-" * 40)
        print(f" 💰 ESTIMATED COST: ${total_cost:.5f}")
        print("="*40 + "\n")