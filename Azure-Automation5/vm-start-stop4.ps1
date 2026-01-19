param(
    [string]$Action
)

. /Users/venkatesh/Devops-GenAI_UST/devops-basics/Azure-Automation5/config1.ps1

if ($Action -eq "start") {
    Write-Host "Starting VM..."
    az vm start --resource-group $ResourceGroup --name $VMName
}

elseif ($Action -eq "stop") {
    Write-Host "Stopping VM..."
    az vm deallocate --resource-group $ResourceGroup --name $VMName
}

else {
    Write-Host "Usage: ./vm-start-stop.ps1 start|stop"
}
