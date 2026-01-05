# PowerShell script for model rollback and upgrade in AKS

param (
    [string]$ResourceGroupName,
    [string]$AKSClusterName,
    [string]$Namespace = "default",
    [string]$DeploymentName,
    [string]$RollbackImage,
    [string]$UpgradeImage
)

# Login to Azure
az login

# Set the context to the AKS cluster
az aks get-credentials --resource-group $ResourceGroupName --name $AKSClusterName

# Function to rollback to a previous image
function Rollback-Model {
    Write-Host "Rolling back deployment $DeploymentName to image $RollbackImage..."
    kubectl set image deployment/$DeploymentName *=$RollbackImage -n $Namespace
    kubectl rollout status deployment/$DeploymentName -n $Namespace
    Write-Host "Rollback completed."
}

# Function to upgrade to a new image
function Upgrade-Model {
    Write-Host "Upgrading deployment $DeploymentName to image $UpgradeImage..."
    kubectl set image deployment/$DeploymentName *=$UpgradeImage -n $Namespace
    kubectl rollout status deployment/$DeploymentName -n $Namespace
    Write-Host "Upgrade completed."
}

# Main menu
Write-Host "Select an operation:"
Write-Host "1. Rollback"
Write-Host "2. Upgrade"
$choice = Read-Host "Enter your choice (1 or 2)"

switch ($choice) {
    "1" {
        Rollback-Model
    }
    "2" {
        Upgrade-Model
    }
    default {
        Write-Host "Invalid choice. Exiting."
    }
}