# PowerShell script to deploy Azure VMs

param (
    [string]$resourceGroupName,
    [string]$location,
    [string]$resourceToken
)

$ErrorActionPreference = "Continue"

# Check if resource group exists
$rgExist = az group show --name $resourceGroupName 2>$null
if (-not $rgExist) {
    az group create --name $resourceGroupName --location $location
}

# Deploy VM
$vmName = "vm$resourceToken"
$vmExist = az vm show --name $vmName --resource-group $resourceGroupName 2>$null
if (-not $vmExist) {
    az vm create --resource-group $resourceGroupName --name $vmName --image UbuntuLTS --admin-username azureuser --generate-ssh-keys
}

Write-Output "Deployment completed successfully."