@echo off
REM Windows Build Script for Siena's Snowy Adventure
REM Must be run from project root with Python and dependencies installed

SET /p VERSION=<VERSION

echo ======================================
echo Siena's Snowy Adventure - Windows Build
echo Version: %VERSION%
echo ======================================
echo.

echo Building with PyInstaller...
python -m PyInstaller siena_snowy_adventure_windows.spec --clean

if %ERRORLEVEL% NEQ 0 (
    echo.
    echo ❌ Build failed!
    exit /b 1
)

echo.
echo ======================================
echo ✅ Build Complete!
echo ======================================
echo.
echo Executable: dist\SienaSnowyAdventure\SienaSnowyAdventure.exe
echo.
echo Creating distribution ZIP...
cd dist
if exist "SienaSnowyAdventure-Windows-v%VERSION%.zip" del "SienaSnowyAdventure-Windows-v%VERSION%.zip"
powershell Compress-Archive -Path SienaSnowyAdventure -DestinationPath SienaSnowyAdventure-Windows-v%VERSION%.zip -Force

if %ERRORLEVEL% NEQ 0 (
    echo.
    echo ❌ ZIP creation failed!
    cd ..
    exit /b 1
)

cd ..

echo.
echo ======================================
echo ✅ DISTRIBUTION READY!
echo ======================================
echo.
echo 📦 Distribution file: dist\SienaSnowyAdventure-Windows-v%VERSION%.zip
echo.
echo Next steps:
echo 1. Test: dist\SienaSnowyAdventure\SienaSnowyAdventure.exe
echo 2. Create GitHub Release with tag v%VERSION%-windows
echo 3. Upload dist\SienaSnowyAdventure-Windows-v%VERSION%.zip to release
echo.
