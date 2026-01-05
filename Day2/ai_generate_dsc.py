# AI Demo: Auto-generate DSC Templates

import openai
import json

# Replace with your OpenAI API key
openai.api_key = "your-api-key"

def generate_dsc_template(prompt):
    """Generate DSC template using OpenAI API."""
    response = openai.Completion.create(
        engine="text-davinci-003",
        prompt=prompt,
        max_tokens=1500
    )
    return response.choices[0].text.strip()

def main():
    prompt = (
        "Generate a PowerShell Desired State Configuration (DSC) template for deploying a web server. "
        "Include configurations for IIS installation, firewall rules, and deployment of a sample website."
    )

    dsc_template = generate_dsc_template(prompt)
    print("Generated DSC Template:")
    print(dsc_template)

    # Save to file
    with open("dsc_template.ps1", "w") as file:
        file.write(dsc_template)

if __name__ == "__main__":
    main()