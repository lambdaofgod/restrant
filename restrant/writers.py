import re
from urllib.parse import urlparse
from pathlib import Path


def make_schema_filename(code_loc):
    # TODO make this customizable using regex or something
    maybe_loc_path = Path(code_loc)
    if maybe_loc_path.expanduser().exists():
        prefix = maybe_loc_path.name
    else:
        parsed_url = urlparse(code_loc)
        prefix = parsed_url.path.replace("/", "-")
    return prefix.strip("-") + ".schema"


def extract_yaml_front_matter(contents):
    yaml_front_matter = None

    # Regex pattern to match YAML front matter
    yaml_pattern = r"```yaml\s*([\s\S]*?)```"

    match = re.search(yaml_pattern, contents)

    if match:
        yaml_front_matter = match.group(1)

    return yaml_front_matter


def write_contents(contents, url, file_output):
    if file_output:
        if type(file_output) is str:
            out_path = file_output
        else:
            out_path = make_schema_filename(url)
        with open(out_path, "w") as f:
            f.write(extract_yaml_front_matter(contents))
