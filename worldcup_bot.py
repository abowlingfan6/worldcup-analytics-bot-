import requests
import pandas as pd

MATCH_ID = 15186710
BASE = f"https://api.sofascore.com/api/v1/event/{MATCH_ID}"

def fetch(endpoint):
    url = f"{BASE}/{endpoint}"
    return requests.get(url).json()

def main():
    stats = fetch("statistics")
    lineups = fetch("lineups")
    incidents = fetch("incidents")

    print("Data pulled successfully")
    print(stats.keys())

if __name__ == "__main__":
    main()
