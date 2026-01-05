# CI/CD Pipeline for App Deployment

This project contains an end-to-end CI/CD pipeline for deploying applications with the following features:

- **PowerShell Validation**: Ensures pre-deployment checks and rollback triggers.
- **AI Decision Nodes**: Implements retry or rollback logic based on deployment outcomes.
- **Automated Release Notes**: Generates release notes using a Python script.
- **Azure Log Analytics Integration**: Provides detailed production insights.

## Project Structure

- `scripts/`: Contains PowerShell scripts for validation and rollback.
- `ai/`: Includes AI-based decision-making logic.
- `release_notes/`: Python script for generating release notes.
- `logs/`: Integration with Azure Log Analytics.

## Getting Started

1. Clone the repository.
2. Install the required tools:
   - Azure CLI
   - Python 3.8+
   - PowerShell 7+
3. Set up the environment variables:
   - `AZURE_WORKSPACE_ID`: Your Azure Log Analytics workspace ID.
   - `AZURE_SHARED_KEY`: Your Azure Log Analytics shared key.
4. Run the pipeline:
   - Execute `validation.ps1` for pre-deployment checks.
   - Deploy the application.
   - Use `rollback.ps1` for rollback if needed.
   - Generate release notes using `generate_notes.py`.

## Requirements

- Azure CLI
- Python 3.8+
- PowerShell 7+

## License

MIT License