import pandas as pd
import os
from evidently.report import Report
from evidently.metrics import ColumnDriftMetric
from datetime import datetime

# Load and prepare data
df = pd.read_csv("data/bank.csv", sep=';')
df = pd.get_dummies(df, drop_first=True)
df = df.loc[:, df.nunique() > 1]  # Delete columns with a single value

reference_data = df.iloc[:2000].reset_index(drop=True)
current_data = df.iloc[2000:].reset_index(drop=True)

# Ensure same columns
common_cols = reference_data.columns.intersection(current_data.columns)
reference_data = reference_data[common_cols]
current_data = current_data[common_cols]

# We select some columns for drift evaluation (we avoid global errors)
columns_to_check = common_cols[:5] 

# Create Evidently report with individual metrics
metrics = [ColumnDriftMetric(column_name=col) for col in columns_to_check]

report = Report(metrics=metrics)
report.run(reference_data=reference_data, current_data=current_data)

# Save the report
os.makedirs("reports", exist_ok=True)
timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
report_path = f"reports/drift_report_{timestamp}.html"
report.save_html(report_path)

print(f"✅ Drift report generated: {report_path}")
