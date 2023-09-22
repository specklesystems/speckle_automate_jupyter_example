import os
import sys

import papermill as pm
from speckle_automate import AutomationContext, AutomationResult, AutomationStatus

if __name__ == "__main__":
    args = sys.argv[1:]

    # we need to pass in the token via an env var, the params cell is executed
    # automatically exposing the token in the output file
    token_env_var = "SPECKLE_TOKEN"

    speckle_token = os.environ.get(token_env_var) or args[2]

    os.environ[token_env_var] = speckle_token

    automation_run_data, function_inputs = args[0], args[1]

    automation_context = AutomationContext.initialize(
        automation_run_data, speckle_token
    )

    output_file = "function.output.ipynb"
    try:
        run_result = pm.execute_notebook(
            "function.ipynb",
            output_file,
            parameters={
                "automation_run_data": automation_run_data,
                "function_inputs": function_inputs,
                "token_env_var": token_env_var,
                "execute_function": True,
            },
        )

        # find the cell by its tag
        function_execution_cells = [
            c for c in run_result.cells if "function_execution" in c.metadata.tags
        ]

        # should have only found 1
        if len(function_execution_cells) != 1:
            msg = (
                "Expected 1 cell to have the tag `function_inputs`,"
                f" found {len(function_execution_cells)}"
            )
            raise ValueError(msg)
        automation_result = AutomationResult.model_validate_json(
            function_execution_cells[0].outputs[-1]["text"]
        )
        automation_context._automation_result = automation_result
        automation_context.store_file_result(output_file)
    except Exception as ex:
        automation_context.mark_run_failed(str(ex))
    finally:
        exit_code = (
            0 if automation_context.run_status == AutomationStatus.SUCCEEDED else 1
        )
        exit(exit_code)
