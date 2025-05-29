
# import matplotlib.pyplot as plt
# import seaborn as sns

# # Load the data
# import pandas as pd

# excel_file = pd.ExcelFile('data.xlsx')  # Replace 'data.xlsx' with the actual path to your Excel file
# df = excel_file.parse('Sheet1')

# # Use the correct column names for plotting
# df_clean = df.dropna(subset=["LLM judge scores for original output", "LLM judge scores for refined output"])

# # Create a DataFrame suitable for seaborn boxplot
# boxplot_data = pd.DataFrame({
#     "Response Type": ["Original"] * len(df_clean) + ["Refined"] * len(df_clean),
#     "Average Judge Score": df_clean["LLM judge scores for original output"].tolist() + df_clean["LLM judge scores for refined output"].tolist()
# })

# # Plot with annotated values on the box
# plt.figure(figsize=(10, 6))
# ax = sns.boxplot(data=boxplot_data, x="Response Type", y="Average Judge Score", palette=["#66c2a5", "#fc8d62"])

# # Annotate boxplot with statistics
# medians = boxplot_data.groupby("Response Type")["Average Judge Score"].median()
# for i, type_ in enumerate(medians.index):
#     median_val = medians[type_]
#     ax.text(i, median_val + 0.1, f"Median: {median_val:.2f}", ha='center', color='black', fontsize=11)

# plt.title("Boxplot of Judge Scores for Original vs Refined Outputs")
# plt.tight_layout()
# plt.show()



import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# Load your data
excel_file = pd.ExcelFile('data.xlsx')  # Replace 'data.xlsx' with the actual path to your Excel file
df = excel_file.parse('Sheet1')

# Convert comma-separated judge scores to a float average
def parse_score(score_str):
    try:
        numbers = [float(x) for x in score_str.split(',')]
        return sum(numbers) / len(numbers)
    except Exception as e:
        print(f"Error parsing: {score_str} — {e}")
        return None

df["Average Judge Score"] = df["Average Judge Score"].apply(parse_score)

# Drop rows with invalid data
df = df.dropna(subset=["Average Judge Score"])

# Plot
sns.set(style="whitegrid")
ax = sns.boxplot(data=df, x="Response Type", y="Average Judge Score", palette=["#66c2a5", "#fc8d62"])

# Add medians
medians = df.groupby("Response Type")["Average Judge Score"].median()
for i, median in enumerate(medians):
    ax.text(i, median + 0.05, f'{median:.2f}', ha='center', color='black')

plt.title("Boxplot of Average Judge Scores by Response Type")
plt.tight_layout()
plt.show()