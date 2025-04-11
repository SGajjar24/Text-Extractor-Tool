import pandas as pd

# Create a sample DataFrame
data = {
    'Customer': ['Jane Doe', 'Robert Johnson', 'Maria Garcia'],
    'Order Number': ['ORD54321', 'ORD67890', 'ORD13579'],
    'Date': ['2025-04-02', '2025-04-03', '2025-04-04'],
    'Amount': [899.95, 1245.50, 349.99],
    'Status': ['Processing', 'Shipped', 'Delivered']
}

df = pd.DataFrame(data)

# Save to Excel file
df.to_excel('/home/ubuntu/text_extractor/sample_data/sample_orders.xlsx', index=False)

# Save to CSV file
df.to_csv('/home/ubuntu/text_extractor/sample_data/sample_orders.csv', index=False)

print("Sample Excel and CSV files created successfully.")
