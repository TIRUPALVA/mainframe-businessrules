import os
import re
import pandas as pd

# Define folder path where COBOL files are uploaded
folder_path = "/mnt/data/cobol_files"

# Define column headers
columns = [
    "Rule Name", "Description", "Key Validations", "Error Conditions",
    "BIAN Domain", "Rule Type", "Domain Name", "Rule Classification"
]

# Helper to convert COBOL conditions into English
def convert_condition_to_english(condition):
    condition = condition.replace("=", "equals").replace(">", "greater than").replace("<", "less than")
    return f"Check if {condition.strip()}."

# Main logic to parse each COBOL line
def parse_cobol_line(file_name, line):
    rule_name = f"Rule from {file_name}"
    key_validations = line.strip()
    description = convert_condition_to_english(line)
    error_conditions = "N/A"

    # Basic keyword-driven BIAN mapping
    domain_mapping = {
        "NAME": "Party Data Management",
        "ACCT": "Product Management",
        "BAL": "Product Management",
        "OVERDRAFT": "Product Management"
    }
    bian_domain = next((v for k, v in domain_mapping.items() if k in line.upper()), "General Management")

    rule_type = "Data Validation Rule" if "SPACES" in line or "0" in line else "Business Rule"
    domain_name = bian_domain
    rule_classification = rule_type

    return {
        "Rule Name": rule_name,
        "Description": description,
        "Key Validations": key_validations,
        "Error Conditions": error_conditions,
        "BIAN Domain": bian_domain,
        "Rule Type": rule_type,
        "Domain Name": domain_name,
        "Rule Classification": rule_classification
    }

# Run extraction
all_rules = []

for file_name in os.listdir(folder_path):
    if file_name.endswith(".cbl"):
        with open(os.path.join(folder_path, file_name), 'r', encoding='utf-8', errors='ignore') as f:
            for line in f:
                if any(keyword in line.upper() for keyword in ["IF", "EVALUATE", "PERFORM"]):
                    all_rules.append(parse_cobol_line(file_name, line))

# Save to Excel
df = pd.DataFrame(all_rules, columns=columns)
df.to_excel("/mnt/data/extracted_business_rules.xlsx", index=False)

