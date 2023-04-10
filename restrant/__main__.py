import fire
from pydantic import BaseModel, Field
from pathlib import Path
import logging
from typing import Union
import restrant
from restrant.loaders import load_code
from restrant import clients, writers


def load_from_file_if_path_exists(str_or_path, meta=""):
    p = Path(str_or_path)
    if p.expanduser().exists():
        logging.info(f"loading {meta} from {str_or_path}")
        with open(p) as f:
            return f.read()
    else:
        return str_or_path


class SpecPrompt(BaseModel):

    prompt_text: str = Field(default=restrant.Defaults.spec_prompt)


def get_lm_client(model_name, **kwargs):
    assert "api_key_path" in kwargs.keys(), "need api key path to use OpenAI"
    client = clients.OpenAIClient(kwargs["api_key_path"], model_name)
    return client


class Main:
    def get_openapi_spec(
        self,
        code_loc,
        max_tokens=1024,
        prompt_or_path=restrant.Defaults.spec_prompt,
        model_name="gpt-3.5-turbo",
        file_output: Union[bool, str] = True,
        **kwargs,
    ):

        prompt_template = load_from_file_if_path_exists(prompt_or_path)

        code = load_code(code_loc)
        prompt = prompt_template.format(code)
        logging.info("asking {client}")
        logging.info("prompt: {prompt}")
        client = get_lm_client(model_name, **kwargs)
        client_response = client.generate(prompt, max_tokens)
        writers.write_contents(client_response, code_loc, file_output)


if __name__ == "__main__":
    fire.Fire(Main())
