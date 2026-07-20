import csv
import re

def update_statistics():
    # 1. Load data from CSVs
    recipes = []
    with open('recipes.csv', mode='r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            recipes.append(row)

    regions = []
    with open('regions.csv', mode='r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            regions.append(row)

    # 2. Extract metrics
    recipe_ids = {r['Recipe Id'] for r in recipes}
    total_recipes = len(recipe_ids)

    veg_count = sum(1 for r in recipes if r['Is Non Veg'].strip().upper() == 'FALSE')
    non_veg_count = sum(1 for r in recipes if r['Is Non Veg'].strip().upper() == 'TRUE')

    popular_ids = {r['Recipe Id'] for r in regions if r['Region Code'] == 'popular'}
    popular_count = len(recipe_ids.intersection(popular_ids))
    regional_count = total_recipes - popular_count

    # 3. Configure region groupings
    region_groups = [
        {'label': '**popular**', 'desc': 'Pan-Indian / Highly Commercialized', 'codes': ['popular'], 'examples': '*Chole Bhature, Palak Paneer, Masala Chai*'},
        {'label': '**AN / LAN**', 'desc': 'Andaman & Nicobar Islands (Settler & Indigenous)', 'codes': ['AN', 'LAN'], 'examples': '*Coconut Prawn Curry, Larop (Pandanus Dough)*'},
        {'label': '**AP / TG**', 'desc': 'Andhra Pradesh & Telangana', 'codes': ['AP', 'TG'], 'examples': '*Gongura Mamsam, Karsi Dumpa (Koya Tuber)*'},
        {'label': '**AR**', 'desc': 'Arunachal Pradesh (Adi, Nyishi, Apatani)', 'codes': ['AR'], 'examples': '*Pasa (Raw Fish Soup), Pikey Pila*'},
        {'label': '**AS**', 'desc': 'Assam (Bodo, Mising, Karbi)', 'codes': ['AS'], 'examples': '*Onla (Rice Powder Curry), Samo Sobai (Snails)*'},
        {'label': '**BR / JH / OR**', 'desc': 'Bihar, Jharkhand & Odisha (Santhal, Oraon, Saora)', 'codes': ['BR', 'JH', 'OR'], 'examples': '*Leto, Rugra Curry, Kai Chutney*'},
        {'label': '**CT**', 'desc': 'Chhattisgarh', 'codes': ['CT'], 'examples': '*Chaprah (Red Ant Chutney), Sikiya Kheer*'},
        {'label': '**GA**', 'desc': 'Goa', 'codes': ['GA'], 'examples': '*Goan Fish Curry, Sorpotel, Lapsi*'},
        {'label': '**GJ / MP / RJ / MH**', 'desc': 'West & Central (Dhodia, Baiga, Bhil, Gond, Warli)', 'codes': ['GJ', 'MP', 'RJ', 'MH'], 'examples': '*Paniya, Putpuda Chicken Stew, Dal Baati*'},
        {'label': '**HP**', 'desc': 'Himachal Pradesh (Gaddi)', 'codes': ['HP'], 'examples': '*Siddu, Chha Gosht (Buttermilk Mutton)*'},
        {'label': '**JK / ML / NL / MZ / MN**', 'desc': 'Himalayan & Northeast Hills (Khasi, Naga, Mizo, Manipuri)', 'codes': ['JK', 'ML', 'NL', 'MZ', 'MN'], 'examples': '*Jadoh, Vawksa Rep, Smoked Pork with Axone*'},
        {'label': '**KA / KL / TN**', 'desc': 'South India (Kodava, Nilgiri, Chenchu)', 'codes': ['KA', 'KL', 'TN'], 'examples': '*Pandi Curry, Othidvar, Wild Greens Sambar*'},
        {'label': '**SK**', 'desc': 'Sikkim', 'codes': ['SK'], 'examples': '*Phagshapa (Pork Fat Stew), Gundruk ko Jhol*'},
        {'label': '**TR / UT / WB**', 'desc': 'Tripura, Uttarakhand & West Bengal', 'codes': ['TR', 'UT', 'WB'], 'examples': '*Chakhwi, Shile Kutu, Hisa Aara Sipi*'},
    ]

    # 4. Generate the Markdown table rows
    table_rows = []
    for g in region_groups:
        matched_ids = {r['Recipe Id'] for r in regions if r['Region Code'] in g['codes']}
        unique_count = len(recipe_ids.intersection(matched_ids))
        table_rows.append(f"| {g['label']} | {g['desc']} | {unique_count} | {g['examples']} |")

    regional_table = "\n".join(table_rows)

    # 5. Read existing README.md
    with open('README.md', 'r', encoding='utf-8') as f:
        readme_text = f.read()

    # 6. Construct the new stats block
    stats_replacement = f"""### Key Statistics
* **Total Recipes:** {total_recipes}
* **Popular / Mainstream Dishes:** {popular_count}
* **Strictly Regional, Indigenous, or Tribal Dishes:** {regional_count}
* **Dietary Classification:**
  * Vegetarian Dishes: {veg_count}
  * Non-Vegetarian Dishes (Meat, Fish, Egg, or Insect): {non_veg_count}

### Regional & Tribal Breakdown
Recipes are mapped to specific regional codes (states, territories, or classifications). A single recipe may map to multiple regions if shared across borders:

| Region/State Code | Region/State/Territory Name | Unique Recipe Count | Notable Tribal / Local Examples |
|:---|:---|:---:|:---|
{regional_table}"""

    # 7. Apply Regex sub to replace old block with new block
    pattern = re.compile(r"(<!-- STATS_START -->).*?(<!-- STATS_END -->)", re.DOTALL)
    new_readme_text = pattern.sub(f"\\1\n{stats_replacement}\n\\2", readme_text)

    # 8. Write modified text back to README.md
    with open('README.md', 'w', encoding='utf-8') as f:
        f.write(new_readme_text)

    print("README.md has been successfully updated with fresh statistics.")

if __name__ == '__main__':
    update_statistics()