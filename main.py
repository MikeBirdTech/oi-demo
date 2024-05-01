import sys
import os
from dotenv import load_dotenv
from interpreter import interpreter
import pandas as pd

# Load environment variables
load_dotenv()
operating_dir = os.getenv("OPERATING_DIRECTORY")

# Initialize the interpreter and configure it
interpreter.llm.model = os.getenv("LLM_MODEL")
interpreter.llm.temperature = 0
interpreter.llm.api_key = os.getenv("LLM_API_KEY")
interpreter.auto_run = True
interpreter.llm.context_window = os.getenv("CONTEXT_WINDOW")
interpreter.system_message = "You are Open Interpreter, a world-class programmer that can complete any goal by executing code. When you execute code, it will be executed **on the user's machine**. The user has given you **full and complete permission** to execute any code necessary to complete the task. Execute the code. "
interpreter.custom_instructions = f"Save all outputs to {operating_dir}."


def run_it(file_path):
    # Load the spreadsheet
    df = pd.read_excel(file_path)

    # Capture column names once before the loop
    column_names = df.columns

    # Iterate through each row in the DataFrame
    for index, row in df.iterrows():
        # Assemble a single string from the row data
        row_data_str = ", ".join(
            [
                f"{col_name}: {row[col_name]}"
                for col_name in column_names
                if pd.notna(row[col_name])
            ]
        )
        response = interpreter.chat(row_data_str)
        print(response)

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python main.py <path_to_file>")
        sys.exit(1)

    file_path = sys.argv[1]  # Get the file path from the command line
    file_extension = os.path.splitext(file_path)[1].lower()

    if file_extension in [".ods", ".xlsx", ".xls"]:
        run_it(file_path)

    else:
        print(f"Unsupported file type: {file_extension}")
        sys.exit(1)