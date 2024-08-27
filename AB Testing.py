import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd


# Load the data
data = pd.read_csv(r'C:\Users\USER\Desktop\Algora\A_B TESTING\cookie_cats (1).csv')

# Inspect the data to ensure all columns are correctly read
print(data.info())
print(data.head())

# Ensure there are no missing values
data.dropna(inplace=True)
# Remove any duplicates
data.drop_duplicates(inplace=True)
# Ensure retention columns are boolean
data['retention_1'] = data['retention_1'].astype('bool')
data['retention_7'] = data['retention_7'].astype('bool')


# Split into CatA and CatB Group
catA_group = data[data['version'] == 'gate_30']
catB_group = data[data['version'] == 'gate_40']

print("catA Group (gate_30):")
print(catA_group.head())

print("CatB Group (gate_40):")
print(catB_group.head())

catA_retention_1 = catA_group['retention_1'].mean()
catB_retention_1 = catB_group['retention_1'].mean()
catA_retention_7 = catA_group['retention_7'].mean()
catB_retention_7 = catB_group['retention_7'].mean()

print(f'First Stage Day 1 Retention: {catA_retention_1}')
print(f'Second Stage Day 1 Retention: {catB_retention_1}')
print(f'First Stage Day 7 Retention: {catA_retention_7}')
print(f'Second Stage Day 7 Retention: {catB_retention_7}')

from scipy import stats

# Perform t-tests for retention rates
t_stat_1, p_val_1 = stats.ttest_ind(catA_group['retention_1'], catB_group['retention_1'])
t_stat_7, p_val_7 = stats.ttest_ind(catA_group['retention_7'], catB_group['retention_7'])

print(f'T-test results for Day 1 Retention: t-statistic={t_stat_1}, p-value={p_val_1}')
print(f'T-test results for Day 7 Retention: t-statistic={t_stat_7}, p-value={p_val_7}')

# Make recommendations based on the results
if p_val_1 < 0.05:
    print("The Day 1 retention change is significant. Consider keeping the barrier.")
else:
    print("The Day 1 retention change is not significant. Consider removing the barrier.")

if p_val_7 < 0.05:
    print("The Day 7 retention change is significant. Consider keeping the barrier.")
else:
    print("The Day 7 retention change is not significant. .")

    # Visualize the data
plt.figure(figsize=(12, 6))

# Plot retention rates for Day 1
plt.subplot(1, 2, 1)
sns.barplot(x=['gate_30', 'gate_40'], y=[catA_retention_1, catB_retention_1])
plt.title('Day 1 Retention Rates')
plt.ylabel('Retention Rate')

# Plot retention rates for Day 7
plt.subplot(1, 2, 2)
sns.barplot(x=['gate_30', 'gate_40'], y=[catA_retention_7, catB_retention_7])
plt.title('Day 7 Retention Rates')
plt.ylabel('Retention Rate')

plt.tight_layout()
plt.show()