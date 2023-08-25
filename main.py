import os
import sys

import papermill as pm

if __name__ == "__main__":
    _, speckle_project_data, function_inputs, speckle_token = sys.argv

    # we need to pass in the token via an env var, the params cell is executed
    # automatically exposing the token in the output file
    token_env_var = "SPECKLE_TOKEN"

    os.environ[token_env_var] = speckle_token

    output_file = "function.output.ipynb"
    pm.execute_notebook(
        "function.ipynb",
        output_file,
        parameters={
            "speckle_project_data": speckle_project_data,
            "function_inputs": function_inputs,
            "token_env_var": token_env_var,
        },
    )
