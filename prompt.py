#🏗️ CORE PRINCIPLE: MULTI-STEP PROMPTS


#Create a step-by-step Azure pipeline with validation, deploy, verification, and rollback.

#🔑 THE 7-BLOCK PROMPT FRAMEWORK

'''
1. ROLE
2. CONTEXT
3. INPUTS
4. CONSTRAINTS
5. STEP SEQUENCE
6. OUTPUT FORMAT
7. VALIDATION RULES
'''

#🧩 TEMPLATE: MULTI-STEP PIPELINE PROMPT

'''
ROLE:
You are a Senior DevOps Automation Engineer.

CONTEXT:
We are automating the deployment of Azure infrastructure using ARM templates via Azure DevOps pipelines.

INPUTS:
- ARM template file: azuredeploy.json
- Parameters file: parameters.dev.json
- Environment: dev
- Azure subscription: already authenticated

CONSTRAINTS:
- Do NOT use preview features.
- Use Azure CLI exclusively.
- Follow least privilege principles.
- Ensure idempotent execution.

STEP SEQUENCE:
1. Validate the ARM template.
2. Create or update the resource group.
3. Deploy the ARM template.
4. Verify the deployment success.
5. Output the resource details.
6. Provide rollback steps in case of deployment failure.

OUTPUT FORMAT:
- YAML pipeline format.
- Each step must be commented for clarity.
- No explanations outside the code block.

VALIDATION RULES:
- The pipeline must fail if validation fails.
- Deployment mode must be incremental.

'''


#🤖 CHAINED PROMPTING (ADVANCED BUT SIMPLE)


'''
Instead of one huge prompt, do controlled chaining:

Prompt 1 – Generate pipeline skeleton

“Generate pipeline stages only.”

Prompt 2 – Add deployment steps

“Add ARM validation and deployment steps.”

Prompt 3 – Add verification

“Add post-deployment verification using Azure CLI.”

Prompt 4 – Add rollback logic

“Add rollback steps triggered on failure.”

'''
