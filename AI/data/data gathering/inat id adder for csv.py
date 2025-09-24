import pandas as pd
import requests
import time

# Load your CSV
df = pd.read_csv("invasive_plants.csv")  # expects columns: scientific_name, common_name, status

inat_ids = []
inat_names = []

def inat_match(name):
    url = "https://api.inaturalist.org/v1/taxa"
    r = requests.get(url, params={"q": name, "per_page": 1})
    if r.status_code == 200:
        results = r.json()["results"]
        if results:
            return results[0]["id"], results[0]["name"]
    return None, None

# Loop over species
for sci_name in df["scientific_name"]:
    taxon_id, inat_name = inat_match(sci_name)
    inat_ids.append(taxon_id)
    time.sleep(0.2)  # polite API rate limiting

# Add results to dataframe
df["inat_taxon_id"] = inat_ids

print(inat_ids)

# Save new CSV
df.to_csv("invasive_plants_with_inat_ids.csv", index=False)

print("✅ Finished. New CSV written as invasive_plants_with_inat_ids.csv")
