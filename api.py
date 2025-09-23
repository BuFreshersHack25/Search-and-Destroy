import requests
import csv
import json

BASE_URL = "https://api.inaturalist.org/v1"
PROJECT_ID = "bournemouth-university-campus-biodiversity-network"
INVASIVE_FILE = "invasive_plants.txt"
OUTPUT_JSON = "flagged_invasives.json"
OUTPUT_CSV = "flagged_invasives.csv"
PER_PAGE = 200
MAX_PAGES = 10


def load_invasives_from_txt(filename=INVASIVE_FILE):
    invasives = []
    with open(filename, newline="", encoding="utf-8") as f:
        reader = csv.reader(f)
        for row in reader:
            if not row or row[0].startswith("#"):
                continue
            scientific, common, *status = row
            invasives.append({
                "scientific_name": scientific.strip().lower(),
                "common_name": common.strip().lower(),
                "status": status[0].strip().lower() if status else ""
            })
    return invasives


def fetch_all_observations(project_id):
    all_obs = []
    for page in range(1, MAX_PAGES + 1):
        url = f"{BASE_URL}/observations"
        params = {
            "project_id": project_id,
            "per_page": PER_PAGE,
            "page": page
        }
        resp = requests.get(url, params=params)
        resp.raise_for_status()
        results = resp.json()["results"]
        if not results:
            break
        all_obs.extend(results)
        print(f"Fetched page {page}, total observations so far: {len(all_obs)}")
    return all_obs


def flag_invasives(observations, invasives):
    flagged = []
    for obs in observations:
        taxon = obs.get("taxon")
        user = obs.get("user", {})
        if not taxon:
            continue
        sci = taxon["name"].lower()
        com = taxon.get("preferred_common_name", "").lower()
        for inv in invasives:
            if sci == inv["scientific_name"] or (com and com == inv["common_name"]):
                flagged.append({
                    "scientific_name": taxon["name"],
                    "common_name": taxon.get("preferred_common_name", ""),
                    "status": inv["status"],
                    "observed_on": obs.get("observed_on", ""),
                    "latitude": obs.get("location", "").split(",")[0] if obs.get("location") else "",
                    "longitude": obs.get("location", "").split(",")[1] if obs.get("location") else "",
                    "photo_url": taxon["default_photo"]["url"] if taxon.get("default_photo") else "",
                    "user_login": user.get("login", ""),
                })
                break
    return flagged


def save_to_json(data, filename=OUTPUT_JSON):
    with open(filename, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    print(f"JSON exported to {filename}")


def save_to_csv(data, filename=OUTPUT_CSV):
    with open(filename, "w", newline="", encoding="utf-8") as f:
        fieldnames = [
            "scientific_name", "common_name", "status", "observed_on",
            "latitude", "longitude", "photo_url", "user_login"
        ]
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        for item in data:
            writer.writerow(item)
    print(f"CSV exported to {filename}")


def main():
    invasives = load_invasives_from_txt()
    print(f"Loaded {len(invasives)} invasive plants from TXT file")

    observations = fetch_all_observations(PROJECT_ID)
    print(f"Total observations fetched from project: {len(observations)}")

    flagged = flag_invasives(observations, invasives)

    print("\nInvasive species detected in Bournemouth University campuses:")
    if flagged:
        for s in flagged:
            print(f"- {s['scientific_name']} ({s['common_name']}) "
                  f"[{s['status']}] observed on {s['observed_on']} at "
                  f"({s['latitude']}, {s['longitude']}) by {s['user_login']}")
    else:
        print("None from your invasive species list were found.")

    save_to_json(flagged)
    save_to_csv(flagged)


if __name__ == "__main__":
    main()

