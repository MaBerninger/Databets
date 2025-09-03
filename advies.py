import git
import os
import pandas as pd

# === Config ===
LOCAL_REPO = r"C:\bets\website\Databets"

# Bronbestand (Excel met meerdere tabbladen)
FILE_SOURCE = r"Z:\Downloads\Voetbal\Live\voetbal_odds.xlsx"

# Doelbestand in je repo (we slaan alleen tabblad 'Advies' op)
FILE_TARGET = os.path.join(LOCAL_REPO, "data", "Advies.xlsx")

# GitHub token direct in de code (alleen voor debug!)
TOKEN = "github_pat_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"

# Repo-URL met token
GITHUB_URL = f"https://{TOKEN}@github.com/maberninger/Databets.git"

# === Stap 1: Lees alleen tabblad 'Advies' in ===
df = pd.read_excel(FILE_SOURCE, sheet_name="Advies")

# Zorg dat de map 'data' bestaat
os.makedirs(os.path.dirname(FILE_TARGET), exist_ok=True)

# Schrijf alleen dit tabblad naar een nieuw Excel-bestand
df.to_excel(FILE_TARGET, sheet_name="Advies", index=False)
print(f"✅ Tabblad 'Advies' gekopieerd: {FILE_SOURCE} → {FILE_TARGET}")

# === Stap 2: Open repo ===
repo = git.Repo(LOCAL_REPO)

# === Stap 3: Stage wijzigingen ===
repo.git.add(all=True)

# === Stap 4: Commit (alleen als er echt iets gewijzigd is) ===
if repo.is_dirty(untracked_files=True):
    repo.index.commit("Update advies-tabblad automatisch vanuit voetbal_odds.xlsx")
    print("📝 Commit gemaakt.")
else:
    print("ℹ️ Geen wijzigingen om te committen.")

# === Stap 5: Push naar GitHub ===
origin = repo.remote(name="origin")
origin.push(refspec="HEAD:refs/heads/main")

print("🚀 Tabblad 'Advies' succesvol naar GitHub gepusht!")
