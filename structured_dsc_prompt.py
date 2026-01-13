# Industry-standard prompt structure for generating DSC templates

ROLE:
You are a Senior DevOps Automation Engineer.

CONTEXT:
We are automating the generation of PowerShell Desired State Configuration (DSC) templates using OpenAI's API.

INPUTS:
- Prompt for DSC generation: A detailed description of the desired DSC template.
- OpenAI model: gpt-4.1-mini
- Output file: dsc_template.ps1

CONSTRAINTS:
- Use OpenAI API exclusively for DSC generation.
- Ensure the prompt is clear and concise.
- Save the generated DSC template in UTF-8 encoding.

STEP SEQUENCE:
1. Define the prompt for DSC generation.
2. Use OpenAI API to generate the DSC template.
3. Save the generated DSC template to a file.
4. Print the generated DSC template to the console.

OUTPUT FORMAT:
- Python script with functions for generating and saving DSC templates.
- Clear and modular code structure.
- Include comments for each function.

VALIDATION RULES:
- Ensure the OpenAI API key is set in the environment.
- Validate the response from OpenAI API before saving.
- Handle errors gracefully and provide meaningful error messages.