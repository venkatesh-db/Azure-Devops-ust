Certainly! Below is a PowerShell Desired State Configuration (DSC) template for deploying a web server with the following features:

- Installing IIS (Web-Server role)
- Creating firewall rules for HTTP (port 80) and HTTPS (port 443)
- Deploying a simple sample website to the default IIS site root

```powershell
Configuration SampleWebServer
{
    param (
        [string]$NodeName = 'localhost',
        [string]$WebsiteContentPath = "C:\\inetpub\\wwwroot\\SampleSite"
    )

    Import-DscResource -ModuleName PSDesiredStateConfiguration
    Import-DscResource -ModuleName xWebAdministration # For advanced IIS config if needed

    Node $NodeName
    {
        # Ensure IIS (Web-Server) role is installed
        WindowsFeature IIS
        {
            Ensure = "Present"
            Name   = "Web-Server"
        }

        # Firewall rule to allow HTTP inbound traffic
        FirewallAllowHTTP
        {
            Name                   = "Allow HTTP"
            Ensure                 = "Present"
            Direction              = "Inbound"
            Action                 = "Allow"
            Protocol               = "TCP"
            LocalPort              = 80
            DisplayName            = "Allow HTTP inbound traffic"
            Enabled                = "True"
        }

        # Firewall rule to allow HTTPS inbound traffic
        FirewallAllowHTTPS
        {
            Name                   = "Allow HTTPS"
            Ensure                 = "Present"
            Direction              = "Inbound"
            Action                 = "Allow"
            Protocol               = "TCP"
            LocalPort              = 443
            DisplayName            = "Allow HTTPS inbound traffic"
            Enabled                = "True"
        }

        # Ensure directory for website content exists
        File WebsiteFolder
        {
            Type        = "Directory"
            DestinationPath = $WebsiteContentPath
            Ensure      = "Present"
            Force       = $true
        }

        # Deploy sample website content (index.html)
        File SampleIndex
        {
            DestinationPath = Join-Path $WebsiteContentPath "index.html"
            Contents        = @"
<!DOCTYPE html>
<html>
<head>
    <title>Sample Website</title>
</head>
<body>
    <h1>Welcome to your DSC-deployed IIS Web Server!</h1>
    <p>This site is deployed via PowerShell DSC.</p>
</body>
</html>
"@
            Ensure          = "Present"
            Type            = "File"
            DependsOn       = "[File]WebsiteFolder"
        }

        # Optional: Configure IIS default site physical path if different from default
        # Using xWebAdministration module for advanced configurations
        # Here set default website to point to the SampleSite folder

        xWebsite DefaultSite
        {
            Ensure          = "Present"
            Name            = "Default Web Site"
            State           = "Started"
            PhysicalPath    = $WebsiteContentPath
            DependsOn       = "[WindowsFeature]IIS"
        }
    }
}
```

---

### How to use this DSC configuration

1. Save the above code to a file, e.g. `SampleWebServer.ps1`.
2. Import the `xWebAdministration` module if not already installed:

```powershell
Install-Module -Name xWebAdministration -Force
```

3. Generate the MOF file by running:

```powershell
.\SampleWebServer.ps1 -NodeName 'localhost' -WebsiteContentPath "C:\inetpub\wwwroot\SampleSite"
```

4. Apply the configuration:

```powershell
Start-DscConfiguration -Path .\SampleWebServer -Wait -Verbose -Force
```

---

### Explanation:

- **WindowsFeature**: Installs the IIS role.
- **FirewallAllowHTTP/HTTPS**: Creates firewall rules to allow HTTP and HTTPS traffic.
- **File WebsiteFolder**: Ensures the website folder exists.
- **File SampleIndex**: Deploys a simple sample `index.html`.
- **xWebsite DefaultSite**: Sets the physical path of the IIS Default Web Site to the sample folder and ensures IIS is running.

Let me know if you want this enhanced, for example adding SSL cert deployment or multiple application pools!