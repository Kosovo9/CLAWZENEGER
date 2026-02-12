$ErrorActionPreference = 'Stop'
Start-Process 'http://127.0.0.1:3000'
Start-Process 'http://127.0.0.1:18789/?token=z50jJAY_979ukYntMZUZtBnCCH4n-rN0JnmKbjwTHWE'
Write-Host 'OK. Abierto:' -ForegroundColor Green
Write-Host 'OpenWebUI: http://127.0.0.1:3000'
Write-Host 'Dashboard: http://127.0.0.1:18789/?token=z50jJAY_979ukYntMZUZtBnCCH4n-rN0JnmKbjwTHWE'
