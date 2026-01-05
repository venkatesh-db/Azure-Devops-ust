# PowerShell script to configure automatic patching for Azure VMs

param (
    [string]$resourceGroupName,
    [string]$vmName
)

$ErrorActionPreference = "Continue"

# Check if VM exists
$vmExist = az vm show --name $vmName --resource-group $resourceGroupName 2>$null
if (-not $vmExist) {
    Write-Error "VM $vmName does not exist in resource group $resourceGroupName."
    exit 1
}

# Enable automatic patching
az vm update \
  --resource-group $resourceGroupName \
  --name $vmName \
  --set osProfile.windowsConfiguration.enableAutomaticUpdates=true

Write-Output "Automatic patching enabled for VM $vmName."