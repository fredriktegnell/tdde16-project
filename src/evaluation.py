import pandas as pd
from sklearn.metrics import classification_report

PREDICTIONS_PATH = "data/predictions.csv"
MERGED_PATH = "data/merged_data.csv"
data = pd.read_csv(MERGED_PATH)
predictions = pd.read_csv(PREDICTIONS_PATH)

actual_results = ['Home Win' if row['Home_Score'] > row['Away_Score'] else 'Away Win' if row['Home_Score'] < row['Away_Score'] else 'Draw' for index, row in data.iterrows()]

predicted_results = predictions['Prediction']

# Classification report
report = classification_report(actual_results, predicted_results, target_names=['Home Win', 'Away Win', 'Draw'])
print("\nClassification Report:\n", report)
