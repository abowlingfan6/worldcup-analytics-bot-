import requests
import pandas as pd
import os

MATCH_ID = 15186710
BASE = f"https://api.sofascore.com/api/v1/event/{MATCH_ID}"


# -----------------------
# FETCH DATA
# -----------------------
def fetch(endpoint):
    url = f"{BASE}/{endpoint}"
    r = requests.get(url)
    return r.json()


def get_lineups():
    return fetch("lineups")


def get_incidents():
    return fetch("incidents")


# -----------------------
# BUILD PLAYERS
# -----------------------
def build_players(lineups):
    players = []

    if not lineups:
        print("No lineups returned")
        return pd.DataFrame(columns=["player", "team", "goals", "assists", "shots", "tackles"])

    for side_key in lineups.keys():
        side_data = lineups.get(side_key, {})

        team_players = side_data.get("players", [])

        for p in team_players:
            player_obj = p.get("player", {})

            name = player_obj.get("name")

            if not name:
                continue

            players.append({
                "player": name,
                "team": side_key,
                "goals": 0,
                "assists": 0,
                "shots": 0,
                "tackles": 0
            })

    if not players:
        return pd.DataFrame(columns=["player", "team", "goals", "assists", "shots", "tackles"])

    return pd.DataFrame(players)


# -----------------------
# ADD INCIDENTS
# -----------------------
def add_incidents(df, incidents):
    for inc in incidents.get("incidents", []):
        name = inc.get("playerName")

        if name in df["player"].values:
            if inc["incidentType"] == "goal":
                df.loc[df["player"] == name, "goals"] += 1

    return df


# -----------------------
# RATING MODEL
# -----------------------
def calculate_rating(row):
    return (
        6.0
        + 1.0 * row["goals"]
        + 0.5 * row["assists"]
        + 0.1 * row["shots"]
        + 0.075 * row["tackles"]
    )


# -----------------------
# SAVE TO GITHUB CSV
# -----------------------
def save_csv(df):
    os.makedirs("data", exist_ok=True)
    df.to_csv("data/worldcup_ratings.csv", index=False)


# -----------------------
# MAIN
# -----------------------
def main():
    lineups = get_lineups()
    incidents = get_incidents()

    players = build_players(lineups)
    players = add_incidents(players, incidents)

    players["rating"] = players.apply(calculate_rating, axis=1)

    save_csv(players)

    print("Updated worldcup_ratings.csv")


if __name__ == "__main__":
    main()
