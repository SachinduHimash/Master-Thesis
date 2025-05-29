import matplotlib.pyplot as plt
import seaborn as sns

# Load the data
import pandas as pd

excel_file = pd.ExcelFile('data.xlsx')  
df = excel_file.parse('Sheet1')


# Select only the relevant similarity metric columns and drop NaNs
similarity_df = df[['JSD', 'Cosine Similarity', 'Euclidean Distance']].dropna()

# Create the pairplot with dot markers instead of crosses
sns.set(style="whitegrid")
pairplot = sns.pairplot(similarity_df, kind='scatter', plot_kws={'color': 'orange', 's': 30})
pairplot.fig.suptitle('Pairplot of Semantic Similarity Metrics (with Dots)', y=1.02)
plt.show()

