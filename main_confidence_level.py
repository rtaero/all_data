import json

# Paths
input_path = "anifrolumab_true_field_level_precision_results_detailed.json"
output_path = "anifrolumab_field_level_precision_results_v2_with_confidence.json"

# Load JSON
with open(input_path, "r", encoding="utf-8") as f:
    data = json.load(f)

# Process
for item in data:
    for res in item.get("evaluator_results", []):
        score = res.get("score", 0.0)
        if score == 0.0:
            res["confidence_level"] = "Low"
        elif 0.0 < score < 0.7:
            res["confidence_level"] = "Medium"
        else:
            res["confidence_level"] = "High"

# Save output
with open(output_path, "w", encoding="utf-8") as f:
    json.dump(data, f, indent=2)
