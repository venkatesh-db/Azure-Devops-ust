# Azure Monitor & Application Insights Setup with Log Analytics Workspace Integration

# Variables
$resourceGroup = "MyResourceGroup"
$location = "eastus"
$logAnalyticsWorkspaceName = "MyLogAnalyticsWorkspace"
$appInsightsName = "MyAppInsights"

# Step 1: Create a Resource Group
Write-Host "Creating Resource Group..."
az group create --name $resourceGroup --location $location

# Step 2: Create a Log Analytics Workspace
Write-Host "Creating Log Analytics Workspace..."
az monitor log-analytics workspace create `
    --resource-group $resourceGroup `
    --workspace-name $logAnalyticsWorkspaceName `
    --location $location

# Step 3: Create Application Insights and Link to Log Analytics Workspace
Write-Host "Creating Application Insights and linking to Log Analytics Workspace..."
$workspaceId = az monitor log-analytics workspace show `
    --resource-group $resourceGroup `
    --workspace-name $logAnalyticsWorkspaceName `
    --query id -o tsv

az monitor app-insights component create `
    --app $appInsightsName `
    --location $location `
    --resource-group $resourceGroup `
    --application-type web `
    --kind web `
    --workspace $workspaceId

# Step 4: Enable Azure DevOps Logs Integration
Write-Host "Enabling Azure DevOps Logs Integration..."
$organization = "https://dev.azure.com/YourOrganization"
$project = "YourProject"

# Ensure the Azure DevOps extension is installed
az extension add --name azure-devops

# Configure defaults for Azure DevOps
az devops configure --defaults organization=$organization project=$project

# Enable Azure DevOps logs integration
az monitor log-analytics workspace data-export create `
    --resource-group $resourceGroup `
    --workspace-name $logAnalyticsWorkspaceName `
    --name DevOpsLogsExport `
    --table-name AzureDiagnostics `
    --destination $workspaceId `
    --enable true

Write-Host "Setup Complete!"