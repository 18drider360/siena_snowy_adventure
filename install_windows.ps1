# Quick installer for Siena's Snowy Adventure - Windows
# Downloads and extracts the game, then launches it

Write-Host "================================================================================" -ForegroundColor Cyan
Write-Host "              SIENA'S SNOWY ADVENTURE - Quick Installer" -ForegroundColor Cyan
Write-Host "================================================================================" -ForegroundColor Cyan
Write-Host ""

# Note: Update version below when you create a Windows release
$Version = "1.2.7"
$DownloadUrl = "https://github.com/18drider360/siena_snowy_adventure/releases/download/v$Version/SienaSnowyAdventure-Windows-v$Version.zip"

Write-Host "Checking for Windows release v$Version..." -ForegroundColor Yellow
$DownloadDir = "$env:USERPROFILE\Downloads"
$ZipFile = "$DownloadDir\SienaSnowyAdventure.zip"
$ExtractDir = "$DownloadDir\SienaSnowyAdventure"
$ExePath = "$ExtractDir\SienaSnowyAdventure\SienaSnowyAdventure.exe"

Write-Host "Downloading Siena's Snowy Adventure v$Version..." -ForegroundColor Yellow
Write-Host ""

try {
    # Download the game
    Invoke-WebRequest -Uri $DownloadUrl -OutFile $ZipFile -UseBasicParsing
    Write-Host "✅ Download complete!" -ForegroundColor Green
    Write-Host ""

    Write-Host "Extracting game files..." -ForegroundColor Yellow

    # Extract the ZIP
    Expand-Archive -Path $ZipFile -DestinationPath $ExtractDir -Force
    Write-Host "✅ Installation complete!" -ForegroundColor Green
    Write-Host ""

    Write-Host "Game installed to: $ExtractDir" -ForegroundColor Cyan
    Write-Host ""
    Write-Host "Launching game..." -ForegroundColor Yellow
    Write-Host ""

    # Launch the game
    Start-Process -FilePath $ExePath

    Write-Host "================================================================================" -ForegroundColor Cyan
    Write-Host "If you see 'Windows protected your PC':" -ForegroundColor Yellow
    Write-Host "  1. Click 'More info'" -ForegroundColor White
    Write-Host "  2. Click 'Run anyway'" -ForegroundColor White
    Write-Host ""
    Write-Host "Enjoy the game! ❄️" -ForegroundColor Cyan
    Write-Host "================================================================================" -ForegroundColor Cyan
    Write-Host ""
}
catch {
    Write-Host ""
    Write-Host "❌ Installation failed!" -ForegroundColor Red
    Write-Host "Error: $_" -ForegroundColor Red
    Write-Host ""
    Write-Host "You can download manually from:" -ForegroundColor Yellow
    Write-Host $DownloadUrl -ForegroundColor White
    Write-Host ""
    Read-Host "Press Enter to exit"
    exit 1
}
