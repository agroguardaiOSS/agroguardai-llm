"""
Inference pipeline for AgroguardAI-LLM.

Loads a base model + LoRA adapter and answers farmer questions.
Supports interactive REPL and single-question CLI mode.

Usage:
    python src/inference.py                                    # interactive
    python src/inference.py --question "My tomato leaf get black spot"  # single shot
    python src/inference.py --base TinyLlama/TinyLlama-1.1B-Chat-v1.0  # switch model
"""

import argparse
import json
import os
import sys

from dotenv import load_dotenv

load_dotenv()

DEFAULT_BASE_MODEL = "meta-llama/Meta-Llama-3-8B-Instruct"
DEFAULT_ADAPTER = "models/agroguardai-lora-adapter"

SYSTEM_PROMPT = (
    "You are AgroguardAI, an agricultural assistant for smallholder farmers. "
    "You provide safe, evidence-based advice. When you lack information, "
    "you refuse to guess. You match the farmer's dialect and never recommend "
    "banned or dangerous products. Always cite your sources."
)


class AgroguardInference:
    """Wrapper around a base model + LoRA adapter for inference."""

    def __init__(
        self,
        base_model: str = DEFAULT_BASE_MODEL,
        adapter_path: str = DEFAULT_ADAPTER,
        load_in_4bit: bool = True,
        max_new_tokens: int = 512,
        temperature: float = 0.3,
        top_p: float = 0.9,
    ):
        self.max_new_tokens = max_new_tokens
        self.temperature = temperature
        self.top_p = top_p

        import torch
        from peft import PeftModel
        from transformers import AutoModelForCausalLM, AutoTokenizer, BitsAndBytesConfig

        tokenizer_id = base_model  # use same as model by default
        self.tokenizer = AutoTokenizer.from_pretrained(tokenizer_id)
        self.tokenizer.pad_token = self.tokenizer.eos_token or self.tokenizer.pad_token

        if load_in_4bit:
            bnb_config = BitsAndBytesConfig(
                load_in_4bit=True,
                bnb_4bit_compute_dtype=torch.bfloat16,
                bnb_4bit_quant_type="nf4",
                bnb_4bit_use_double_quant=True,
            )
        else:
            bnb_config = None

        base = AutoModelForCausalLM.from_pretrained(
            base_model,
            quantization_config=bnb_config,
            device_map="auto",
            torch_dtype=torch.bfloat16,
            trust_remote_code=True,
        )

        # Merge LoRA adapter
        if adapter_path and Path(adapter_path).exists():
            self.model = PeftModel.from_pretrained(base, adapter_path)
            self.model.eval()
            print(f"[✓] LoRA adapter loaded from {adapter_path}")
        else:
            self.model = base
            if adapter_path:
                print(f"[!] Adapter path {adapter_path} not found — using base model only")

    def _build_prompt(self, question: str, dialect: str = "", crop: str = "", region: str = "") -> str:
        """Build a chat-format prompt for inference."""
        parts = [f"<|system|>\n{SYSTEM_PROMPT}</s>\n"]

        instruction = f"A farmer asks the following question"
        if dialect:
            instruction += f" in {dialect}"
        if crop:
            instruction += f" about {crop}"
        if region:
            instruction += f" from {region}"
        instruction += ". Respond with safe, practical agronomic advice in the same dialect.\n\n"
        instruction += f"Farmer: {question}"

        parts.append(f"<|user|>\n{instruction}</s>\n")
        parts.append("<|assistant|>\n")
        return "".join(parts)

    def ask(self, question: str, dialect: str = "", crop: str = "", region: str = "") -> str:
        """Run inference on a single question."""
        prompt = self._build_prompt(question, dialect=dialect, crop=crop, region=region)
        inputs = self.tokenizer(prompt, return_tensors="pt").to(self.model.device)

        import torch
        with torch.no_grad():
            outputs = self.model.generate(
                **inputs,
                max_new_tokens=self.max_new_tokens,
                temperature=self.temperature,
                top_p=self.top_p,
                do_sample=True,
                pad_token_id=self.tokenizer.eos_token_id,
            )

        generated = self.tokenizer.decode(outputs[0], skip_special_tokens=True)
        # Return only the assistant's response (everything after the last <|assistant|>)
        if "<|assistant|>" in generated:
            return generated.split("<|assistant|>")[-1].strip()
        return generated[len(prompt):].strip()


def interactive_loop(inference: AgroguardInference):
    """Run an interactive REPL for asking farmer questions."""
    print("\n" + "=" * 60)
    print("  AgroguardAI-LLM Inference — type 'quit' to exit")
    print("=" * 60 + "\n")

    while True:
        try:
            question = input("Farmer > ").strip()
        except (EOFError, KeyboardInterrupt):
            print("\nGoodbye.")
            break

        if question.lower() in ("quit", "exit", "q"):
            print("Goodbye.")
            break
        if not question:
            continue

        answer = inference.ask(question)
        print(f"\nAgroguardAI > {answer}\n")


def main():
    parser = argparse.ArgumentParser(description="AgroguardAI-LLM Inference")
    parser.add_argument("--question", "-q", default="", help="Single question to answer")
    parser.add_argument("--base", default=DEFAULT_BASE_MODEL, help="Base model ID")
    parser.add_argument("--adapter", default=DEFAULT_ADAPTER, help="LoRA adapter path or Hub repo")
    parser.add_argument("--dialect", default="", help="Dialect of the question")
    parser.add_argument("--crop", default="", help="Crop being asked about")
    parser.add_argument("--region", default="", help="Region of the farmer")
    parser.add_argument("--no-4bit", action="store_true", help="Disable 4-bit quantization")
    parser.add_argument("--max-tokens", type=int, default=512)
    parser.add_argument("--temperature", type=float, default=0.3)
    args = parser.parse_args()

    inference = AgroguardInference(
        base_model=args.base,
        adapter_path=args.adapter,
        load_in_4bit=not args.no_4bit,
        max_new_tokens=args.max_tokens,
        temperature=args.temperature,
    )

    if args.question:
        answer = inference.ask(
            args.question,
            dialect=args.dialect,
            crop=args.crop,
            region=args.region,
        )
        print(answer)
    else:
        interactive_loop(inference)


if __name__ == "__main__":
    main()
