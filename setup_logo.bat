@echo off
REM Auto-process and setup logo

echo.
echo ============================================================
echo  Logo Processing and Setup
echo ============================================================
echo.

if not exist "logo.png" (
    echo ERROR: Please save logo as "logo.png" in this folder
    echo.
    echo Expected location: %cd%\logo.png
    echo.
    pause
    exit /b 1
)

echo [1/3] Processing logo (making background transparent)...
python process_logo.py

if errorlevel 1 (
    echo ERROR: Failed to process logo
    pause
    exit /b 1
)

echo.
echo [2/3] Moving processed logos to assets folder...
if not exist "assets" mkdir assets
move /Y logo_transparent.png assets\ >nul
move /Y logo_optimized.png assets\ >nul
echo [OK] Logos moved to assets folder

echo.
echo [3/3] Done!
echo.
echo ============================================================
echo  Logo Setup Complete
echo ============================================================
echo.
echo The dashboard will now display your company logo!
echo.
echo Restart the dashboard to see the changes:
echo   python dashboard.py
echo.
pause
