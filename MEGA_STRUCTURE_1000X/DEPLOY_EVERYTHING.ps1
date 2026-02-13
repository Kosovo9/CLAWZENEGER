<#
.SYNOPSIS
    DEPLOY_EVERYTHING.ps1 - Master Deployment Script for Clawzeneger 1000X
#>
$ErrorActionPreference = "Stop"
Write-Host "🔥 CLAWZENEGER MASTER DEPLOYMENT INITIATED..." -ForegroundColor Cyan

$root = "c:\CLAWZENEGER\MEGA_STRUCTURE_1000X"
Set-Location $root

# 1. Environment Check
if (-not (Test-Path ".env")) {
    Write-Host "Creating .env..." -ForegroundColor Yellow
    Copy-Item ".env.example" ".env" -ErrorAction SilentlyContinue
}

# 2. Core Infrastructure (God Mode)
Write-Host "🚀 Launching Core Infrastructure (Postgres, Redis, Chroma, LLMs)..." -ForegroundColor Green
docker-compose -f docker-compose.god_mode.FINAL.yml up -d --build

# 3. HubZeneger (The Brain & Dashboard)
Write-Host "🧠 Launching HubZeneger (Orchestrator & Dashboard)..." -ForegroundColor Green
Set-Location "$root\hubzeneger"
docker-compose -f docker-compose.hubzeneger.yml up -d --build

# 4. Lead Generation Automation (The Money Makers)
Write-Host "💸 Launching Lead Automation Agents (LeadHunter, Closer)..." -ForegroundColor Green
Set-Location "$root\clawzeneger-skills\lead-generation-automation"
docker-compose -f docker-compose.leadgen.yml up -d --build

# 5. Summary
Clear-Host
Write-Host "✅ SYSTEM FULLY OPERATIONAL" -ForegroundColor Green -BackgroundColor Black
Write-Host "================================================================"
Write-Host "📊 DASHBOARD:       http://localhost:3000  (Control Center)"
Write-Host "🧠 ORCHESTRATOR:    http://localhost:8000  (API Docs)"
Write-Host "🛠️  SCILL SYSTEM:    http://localhost:8002  (Funnel/Payments)"
Write-Host "================================================================"
Write-Host "💰 MONEY PLAN (NEXT 3 HOURS):"
Write-Host "   1. Open Dashboard -> Agents Panel"
Write-Host "   2. Activate 'LeadHunter' to scrape Twitter/Linkedin"
Write-Host "   3. Activate 'SalesCloser' to auto-email proposals"
Write-Host "   4. Monitor 'PaymentMethods' component for incoming $$"
Write-Host "================================================================"

Start-Process "http://localhost:3000"