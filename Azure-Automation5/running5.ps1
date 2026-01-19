#pwsh ./running5.ps1



Write-Host "==============================="
Write-Host " Azure Automation Started "
Write-Host "==============================="

# 1️⃣ Load config
. /Users/venkatesh/Devops-GenAI_UST/devops-basics/Azure-Automation5/config1.ps1

# 2️⃣ Connect to Azure
. /Users/venkatesh/Devops-GenAI_UST/devops-basics/Azure-Automation5/connect-azure2.ps1

# 3️⃣ Server health check
. /Users/venkatesh/Devops-GenAI_UST/devops-basics/Azure-Automation5/server-health3.ps1

# 4️⃣ VM operation
/Users/venkatesh/Devops-GenAI_UST/devops-basics/Azure-Automation5/vm-start-stop4.ps1 stop
# change to 'start' if needed

Write-Host "==============================="
Write-Host " Automation Completed "
Write-Host "==============================="
