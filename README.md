# Food-eaten-in-India

A relational database of Indian culinary recipes containing unique regional entries. This dataset is designed to address a common gap in mainstream culinary datasets: while major food databases focus primarily on widely commercialized Indian dishes, this dataset documents local, regional, indigenous, and tribal preparations alongside popular national staples.

The dataset is divided into four relational CSV files: `recipes.csv`, `ingredients.csv`, `instructions.csv`, and `regions.csv`.

---

## Important Disclaimer: Data Verification

> [!WARNING]
> **This dataset has been programmatically compiled/synthesized and has not been verified by a human.** 
> While efforts have been made to align cooking steps, ingredients, and regional mappings, the data may contain errors, omissions, or inaccuracies regarding measurements, botanical names, cultural origins, or safety guidelines. Do not use this data as a definitive guide for preparing toxic wild tubers or consuming rare ingredients without consulting verified, authoritative anthropological or culinary sources.

---

## Dataset Overview

Standard Indian food datasets frequently omit the culinary traditions of forest-dwelling, pastoralist, and indigenous communities. This dataset captures both mainstream staples and highly localized preparations—such as Gond *Kikad Roti*, Mising *Namsing Chutney*, Toda *Othidvar*, and Apatani *Chura Sabji*.

<!-- STATS_START -->
### Key Statistics
* **Total Recipes:** 305
* **Popular / Mainstream Dishes:** 134
* **Strictly Regional, Indigenous, or Tribal Dishes:** 171
* **Dietary Classification:**
  * Vegetarian Dishes: 198
  * Non-Vegetarian Dishes (Meat, Fish, Egg, or Insect): 107

### Regional & Tribal Breakdown
Recipes are mapped to specific regional codes (states, territories, or classifications). A single recipe may map to multiple regions if shared across borders:

| Region/State Code | Region/State/Territory Name | Unique Recipe Count | Notable Tribal / Local Examples |
|:---|:---|:---:|:---|
| **popular** | Pan-Indian / Highly Commercialized | 134 | *Chole Bhature, Palak Paneer, Masala Chai* |
| **AN / LAN** | Andaman & Nicobar Islands (Settler & Indigenous) | 8 | *Coconut Prawn Curry, Larop (Pandanus Dough)* |
| **AP / TG** | Andhra Pradesh & Telangana | 15 | *Gongura Mamsam, Karsi Dumpa (Koya Tuber)* |
| **AR** | Arunachal Pradesh (Adi, Nyishi, Apatani) | 8 | *Pasa (Raw Fish Soup), Pikey Pila* |
| **AS** | Assam (Bodo, Mising, Karbi) | 8 | *Onla (Rice Powder Curry), Samo Sobai (Snails)* |
| **BR / JH / OR** | Bihar, Jharkhand & Odisha (Santhal, Oraon, Saora) | 18 | *Leto, Rugra Curry, Kai Chutney* |
| **CT** | Chhattisgarh | 8 | *Chaprah (Red Ant Chutney), Sikiya Kheer* |
| **GA** | Goa | 5 | *Goan Fish Curry, Sorpotel, Lapsi* |
| **GJ / MP / RJ / MH** | West & Central (Dhodia, Baiga, Bhil, Gond, Warli) | 18 | *Paniya, Putpuda Chicken Stew, Dal Baati* |
| **HP** | Himachal Pradesh (Gaddi) | 11 | *Siddu, Chha Gosht (Buttermilk Mutton)* |
| **JK / ML / NL / MZ / MN** | Himalayan & Northeast Hills (Khasi, Naga, Mizo, Manipuri) | 42 | *Jadoh, Vawksa Rep, Smoked Pork with Axone* |
| **KA / KL / TN** | South India (Kodava, Nilgiri, Chenchu) | 16 | *Pandi Curry, Othidvar, Wild Greens Sambar* |
| **SK** | Sikkim | 9 | *Phagshapa (Pork Fat Stew), Gundruk ko Jhol* |
| **TR / UT / WB** | Tripura, Uttarakhand & West Bengal | 23 | *Chakhwi, Shile Kutu, Hisa Aara Sipi* |
<!-- STATS_END -->

---

## Relational Database Schema

The database uses a clean, normalized relational design. The datasets link together via the common key: **`Recipe Id`**.

