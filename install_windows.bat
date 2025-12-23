@echo off
REM Quick installer for Siena's Snowy Adventure - Windows
REM Downloads and extracts the game, then launches it

echo ================================================================================
echo              SIENA'S SNOWY ADVENTURE - Quick Installer
echo ================================================================================
echo.

REM Note: Update VERSION below when you create a Windows release
SET VERSION=1.2.7
SET DOWNLOAD_URL=https://github.com/18drider360/siena_snowy_adventure/releases/download/v%VERSION%/SienaSnowyAdventure-Windows-v%VERSION%.zip

REM Check if release exists before downloading
echo Checking for Windows release v%VERSION%...
SET DOWNLOAD_DIR=%USERPROFILE%\Downloads
SET ZIP_FILE=%DOWNLOAD_DIR%\SienaSnowyAdventure.zip
SET EXTRACT_DIR=%DOWNLOAD_DIR%\SienaSnowyAdventure
SET EXE_PATH=%EXTRACT_DIR%\SienaSnowyAdventure\SienaSnowyAdventure.exe

echo Downloading Siena's Snowy Adventure v%VERSION%...
echo.

REM Download using PowerShell
powershell -Command "& {Invoke-WebRequest -Uri '%DOWNLOAD_URL%' -OutFile '%ZIP_FILE%'}"

if %ERRORLEVEL% NEQ 0 (
    echo.
    echo ❌ Download failed! Please check your internet connection.
    echo.
    echo You can download manually from:
    echo %DOWNLOAD_URL%
    pause
    exit /b 1
)

echo ✅ Download complete!
echo.
echo Extracting game files...

REM Extract using PowerShell
powershell -Command "& {Expand-Archive -Path '%ZIP_FILE%' -DestinationPath '%EXTRACT_DIR%' -Force}"

if %ERRORLEVEL% NEQ 0 (
    echo.
    echo ❌ Extraction failed!
    pause
    exit /b 1
)

echo ✅ Installation complete!
echo.
echo Game installed to: %EXTRACT_DIR%
echo.
echo Launching game...
echo.

REM Launch the game
start "" "%EXE_PATH%"

echo.
echo ================================================================================
echo If you see "Windows protected your PC":
echo   1. Click "More info"
echo   2. Click "Run anyway"
echo.
echo Enjoy the game! ❄️
echo ================================================================================
echo.
