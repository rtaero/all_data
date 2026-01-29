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

# Initialize the new SDK client
client = Scorable(api_key=SCORABLE_API_KEY)

# Ensure this ID matches your specific Judge in the Scorable dashboard
JUDGE_ID = "dfacda24-5572-46f8-aedf-43a62fb65ca5"

# -----------------------
# INPUT CONTEXT (Source Text)
# -----------------------
input_text = (
    "1 INDICATIONS AND USAGE: 1.1 Melanoma. "
    "KEYTRUDA® (pembrolizumab) is indicated for the treatment of patients "
    "with unresectable or metastatic melanoma. "
    "DOSAGE AND ADMINISTRATION: 200 mg every 3 weeks. "
    "CLINICAL STUDIES: KEYNOTE-006 evaluated OS and PFS. "
    "ADVERSE REACTIONS: fatigue (28%), diarrhea (26%), rash (24%)."
)

# -----------------------
# TARGET OUTPUT (To be evaluated)
# -----------------------
output_json = {
    "IndicationTabs": {"title": "Melanoma"},
    "IndicationUsage": {
        "label_text": "KEYTRUDA® (pembrolizumab) is indicated for the treatment of patients with unresectable or metastatic melanoma.",
        "setting": "Unresectable or Metastatic",
        "line_of_therapy": None,
        "histology": "Melanoma",
        "biomarkers": None,
        "regimen": {
            "components": ["pembrolizumab"],
            "dose_keytruda": "200 mg every 3 weeks"
        }
    },
    "TargetPopulation": {
        "age_range": "Adult and pediatric (12 years and older)",
        "sex": None,
        "ECOG_status": None
    },
    "Efficacy": {
        "PrimaryEndpoints": {
            "trial": "KEYNOTE-006",
            "endpoints": ["Overall Survival", "Progression-Free Survival"]
        }
    },
    "SafetyTolerability": {
        "common_AEs_20pct_plus": ["fatigue", "diarrhea", "rash"]
    }
}

# -----------------------
# FIELD EXTRACTION MAPPING
# -----------------------
FIELDS_TO_EVALUATE = {
    "IndicationTabs.title": lambda o: {"IndicationTabs": {"title": o["IndicationTabs"]["title"]}},
    "IndicationUsage.label_text": lambda o: {"IndicationUsage": {"label_text": o["IndicationUsage"]["label_text"]}},
    "IndicationUsage.setting": lambda o: {"IndicationUsage": {"setting": o["IndicationUsage"]["setting"]}},
    "IndicationUsage.line_of_therapy": lambda o: {"IndicationUsage": {"line_of_therapy": o["IndicationUsage"]["line_of_therapy"]}},
    "IndicationUsage.histology": lambda o: {"IndicationUsage": {"histology": o["IndicationUsage"]["histology"]}},
    "IndicationUsage.regimen.dose_keytruda": lambda o: {
        "IndicationUsage": {"regimen": {"dose_keytruda": o["IndicationUsage"]["regimen"]["dose_keytruda"]}}
    },
    "SafetyTolerability.common_AEs_20pct_plus": lambda o: {
        "SafetyTolerability": {"common_AEs_20pct_plus": o["SafetyTolerability"]["common_AEs_20pct_plus"]}
    }
}

# -----------------------
# EXECUTE EVALUATIONS
# -----------------------
all_results = []

print(f"Starting field-level evaluation for {len(FIELDS_TO_EVALUATE)} fields...")

for field_name, extractor in FIELDS_TO_EVALUATE.items():
    try:
        # 1. Prepare the sliced JSON for the specific field
        sliced_output = extractor(output_json)

        # 2. Call the judge using the NEW SDK syntax
        # The 'response' parameter takes a string. We wrap our inputs in a single JSON string.
        result = client.judges.run(
            judge_id=JUDGE_ID,
            response=json.dumps({
                "input_text": input_text,
                "output_json": sliced_output
            })
        )

        # 3. Use model_dump() to convert the response object to a dictionary
        result_dict = result.model_dump()
        
        # 4. Attach the field name for easier tracking in the final report
        result_dict["evaluated_field"] = field_name
        all_results.append(result_dict)
        
        print(f"✅ Evaluated: {field_name}")

    except Exception as e:
        print(f"❌ Failed to evaluate {field_name}: {str(e)}")

# -----------------------
# SAVE RESULTS
# -----------------------
output_path = "melanoma_precision_results.json"
with open(output_path, "w", encoding="utf-8") as f:
    json.dump(all_results, f, indent=2)

print(f"\nSuccess! Results saved to {output_path}")