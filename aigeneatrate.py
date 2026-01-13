
'''
# azure dsc  desired state configuration for ai gen

'''


'''
flow of code 

1. create prompt powershell desired state dsc 
2. openai model
3. response openai 
4. response from  openai  we write in to as ur wish filename ps1 

'''

# Replace with your OpenAI API key


"""
Azure DSC – Desired State Configuration Generator using OpenAI (NEW API)
"""

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


def main():
    prompt = (
        "Generate a PowerShell Desired State Configuration (DSC) template for deploying a web server. "
        "Include IIS installation, firewall rules, and deployment of a sample website."
    )

    dsc_template = generate_dsc_template(prompt)

    print("===== Generated DSC Template =====\n")
    print(dsc_template)

    # Save DSC to file
    with open("dsc_template.ps1", "w", encoding="utf-8") as file:
        file.write(dsc_template)

    print("\nDSC template saved as dsc_template.ps1")


if __name__ == "__main__":
    main()
