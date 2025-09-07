@echo off
cd /d C:\bets\website\Databets

REM === Haal laatste wijzigingen van GitHub ===
git pull origin main --rebase

REM === Draai advies.py om Advies.xlsx bij te werken ===
python advies.py

REM === Alles toevoegen aan git ===
git add .

REM === Commit alleen als er iets te committen is ===
git diff --cached --quiet
IF ERRORLEVEL 1 (
    git commit -m "Automatische update"
)

REM === Push naar GitHub ===
git push origin main

pause
