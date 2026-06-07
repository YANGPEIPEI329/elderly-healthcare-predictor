# ─────────────────────────────────────────────────────────────
#  One-click deploy script
#  Commits all local changes and pushes to GitHub.
#  Render auto-deploys from the `main` branch (autoDeploy: true),
#  so pushing is all that's needed to ship an update.
#
#  Usage:
#     .\deploy.ps1                       # uses a timestamp commit message
#     .\deploy.ps1 "fix prediction bug"  # custom commit message
# ─────────────────────────────────────────────────────────────
param(
    [string]$Message = "Update $(Get-Date -Format 'yyyy-MM-dd HH:mm')"
)

# Make sure gh / git are on PATH even in a fresh shell
$env:Path = [Environment]::GetEnvironmentVariable("Path","Machine") + ";" + [Environment]::GetEnvironmentVariable("Path","User")

# Always run from the folder this script lives in
Set-Location $PSScriptRoot

Write-Host "==> Staging changes..." -ForegroundColor Cyan
git add -A

# Stop early if there is nothing to commit
$changes = git status --porcelain
if (-not $changes) {
    Write-Host "No changes to deploy. Working tree is clean." -ForegroundColor Yellow
    exit 0
}

Write-Host "==> Committing: $Message" -ForegroundColor Cyan
git -c user.name="WQD7003 Group8" -c user.email="group8@example.com" commit -m $Message

Write-Host "==> Pushing to GitHub (Render will auto-deploy)..." -ForegroundColor Cyan
git push

Write-Host ""
Write-Host "Done. Render is now building the new version." -ForegroundColor Green
Write-Host "Track it at: https://dashboard.render.com" -ForegroundColor Green
Write-Host "Live URL:    https://elderly-healthcare-predictor.onrender.com" -ForegroundColor Green
