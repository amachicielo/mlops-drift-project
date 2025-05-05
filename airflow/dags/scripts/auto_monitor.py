import os
import pandas as pd
from evidently.report import Report
from evidently.metrics import ColumnDriftMetric
from datetime import datetime
import subprocess

# Load and prepare data
df = pd.read_csv("data/bank.csv", sep=';')
df = pd.get_dummies(df, drop_first=True)
df = df.loc[:, df.nunique() > 1]

reference_data = df.iloc[:2000].reset_index(drop=True)
current_data = df.iloc[2000:].reset_index(drop=True)

# Ensure same columns
common_cols = reference_data.columns.intersection(current_data.columns)
reference_data = reference_data[common_cols]
current_data = current_data[common_cols]

# Exclude problematic columns
excluded_columns = ['pdays', 'previous']
columns_to_check = [col for col in common_cols if col not in excluded_columns][:10]

# Create Evidently report with selected columns
metrics = [ColumnDriftMetric(column_name=col) for col in columns_to_check]
report = Report(metrics=metrics)
report.run(reference_data=reference_data, current_data=current_data)

# Evaluate drift
drift_detected = False
results = report.as_dict()

for metric_result in results['metrics']:
    column = metric_result['result'].get('column_name')
    drift = metric_result['result'].get('drift_detected', False)
    if drift:
        print(f"⚠️ Drift detected in the column: {column}")
        drift_detected = True

# Save HTML of the report
os.makedirs("reports", exist_ok=True)
timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
report_path = f"reports/drift_auto_report_{timestamp}.html"
report.save_html(report_path)
print(f"📊 Report saved: {report_path}")

# If there is drift, run training
if drift_detected:
    print("🔁 Retraining model due to drift...")
    subprocess.run(["python", "src/training/train_model.py"])
    print("✅ Retrained model.")
else:
    print("✅ No drift detected. The model is not retrained.")
