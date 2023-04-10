class Defaults:

    spec_prompt = (
        "given the following REST server code write its OpenAPI schema.\n"
        + "Enclose the schema in markdown code block that opens with ```yaml.:\n{}"
    )

    make_client_prompt = (
        "given the following OpenAPI specification\n"
        + "write a client {} and an example of request made using this client\n"
        + "specification:\n{}"
    )
