import requests
import time
import pandas as pd


# ----- CONFIG -----
INAT_TIMEOUT = 10

# List of invasive taxon IDs (your list from before)
INVASIVE_IDS = {
    48537, 77310, 208800, 60951, 1557658, 47892, 57623, 60202, 75386,
    131249, 159852, 165603, 1619462, 164566, 79388, 47911, 430581,
    84813, 75921, 60220, 75255, 474366, 116710, 62666, 1493168, 79137,
    64240, 52714, 70020, 48888, 78976, 962637, 58754, 1466281
}


def inat_get_taxon(taxon_id):
    url = f"https://api.inaturalist.org/v1/taxa/{taxon_id}"
    r = requests.get(url, timeout=INAT_TIMEOUT)
    r.raise_for_status()
    time.sleep(0.2)  # polite delay
    return r.json()

def main():
    inat_ids = sorted(list(INVASIVE_IDS))  # only fetching your invasive list

    rows = []
    for tid in inat_ids:
        print(f"Fetching iNat taxon {tid}...")
        try:
            j = inat_get_taxon(tid)
            result = j.get("results", [{}])[0]
            sci_name = result.get("name")
            common_name = result.get("preferred_common_name") or result.get("common_name") or ""
            status = "invasive" if tid in INVASIVE_IDS else ""
            rows.append({
                "scientific_name": sci_name,
                "common_name": common_name,
                "status": status,
                "inat_taxon_id": tid
            })
        except Exception as e:
            print(f"[ERROR] Failed to fetch taxon {tid}: {e}")
            rows.append({
                "scientific_name": "",
                "common_name": "",
                "status": "invasive" if tid in INVASIVE_IDS else "",
                "inat_taxon_id": tid
            })
        time.sleep(0.2)  # polite delay

    df = pd.DataFrame(rows)
    out_csv = "inat_invasive_taxa.csv"
    df.to_csv(out_csv, index=False)
    print(f"✅ Done. Wrote {out_csv}")

if __name__ == "__main__":
    main()
