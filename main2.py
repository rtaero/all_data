# pip install scorable python-dotenv

import os
import json
from scorable import Scorable
from dotenv import load_dotenv

# -----------------------
# ENV + CLIENT SETUP
# -----------------------
load_dotenv()

SCORABLE_API_KEY = os.getenv("SCORABLE_API_KEY")
if not SCORABLE_API_KEY:
    raise ValueError("SCORABLE_API_KEY not found in .env")

client = Scorable(api_key=SCORABLE_API_KEY)

JUDGE_ID = "2d44d810-1362-4f7b-92dc-9a727838a164"

# -----------------------
# INPUT CONTEXT
# -----------------------
input_text = (
    "1 INDICATIONS AND USAGE: SAPHNELO is indicated for the treatment of adult "
    "patients with moderate to severe systemic lupus erythematosus (SLE), who "
    "are receiving background immunosuppressive therapy. Limitations of Use: "
    "SAPHNELO is not recommended for use in patients with severe active lupus "
    "nephritis or severe active central nervous system lupus. "
    "2 DOSAGE AND ADMINISTRATION: The recommended dosage of SAPHNELO is 300 mg "
    "administered as an intravenous infusion over a 30-minute period every 4 weeks. "
    "6 ADVERSE REACTIONS: The most common adverse reactions (incidence ≥ 20%) "
    "were nasopharyngitis, upper respiratory tract infection, and infusion-related "
    "reactions. 8.4 Pediatric Use: The safety and efficacy of SAPHNELO in pediatric "
    "patients have not been established."
)

# -----------------------
# OUTPUT JSON
# -----------------------
output_json = {
    "IndicationTabs": {
        "title": "Systemic Lupus Erythematosus"
    },
    "IndicationUsage": {
        "label_text": (
            "SAPHNELO is indicated for the treatment of adult patients with moderate "
            "to severe systemic lupus erythematosus (SLE), who are receiving "
            "background immunosuppressive therapy."
        ),
        "setting": "Moderate to severe disease state",
        "line_of_therapy": "Add-on to background immunosuppressive therapy",
        "regimen": {
            "components": ["Anifrolumab"]
        }
    },
    "TargetPopulation": {
        "age_range": "Adult patients",
        "prior_therapy": "Receiving background immunosuppressive therapy"
    },
    "SafetyTolerability": {
        "common_AEs_20pct_plus": [
            "Nasopharyngitis",
            "Upper respiratory tract infection",
            "Infusion-related reactions"
        ]
    }
}

# -----------------------
# RECURSIVE FIELD FLATTENER
# -----------------------
def extract_leaf_fields(obj, parent_key=""):
    fields = {}
    if isinstance(obj, dict):
        for k, v in obj.items():
            full_key = f"{parent_key}.{k}" if parent_key else k
            fields.update(extract_leaf_fields(v, full_key))
    else:
        fields[parent_key] = obj
    return fields

# -----------------------
# CREATE FIELD-LEVEL SLICES
# -----------------------
leaf_fields = extract_leaf_fields(output_json)

print(f"Discovered {len(leaf_fields)} leaf metadata fields")

# -----------------------
# EXECUTE FIELD-BY-FIELD EVALUATION
# -----------------------
all_results = []

for field_path, field_value in leaf_fields.items():

    # rebuild minimal JSON containing only this field
    keys = field_path.split(".")
    sliced_output = current = {}

    for key in keys[:-1]:
        current[key] = {}
        current = current[key]

    current[keys[-1]] = field_value

    try:
        result = client.judges.run(
            judge_id=JUDGE_ID,
            response=json.dumps({
                "input_text": input_text,
                "output_json": sliced_output
            })
        )

        result_dict = result.model_dump()
        result_dict["evaluated_field"] = field_path
        all_results.append(result_dict)

        print(f"✅ Evaluated: {field_path}")

    except Exception as e:
        print(f"❌ Failed: {field_path} → {str(e)}")

# -----------------------
# SAVE RESULTS
# -----------------------
output_path = "anifrolumab_true_field_level_precision_results_detailed.json"

with open(output_path, "w", encoding="utf-8") as f:
    json.dump(all_results, f, indent=2)

print(f"\nSuccess! Results saved to {output_path}")
