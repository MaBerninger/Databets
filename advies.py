import git
import os
import pandas as pd
from datetime import datetime

# === Config ===
LOCAL_REPO = r"C:\bets\website\Databets"

# Bronbestand (Excel met meerdere tabbladen)
FILE_SOURCE = r"Z:\Downloads\Voetbal\Live\voetbal_odds.xlsx"

# Doelbestand in je repo (we slaan alleen tabblad 'Advies' op)
FILE_TARGET = os.path.join(LOCAL_REPO, "data", "Advies.xlsx")

# (Optioneel) Token/URL als je via HTTPS met token wil pushen; niet vereist als je git-credentials al goed staan.
TOKEN = "github_pat_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"
GITHUB_URL = f"https://{TOKEN}@github.com/maberninger/Databets.git"

def main():
    # === Stap 1: Lees alleen tabblad 'Advies' in ===
    df = pd.read_excel(FILE_SOURCE, sheet_name="Advies")

    # === Stap 1b: Voeg timestamp-rij toe bovenaan (A1) ===
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    ts_text = f"Laatst bijgewerkt: {timestamp}"

    # Maak een 1-rij DataFrame met in kolom A de timestamp en verder lege velden,
    # met dezelfde kolomnamen als df zodat concat netjes werkt.
    ts_row = pd.DataFrame([[ts_text] + [""] * (len(df.columns) - 1)], columns=df.columns)

    # Concat: timestamp-rij boven, daarna het originele 'Advies'-tabblad
    out_df = pd.concat([ts_row, df], ignore_index=True)

    # Zorg dat de map 'data' bestaat
    os.makedirs(os.path.dirname(FILE_TARGET), exist_ok=True)

    # Schrijf het resultaat naar Excel (tabblad 'Advies'); headers van df komen op rij 2
    out_df.to_excel(FILE_TARGET, sheet_name="Advies", index=False)
    print(f"✅ Tabblad 'Advies' gekopieerd en timestamp gezet in A1: {FILE_SOURCE} → {FILE_TARGET}")
    print(f"🕒 Timestamp: {ts_text}")

    # === Stap 2: Open repo ===
    repo = git.Repo(LOCAL_REPO)

    # === Stap 3: Stage wijzigingen ===
    repo.git.add(all=True)

    # === Stap 4: Commit (alleen als er echt iets gewijzigd is) ===
    if repo.is_dirty(untracked_files=True):
        repo.index.commit("Update advies-tabblad + timestamp in A1")
        print("📝 Commit gemaakt.")
    else:
        print("ℹ️ Geen wijzigingen om te committen.")

    # === Stap 5: Push naar GitHub ===
    origin = repo.remote(name="origin")
    # Als je per se via de token-URL wil pushen:
    # origin.set_url(GITHUB_URL)
    origin.push(refspec="HEAD:refs/heads/main")
    print("🚀 Tabblad 'Advies' succesvol naar GitHub gepusht!")

if __name__ == "__main__":
    main()
