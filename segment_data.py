import pandas as pd

# 1. Load Data & Clean
df = pd.read_csv("European_Bank (1).csv")
df = df.drop(columns=["Surname", "CustomerId"], errors="ignore")

# 2. Age Segmentation (<30, 30–45, 46–60, 60+)
bins_age = [0, 29, 45, 60, 150]
labels_age = ['<30', '30-45', '46-60', '60+']
df['Age_Group'] = pd.cut(df['Age'], bins=bins_age, labels=labels_age)

# 3. Credit Score Bands (Low <580, Medium 580-669, High 670+)
bins_credit = [0, 579, 669, 850]
labels_credit = ['Low', 'Medium', 'High']
df['Credit_Score_Band'] = pd.cut(df['CreditScore'], bins=bins_credit, labels=labels_credit)

# 4. Tenure Groups (New 0-2, Mid-term 3-5, Long-term 6-10)
bins_tenure = [-1, 2, 5, 15]
labels_tenure = ['New', 'Mid-term', 'Long-term']
df['Tenure_Group'] = pd.cut(df['Tenure'], bins=bins_tenure, labels=labels_tenure)

# 5. Balance Segments (Zero, Low <50k, High 50k+)
bins_balance = [-1, 0, 50000, 300000]
labels_balance = ['Zero-balance', 'Low-balance', 'High-balance']
df['Balance_Segment'] = pd.cut(df['Balance'], bins=bins_balance, labels=labels_balance)

# 6. Save the new segmented dataset
df.to_csv("European_Bank_Segmented.csv", index=False)
print("Success! Segmentation complete. European_Bank_Segmented.csv created.")