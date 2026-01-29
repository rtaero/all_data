'''
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

# Initialize client using new SDK
client = Scorable(api_key=SCORABLE_API_KEY)

# Updated Judge ID (new SDK example)
JUDGE_ID = "2d44d810-1362-4f7b-92dc-9a727838a164"

# -----------------------
# INPUT CONTEXT (Anifrolumab FDA label)
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
# TARGET OUTPUT (Anifrolumab UI JSON)
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
# FIELD EXTRACTION MAPPING
# -----------------------
FIELDS_TO_EVALUATE = {
    "IndicationTabs.title": lambda o: {
        "IndicationTabs": {"title": o["IndicationTabs"]["title"]}
    },
    "IndicationUsage.label_text": lambda o: {
        "IndicationUsage": {"label_text": o["IndicationUsage"]["label_text"]}
    },
    "IndicationUsage.setting": lambda o: {
        "IndicationUsage": {"setting": o["IndicationUsage"]["setting"]}
    },
    "IndicationUsage.line_of_therapy": lambda o: {
        "IndicationUsage": {"line_of_therapy": o["IndicationUsage"]["line_of_therapy"]}
    },
    "IndicationUsage.regimen.components": lambda o: {
        "IndicationUsage": {
            "regimen": {"components": o["IndicationUsage"]["regimen"]["components"]}
        }
    },
    "TargetPopulation.age_range": lambda o: {
        "TargetPopulation": {"age_range": o["TargetPopulation"]["age_range"]}
    },
    "TargetPopulation.prior_therapy": lambda o: {
        "TargetPopulation": {"prior_therapy": o["TargetPopulation"]["prior_therapy"]}
    },
    "SafetyTolerability.common_AEs_20pct_plus": lambda o: {
        "SafetyTolerability": {
            "common_AEs_20pct_plus": o["SafetyTolerability"]["common_AEs_20pct_plus"]
        }
    }
}

# -----------------------
# EXECUTE FIELD-BY-FIELD EVALUATION
# -----------------------
all_results = []

print(f"Starting field-level evaluation for anifrolumab ({len(FIELDS_TO_EVALUATE)} fields)...")

for field_name, extractor in FIELDS_TO_EVALUATE.items():
    try:
        sliced_output = extractor(output_json)

        result = client.judges.run(
            judge_id=JUDGE_ID,
            response=json.dumps({
                "input_text": input_text,
                "output_json": sliced_output
            })
        )

        result_dict = result.model_dump()
        result_dict["evaluated_field"] = field_name
        all_results.append(result_dict)

        print(f"✅ Evaluated: {field_name}")

    except Exception as e:
        print(f"❌ Failed to evaluate {field_name}: {str(e)}")

# -----------------------
# SAVE RESULTS
# -----------------------
output_path = "anifrolumab_field_level_precision_results_v2.json"

with open(output_path, "w", encoding="utf-8") as f:
    json.dump(all_results, f, indent=2)

print(f"\nSuccess! Results saved to {output_path}")

''' 




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

# Initialize client using new SDK
client = Scorable(api_key=SCORABLE_API_KEY)

# Updated Judge ID (new SDK example)
JUDGE_ID = "2d44d810-1362-4f7b-92dc-9a727838a164"

# -----------------------
# INPUT CONTEXT (Anifrolumab FDA label)
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
# TARGET OUTPUT (Anifrolumab UI JSON)
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
# FIELD EXTRACTION MAPPING
# -----------------------
FIELDS_TO_EVALUATE = {
    "IndicationTabs.title": lambda o: {
        "IndicationTabs": {"title": o["IndicationTabs"]["title"]}
    },
    "IndicationUsage.label_text": lambda o: {
        "IndicationUsage": {"label_text": o["IndicationUsage"]["label_text"]}
    },
    "IndicationUsage.setting": lambda o: {
        "IndicationUsage": {"setting": o["IndicationUsage"]["setting"]}
    },
    "IndicationUsage.line_of_therapy": lambda o: {
        "IndicationUsage": {"line_of_therapy": o["IndicationUsage"]["line_of_therapy"]}
    },
    "IndicationUsage.regimen.components": lambda o: {
        "IndicationUsage": {
            "regimen": {"components": o["IndicationUsage"]["regimen"]["components"]}
        }
    },
    "TargetPopulation.age_range": lambda o: {
        "TargetPopulation": {"age_range": o["TargetPopulation"]["age_range"]}
    },
    "TargetPopulation.prior_therapy": lambda o: {
        "TargetPopulation": {"prior_therapy": o["TargetPopulation"]["prior_therapy"]}
    },
    "SafetyTolerability.common_AEs_20pct_plus": lambda o: {
        "SafetyTolerability": {
            "common_AEs_20pct_plus": o["SafetyTolerability"]["common_AEs_20pct_plus"]
        }
    }
}

# -----------------------
# EXECUTE FIELD-BY-FIELD EVALUATION
# -----------------------
all_results = []

print(f"Starting field-level evaluation for anifrolumab ({len(FIELDS_TO_EVALUATE)} fields)...")

for field_name, extractor in FIELDS_TO_EVALUATE.items():
    try:
        sliced_output = extractor(output_json)

        result = client.judges.run(
            judge_id=JUDGE_ID,
            response=json.dumps({
                "input_text": input_text,
                "output_json": sliced_output
            })
        )

        result_dict = result.model_dump()
        result_dict["evaluated_field"] = field_name
        all_results.append(result_dict)

        print(f"✅ Evaluated: {field_name}")

    except Exception as e:
        print(f"❌ Failed to evaluate {field_name}: {str(e)}")

# -----------------------
# SAVE RESULTS
# -----------------------
output_path = "anifrolumab_field_level_precision_results_v2.json"

with open(output_path, "w", encoding="utf-8") as f:
    json.dump(all_results, f, indent=2)

print(f"\nSuccess! Results saved to {output_path}")

