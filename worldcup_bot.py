import requests
import pandas as pd
import os

MATCH_ID = 15186710
BASE = f"https://api.sofascore.com/api/v1/event/{MATCH_ID}"


# -----------------------
# FETCH DATA SAFELY
# -----------------------
def fetch(endpoint):
    url = f"{BASE}/{endpoint}"

    try:
        r = requests.get(url, headers={"User-Agent": "Mozilla/5.0"})
        r.raise_for_status()
        return r.json()
    except:
        return {}


# -----------------------
# GET INCIDENTS (SAFE DATA SOURCE)
# -----------------------
def get_incidents():
    data = fetch("incidents")
    return data if data else {}


# -----------------------
# BUILD PLAYERS FROM INCIDENTS
# (MOST RELIABLE METHOD)
# -----------------------
def build_players(incidents):
    players = {}

    if not incidents:
        return pd.DataFrame(columns=["player", "goals"])

    for inc in incidents.get("incidents", []):
        name = inc.get("playerName")

        if not name:
            continue

        if name not in players:
            players[name] = {
                "player": name,
                "goals": 0
            }

        if inc.get("incidentType") == "goal":
            players[name]["goals"] += 1

    return pd.DataFrame(players.values())


# -----------------------
# RATING MODEL
# -----------------------
def calculate_rating(row):
    return 6.0 + (1.0 * row["goals"])


# -----------------------
# SAVE CSV
# -----------------------
def save_csv(df):
    os.makedirs("data", exist_ok=True)
    df.to_csv("data/worldcup_ratings.csv", index=False)


# -----------------------
# MAIN
# -----------------------
def main():
    print("Starting bot...")

    incidents = get_incidents()

    players = build_players(incidents)

    print("Players extracted:")
    print(players)

    if players.empty:
        print("No data found. Exiting safely.")
        return

    players["rating"] = players.apply(calculate_rating, axis=1)

    save_csv(players)

    print("SUCCESS - CSV updated")


if __name__ == "__main__":
    main()
