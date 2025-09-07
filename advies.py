import git
import os
import pandas as pd
import time
from datetime import datetime

# === Config ===
LOCAL_REPO = r"C:\bets\website\Databets"
FILE_SOURCE = r"Z:\Downloads\Voetbal\Live\voetbal_odds.xlsx"
FILE_TARGET = os.path.join(LOCAL_REPO, "data", "Advies.xlsx")

def process_file():
    # Probeer bestand max 30x te openen
    for attempt in range(1, 31):
        try:
            df = pd.read_excel(FILE_SOURCE, sheet_name="Advies")

            # Timestamp toevoegen
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            ts_text = f"Laatst bijgewerkt: {timestamp}"
            ts_row = pd.DataFrame([[ts_text] + [""] * (len(df.columns) - 1)], columns=df.columns)
            out_df = pd.concat([ts_row, df], ignore_index=True)

            # Map maken als nodig
            os.makedirs(os.path.dirname(FILE_TARGET), exist_ok=True)

            # Schrijf output
            out_df.to_excel(FILE_TARGET, sheet_name="Advies", index=False)
            print(f"✅ Tabblad 'Advies' gekopieerd en timestamp gezet: {ts_text}")

            # Git commit + push
            repo = git.Repo(LOCAL_REPO)
            repo.git.add(all=True)
            if repo.is_dirty(untracked_files=True):
                repo.index.commit("Update advies-tabblad + timestamp in A1")
                print("📝 Commit gemaakt.")
            else:
                print("ℹ️ Geen wijzigingen om te committen.")
            origin = repo.remote(name="origin")
            origin.push(refspec="HEAD:refs/heads/main")
            print("🚀 Tabblad 'Advies' succesvol naar GitHub gepusht!")
            return  # Gelukt, stop met retryen

        except Exception as e:
            print(f"❌ Poging {attempt}/30 mislukt: {e}")
            if attempt < 30:
                print("⏳ Wachten 20 sec en opnieuw proberen...")
                time.sleep(20)
            else:
                print("⛔ Bestand bleef onbereikbaar. Stop na 30 pogingen.")
                return

def main():
    process_file()   # 1x draaien i.p.v. oneindige loop

if __name__ == "__main__":
    main()
