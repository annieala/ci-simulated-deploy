# data_analysis.py
# Task 1: Dataset Analysis and Insights

import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# -------------------------------
# 1. Load dataset
# -------------------------------
df = pd.read_csv("All_Diets.csv")

# -------------------------------
# 2. Handle missing data (fill missing values with mean)
# -------------------------------
df = df.fillna(df.mean(numeric_only=True))

# -------------------------------
# 3. Calculate the average macronutrient content for each diet type
# -------------------------------
avg_macros = df.groupby("Diet_type")[["Protein(g)", "Carbs(g)", "Fat(g)"]].mean()
print("\n=== Average Macronutrients per Diet Type ===")
print(avg_macros)

# -------------------------------
# 4. Top 5 protein-rich recipes per diet type
# -------------------------------
top_protein = df.sort_values("Protein(g)", ascending=False).groupby("Diet_type").head(5)
print("\n=== Top 5 Protein-Rich Recipes per Diet Type ===")
print(top_protein[["Diet_type", "Recipe_name", "Protein(g)", "Cuisine_type"]])

# -------------------------------
# 5. Diet type with highest protein
# -------------------------------
highest_protein = avg_macros["Protein(g)"].idxmax()
print("\nDiet type with highest protein content:", highest_protein)

# -------------------------------
# 6. Most common cuisine per diet type
# -------------------------------
common_cuisines = df.groupby("Diet_type")["Cuisine_type"].agg(lambda x: x.mode()[0])
print("\n=== Most Common Cuisines per Diet Type ===")
print(common_cuisines)

# -------------------------------
# 7. Add new metrics
# -------------------------------
df["Protein_to_Carbs_ratio"] = df["Protein(g)"] / df["Carbs(g)"]
df["Carbs_to_Fat_ratio"] = df["Carbs(g)"] / df["Fat(g)"]

print("\n=== Sample of New Metrics ===")
print(
    df[
        ["Diet_type", "Recipe_name", "Protein_to_Carbs_ratio", "Carbs_to_Fat_ratio"]
    ].head()
)

# -------------------------------
# 8. Visualizations
# -------------------------------

# Bar Chart – Average Protein
plt.figure(figsize=(8, 5))
sns.barplot(x=avg_macros.index, y=avg_macros["Protein(g)"])
plt.title("Average Protein by Diet Type")
plt.ylabel("Average Protein (g)")
plt.xticks(rotation=45)
plt.tight_layout()
plt.savefig("avg_protein_by_diet_type.png")
plt.show()

# Heatmap – Macronutrients
plt.figure(figsize=(8, 5))
sns.heatmap(avg_macros, annot=True, cmap="coolwarm", fmt=".2f")
plt.title("Average Macronutrients by Diet Type")
plt.tight_layout()
plt.savefig("avg_macros_heatmap.png")
plt.show()

# Scatter Plot – Top Protein Recipes
plt.figure(figsize=(8, 5))
sns.scatterplot(
    data=top_protein,
    x="Protein(g)",
    y="Carbs(g)",
    hue="Diet_type",
    style="Cuisine_type",
)
plt.title("Top 5 Protein-rich Recipes by Diet Type")
plt.tight_layout()
plt.savefig("top_protein_recipes_scatter.png")
plt.show()
