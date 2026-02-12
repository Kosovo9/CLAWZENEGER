# Convertir JPG a ICO usando .NET
Add-Type -AssemblyName System.Drawing

$jpgPath = "D:\Neil Virtual Tests\NexoBot\nexobot-icon.jpg"
$icoPath = "D:\Neil Virtual Tests\NexoBot\nexobot-icon.ico"

# Cargar la imagen
$img = [System.Drawing.Image]::FromFile($jpgPath)

# Crear un bitmap con el tamaño deseado (256x256 para mejor calidad)
$bitmap = New-Object System.Drawing.Bitmap 256, 256
$graphics = [System.Drawing.Graphics]::FromImage($bitmap)
$graphics.InterpolationMode = [System.Drawing.Drawing2D.InterpolationMode]::HighQualityBicubic
$graphics.DrawImage($img, 0, 0, 256, 256)

# Guardar como ICO
$bitmap.Save($icoPath, [System.Drawing.Imaging.ImageFormat]::Icon)

# Limpiar recursos
$graphics.Dispose()
$bitmap.Dispose()
$img.Dispose()

Write-Host "✅ Ícono convertido a ICO: $icoPath"

# Crear el acceso directo
$WshShell = New-Object -comObject WScript.Shell
$Shortcut = $WshShell.CreateShortcut("$env:USERPROFILE\Desktop\NexoBot.lnk")
# Extract real token from systemd service
$RealToken = wsl bash -c "systemctl --user show clawdbot-gateway.service -p Environment | grep CLAWDBOT_GATEWAY_TOKEN | sed 's/.*CLAWDBOT_GATEWAY_TOKEN=//;s/ .*//' | tr -d '\n'"
$Shortcut.TargetPath = "C:\Program Files\Google\Chrome\Application\chrome.exe"
$Shortcut.Arguments = "--new-window --app=http://localhost:18789/chat?token=$RealToken"
$Shortcut.IconLocation = $icoPath
$Shortcut.Description = "Abrir NexoBot Chat"
$Shortcut.WorkingDirectory = "D:\Neil Virtual Tests\NexoBot"
$Shortcut.Save()

Write-Host "✅ Acceso directo creado en el escritorio: NexoBot.lnk"
Write-Host ""
Write-Host "🎯 Haz doble clic en el ícono 'NexoBot' en tu escritorio para abrir el chat"
