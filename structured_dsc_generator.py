from openai import OpenAI
import json

# Initialize OpenAI client
client = OpenAI()   # reads OPENAI_API_KEY from env

def generate_dsc_template(prompt: str) -> str:
    """
    Generate PowerShell DSC template using OpenAI Responses API
    """

    response = client.responses.create(
        model="gpt-4.1-mini",
        input=prompt,
        max_output_tokens=1500
    )

    return response.output_text.strip()

def save_dsc_to_file(dsc_template: str, filename: str = "dsc_template.ps1") -> None:
    """
    Save the generated DSC template to a file
    """
    with open(filename, "w", encoding="utf-8") as file:
        file.write(dsc_template)
    print(f"\nDSC template saved as {filename}")

def main():
    """
    Main function to generate and save DSC template
    """
    prompt = (
        "Generate a PowerShell Desired State Configuration (DSC) template for deploying a web server. "
        "Include IIS installation, firewall rules, and deployment of a sample website."
    )

    print("===== Generating DSC Template =====")
    dsc_template = generate_dsc_template(prompt)

    print("===== Generated DSC Template =====\n")
    print(dsc_template)

    save_dsc_to_file(dsc_template)

if __name__ == "__main__":
    main()
    
    