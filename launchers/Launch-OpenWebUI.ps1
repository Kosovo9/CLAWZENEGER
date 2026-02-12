Start-Process -FilePath 'D:\Neil Virtual Tests\NexoBot\NexoBot-Manager.ps1' -ArgumentList '-Action Start' -WindowStyle Hidden; Start-Sleep -Seconds 5; Start-Process 'http://localhost:3000'
