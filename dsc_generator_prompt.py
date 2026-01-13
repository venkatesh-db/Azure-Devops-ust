# Python script for automating PowerShell DSC template generation using OpenAI API

from openai import OpenAI
import os

# Initialize OpenAI client
client = OpenAI()   # reads OPENAI_API_KEY from env

def generate_dsc_template(prompt: str) -> str:
    """
    Generate PowerShell DSC template using OpenAI Responses API
    """
    try:
        response = client.responses.create(
            model="gpt-4.1-mini",
            input=prompt,
            max_output_tokens=1500
        )
        return response.output_text.strip()
    except Exception as e:
        raise RuntimeError(f"Error generating DSC template: {e}")

def save_dsc_to_file(dsc_template: str, filename: str = "dsc_template.ps1") -> None:
    """
    Save the generated DSC template to a file
    """
    try:
        with open(filename, "w", encoding="utf-8") as file:
            file.write(dsc_template)
        print(f"\nDSC template saved as {filename}")
    except Exception as e:
        raise RuntimeError(f"Error saving DSC template to file: {e}")

def main():
    """
    Main function to generate and save DSC template
    """
    # Step 1: Define the prompt for DSC generation
    prompt = (
        "Generate a PowerShell Desired State Configuration (DSC) template for deploying a web server. "
        "Include IIS installation, firewall rules, and deployment of a sample website."
    )

    # Step 2: Use OpenAI API to generate the DSC template
    print("===== Generating DSC Template =====")
    try:
        dsc_template = generate_dsc_template(prompt)
    except RuntimeError as e:
        print(e)
        return

    # Step 3: Print the generated DSC template to the console
    print("===== Generated DSC Template =====\n")
    print(dsc_template)

    # Step 4: Save the generated DSC template to a file
    try:
        save_dsc_to_file(dsc_template)
    except RuntimeError as e:
        print(e)

if __name__ == "__main__":
    # Validation Rule: Ensure the OpenAI API key is set in the environment
    if not os.getenv("OPENAI_API_KEY"):
        print("Error: OPENAI_API_KEY is not set in the environment.")
    else:
        main()