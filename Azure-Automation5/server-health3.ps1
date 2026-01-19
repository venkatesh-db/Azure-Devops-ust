Write-Host "Checking server health..."

Write-Host "CPU Info: Skipped (Not supported on this OS)"

Write-Host "Disk Info:"
Get-PSDrive -PSProvider FileSystem

