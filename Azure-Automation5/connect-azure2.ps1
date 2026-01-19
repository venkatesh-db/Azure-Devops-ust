param(
    [Parameter(Mandatory = $true)]
    [ValidateSet("start", "stop")]
    [string]$Action,

    [Parameter(Mandatory = $true)]
    [string]$SubscriptionId,

    [Parameter(Mandatory = $true)]
    [string]$ResourceGroup,

    [Parameter(Mandatory = $true)]
    [string]$VMName
)

Write-Host "Setting Azure subscription..."
az account set --subscription $SubscriptionId

if ($LASTEXITCODE -ne 0) {
    Write-Error "Failed to set Azure subscription"
    exit 1
}

Write-Host "Agent Disk Info (for troubleshooting):"
Get-PSDrive -PSProvider FileSystem

if ($Action -eq "start") {
    Write-Host "Starting VM $VMName..."
    az vm start --resource-group $ResourceGroup --name $VMName
}
elseif ($Action -eq "stop") {
    Write-Host "Stopping VM $VMName..."
    az vm deallocate --resource-group $ResourceGroup --name $VMName
}

Write-Host "Action '$Action' completed successfully."




