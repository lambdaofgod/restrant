import abc
import openai
from typing import List, Dict, Optional
import os
from pathlib import Path as P
import logging


class LMClient(abc.ABC):
    @abc.abstractmethod
    def generate(self, text: str, max_tokens=128, temperature=1, n=1, **kwargs):
        pass


class OpenAIClient(LMClient):
    def __init__(
        self,
        api_key_path: Optional[str],
        model_name: str = "gpt-3.5-turbo",
    ):
        self.model_name = model_name
        if api_key_path is None:
            api_key = os.getenv("openai_api_key")
            assert (
                api_key is not None
            ), "no api key path specified, failed loading api key from var"
        else:
            with open(P(api_key_path).expanduser()) as key_file:
                api_key = key_file.read().strip()
        openai.api_key = api_key
        logging.info(f"loaded OpenAI client for {model_name}")

    def generate(self, text, max_tokens=128, temperature=1, n=1, **kwargs):
        messages = [{"role": "user", "content": text}]
        return self.generate_impl(messages, max_tokens, temperature, n, **kwargs)

    def generate_impl(
        self,
        messages: List[Dict[str, str]],
        max_tokens: int = 128,
        # sampling temperature
        temperature: float = 1,
        # nucleus sampling arg
        top_p: int = 1,
        # n returned sequences
        n: int = 1,
        # penalizes already present tokens
        presence_penalty: float = 0,
        # penalizes token repetition
        frequency_penalty: float = 0,
        # can make some tokens less probable
        logit_bias: Dict[str, int] = dict(),
        stream: bool = False,
    ):
        completion = openai.ChatCompletion.create(
            model=self.model_name,
            messages=messages,
            max_tokens=max_tokens,
            temperature=temperature,
            top_p=top_p,
            n=n,
            presence_penalty=presence_penalty,
            frequency_penalty=frequency_penalty,
            logit_bias=logit_bias,
            stream=stream,
        )
        return completion["choices"][0]["message"]["content"]
