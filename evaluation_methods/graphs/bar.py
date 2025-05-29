import matplotlib.pyplot as plt
import seaborn as sns

# Load the data
import pandas as pd

excel_file = pd.ExcelFile('data.xlsx') 
df = excel_file.parse('Sheet1')

# Clean the data
df_clean = df[['Topic', 'LLM judge Conclusion']].dropna()

# Normalize conclusion labels
def classify_conclusion(text):
    text = text.lower()
    if "better" in text:
        return "Refined better"
    elif "equal" in text or "same" in text:
        return "Equal"
    elif "worse" in text:
        return "Refined worse"
    else:
        return "Uncategorized"

df_clean['Judgment'] = df_clean['LLM judge Conclusion'].apply(classify_conclusion)

# Define pastel colors
pastel_palette = sns.color_palette("pastel")

grouped = df_clean.groupby(['Topic', 'Judgment']).size().unstack(fill_value=0)


# Re-plot using the pastel palette
plt.figure(figsize=(12, 8))
grouped.plot(
    kind='bar',
    stacked=True,
    color=pastel_palette[:len(grouped.columns)],  # match number of categories
    edgecolor='black'
)

# plt.title('Figure 1: LLM-as-a-Judge Outcomes by Topic')
plt.xlabel('Topic')
plt.ylabel('Count of Judgments')
plt.xticks(rotation=45, ha='right')
plt.legend(title='LLM Judgment')
plt.tight_layout()
plt.grid(axis='y', linestyle='--', alpha=0.7)
plt.show()


