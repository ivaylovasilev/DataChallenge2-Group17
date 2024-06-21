
import matplotlib.pyplot as plt
import matplotlib
matplotlib.use('Agg')
import pandas as pd
import seaborn as sns



file_path = r"C:\Users\20224781\OneDrive - TU Eindhoven\Desktop\dc2\2019.csv"
data = pd.read_csv(file_path)


borough_columns = [col for col in data.columns if col.startswith('BOROUGH_')]
borough_names = [col.replace('BOROUGH_', '') for col in borough_columns]

# Extract numeric features (excluding the borough columns)
numeric_features = data.select_dtypes(include=['number']).drop(columns=['Unnamed: 0'])

# Create an empty DataFrame to store aggregated borough data
borough_aggregated = pd.DataFrame(index=borough_names, columns=numeric_features.columns)

# Aggregate the data for each borough by calculating the mean of each feature
for borough_col, borough_name in zip(borough_columns, borough_names):
    borough_data = data[data[borough_col]]
    borough_mean = borough_data[numeric_features.columns].mean()
    borough_aggregated.loc[borough_name] = borough_mean

# Calculate the correlation matrix between boroughs
correlation_matrix = borough_aggregated.T.corr()

correlation_matrix.to_csv('borough_correlation_matrix.csv')

# Plot the heatmap of the correlation matrix
plt.figure(figsize=(18, 15))
sns.heatmap(correlation_matrix, annot=True, fmt=".2f", cmap='coolwarm', linewidths=.5)
plt.title('Borough Correlation Matrix')
plt.savefig('borough_correlation_matrix.png')  # Save the figure
plt.show()