import pandas as pd 
import anthropic


column_names =[
    "age", "workclass", "fnlwgt", "education", "education-num",
    "marital-status", "occupation", "relationship", "race", "sex",
    "capital-gain", "capital-loss", "hours-per-week", "native-country",
    "income"
]
df = pd.read_csv("adult.data",header = None, names = column_names, sep = ", " , engine = "python" )


df["sex"] = df["sex"].str.strip()
df["income"] = df["income"].str.strip()
df["race"] = df["race"].str.strip()
protected_keywords = [
 "sex", "gender", "male", "female", "race", "ethnicity", "ethnic", "color", "age", "country", "nationality", "national", "origin", "native","religion", "religious", "faith", "disability", "disabled", "marital", "married","veteran", "military", "education", "degree", "language",
]

def detect_columns(df):
    demographic_cols = []
    for i in df.columns:
        if df[i].nunique()< 10 and i != "income" and any(keyword in i.lower() for keyword in protected_keywords):
            demographic_cols.append(i)
    return demographic_cols

def detect_outcomes(df):
    outcome_keywords = [
        "income", "salary", "hired", "hiring", "outcome",
        "decision", "result", "status", "approved",
        "rejected", "selected", "wage", "pay"
    ]
    outcome_cols = []
    for i in df.columns:
        for keyword in outcome_keywords:
            if i.lower() == keyword:
                outcome_cols.append(i)
                break
    return outcome_cols 
success_keywords = [
    "yes", "hired", "accepted", "approved",
    "selected", "passed", "success", "true",
    "1", ">50", "high", "pass"
]
def contains_success(value):
    for keyword in success_keywords:
        if keyword in str(value).lower():
            return True
    return False
def detect_bias(df,demographic_col,outcome_col):
    rates = {}
    findings = []
    x = df[demographic_col].unique()
    print(f"\n--- Analyzing bias for: {demographic_col} ---")
    for group in x :
        group_data =  df[df[demographic_col]==group]
        success_data = group_data[group_data[outcome_col].apply(contains_success)]

        success_rates = len(success_data)/len(group_data)
        rates[group] = success_rates
    best_rate = max(rates.values())
    if best_rate == 0:
        print(f"Could not detect any successful outcomes in {demographic_col}")
        return
    for group, rate in rates.items():
        ratio = rate/best_rate
        findings.append({
            "group": group,
            "rate": round(rate * 100, 2),
            "ratio": round(ratio * 100, 2),
            "demographic_col": demographic_col,
            "bias_detected": ratio < 0.80
        })
        if ratio < 0.80:
            print(f"\n⚠ WARNING: {group} — Ratio: {round(ratio * 100, 2)}%")
    return findings

demographic_cols = detect_columns(df)
outcome_col = detect_outcomes(df)[0]

all_findings = []
for col in demographic_cols:
    findings = detect_bias(df, col, outcome_col)
    all_findings.extend(findings)

print("\nAll findings:", all_findings)