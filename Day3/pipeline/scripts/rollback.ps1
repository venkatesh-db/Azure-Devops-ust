# PowerShell Script for Rollback

Write-Host "Starting rollback process..."

# Example rollback logic
if (Test-Path -Path "C:\Backup\BackupFile.txt") {
    try {
        Copy-Item -Path "C:\Backup\BackupFile.txt" -Destination "C:\OriginalLocation\" -Force
        Write-Host "Rollback completed: Backup restored." -ForegroundColor Green

        # Log rollback success to external system
        $logMessage = "Rollback completed successfully at $(Get-Date)"
        Invoke-RestMethod -Uri "https://example-log-endpoint" -Method Post -Body (@{ message = $logMessage } | ConvertTo-Json) -ContentType "application/json"
    } catch {
        Write-Host "Error during rollback: $_" -ForegroundColor Red
        # Log rollback error to external system
        $logMessage = "Rollback failed at $(Get-Date): $_"
        Invoke-RestMethod -Uri "https://example-log-endpoint" -Method Post -Body (@{ message = $logMessage } | ConvertTo-Json) -ContentType "application/json"
        exit 1
    }
} else {
    Write-Host "Rollback failed: Backup file not found." -ForegroundColor Red
    # Log rollback failure to external system
    $logMessage = "Rollback failed at $(Get-Date): Backup file not found."
    Invoke-RestMethod -Uri "https://example-log-endpoint" -Method Post -Body (@{ message = $logMessage } | ConvertTo-Json) -ContentType "application/json"
    exit 1
}