```
                  ┌───────────────┐
                  │  recipes.csv  │  (One-to-Many on Recipe Id)
                  └───────┬───────┘
                          │
         ┌────────────────┼────────────────┐
         ▼                ▼                ▼
┌────────────────┐ ┌──────────────┐ ┌──────────────┐
│ingredients.csv │ │instructions. │ │  regions.csv │
└────────────────┘ └──────────────┘ └──────────────┘
```

### Data Dictionary

#### 1. `recipes.csv`
Contains the core metadata for each dish.
* `Recipe Id` (Primary Key): Text identifier.
* `Recipe Name English`: Standardized English name.
* `Recipe Name Local`: Local, regional, or tribal name.
* `Is Non Veg`: Boolean (`TRUE`/`FALSE`).
* `Total Active Time`: Hands-on prep time in seconds. `-1` denotes unavailable values (e.g., traditional fermented spirits).
* `Total Passive Time`: Hands-off resting/marination/cooking time in seconds.
* `Total Steps`: Integer count of chronological instructions.
* `Warning`: Important warnings (e.g., legal restrictions, toxicity management instructions).
* `Extra Info`: Additional historical, culinary, or cultural context.

#### 2. `ingredients.csv`
Lists ingredients required for each recipe.
* `Recipe Id` (Foreign Key): Link to `recipes.csv`.
* `Name`: Ingredient name.
* `Amount`: Quantity (or `-1` if "to taste" or unquantified).
* `Unit`: Units of measure (e.g., grams, cups, sets).
* `Is local`: Boolean (`TRUE`/`FALSE`). `TRUE` denotes items unique to regional ecosystems or tribal foraging (e.g., Sal leaves, specific wild yams, kola khar, red ants).

#### 3. `instructions.csv`
Defines chronological preparation steps.
* `Recipe Id` (Foreign Key): Link to `recipes.csv`.
* `Step Count`: Step order index.
* `Message`: Preparation/cooking instructions.
* `Active time`: Active duration for the step in seconds.
* `Passive time`: Passive duration for the step in seconds.

#### 4. `regions.csv`
Maps recipes to geographic and cultural classifications.
* `Recipe Id` (Foreign Key): Link to `recipes.csv`.
* `Region Code`: Standardized region/state mapping or `'popular'` designation.

---

## Known Placeholders & Data Integrity Notes

Users working with this dataset should keep the following design choices in mind:
1. **Unquantified Ingredients:** Ingredients added "to taste" or used for garnishing (such as salt, ghee for serving, or finishing herbs) are listed with an `Amount` value of `-1`.
2. **Traditional Fermented Beverages:** Items such as `handia`, `apong`, or `tadi` do not contain formal step-by-step measurements. These are documented in `recipes.csv` with `Total Steps` of `0` and times set to `-1` due to their reliance on highly specific, non-standardized herbal starter cultures.

---

## How to Query the Dataset (Python Example)

To reconstruct a complete recipe with its metadata, ingredients, and instructions using Pandas:

```python
import pandas as pd

# Load datasets
recipes = pd.read_csv('recipes.csv')
ingredients = pd.read_csv('ingredients.csv')
instructions = pd.read_csv('instructions.csv')

recipe_id = "pork_vindaloo"

# 1. Fetch metadata
meta = recipes[recipes['Recipe Id'] == recipe_id]
print(f"Recipe: {meta['Recipe Name English'].values[0]} ({meta['Recipe Name Local'].values[0]})")

# 2. Fetch ingredients
ing = ingredients[ingredients['Recipe Id'] == recipe_id]
print("\nIngredients:")
for _, row in ing.iterrows():
    amount = row['Amount'] if row['Amount'] != -1 else "To taste"
    unit = row['Unit'] if pd.notna(row['Unit']) else ""
    print(f"- {row['Name']}: {amount} {unit}")

# 3. Fetch instructions
steps = instructions[instructions['Recipe Id'] == recipe_id].sort_values('Step Count')
print("\nInstructions:")
for _, row in steps.iterrows():
    print(f"{row['Step Count']}. {row['Message']}")
```

---

## License & Contributions
This dataset is open for educational, sociological, and computational analysis. Contributions expanding regional tribal culinary data are welcome. Please submit a pull request with additions formatted to match the relational schema.