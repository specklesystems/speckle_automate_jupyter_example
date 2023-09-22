"""
This module extracts the JSON schema from the FunctionInputs class the notebook.

WARNING: you probably should not be modifying this unless you know what you are doing.
"""
import json
from pathlib import Path

import papermill as pm


def save_schema_to_file(file_path: str):
    """
    Executes the notebook without valid input values.

    Its fine, since we're only interested in the result of the `function_inputs` cell.
    """
    notebook_path = "function.ipynb"
    run_result = pm.execute_notebook(notebook_path, "-")

    # find the cell by its tag
    function_inputs_cells = [
        c for c in run_result.cells if "function_inputs" in c.metadata.tags
    ]

    # should have only found 1
    if len(function_inputs_cells) != 1:
        msg = (
            "Expected 1 cell to have the tag `function_inputs`,"
            f" found {len(function_inputs_cells)}"
        )
        raise ValueError(msg)

    # parse and dump the schema to make sure its a valid json object
    schema = json.dumps(json.loads(function_inputs_cells[0].outputs[0].text))

    Path(file_path).write_text(schema)


if __name__ == "__main__":
    import sys

    _, file_path = sys.argv

    save_schema_to_file(file_path)
