import pandas as pd
import numpy as np
import plotly.graph_objects as go
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import StandardScaler

# Load the CSV file from the specified location
file_path = "/FILEPATH/data.csv"  # Replace with the correct path
data = pd.read_csv(file_path)

# Replace 'NULL' with NaN for proper handling of missing values
data.replace('NULL', np.nan, inplace=True)

# Convert the DataFrame from wide to long format
data_long = pd.melt(data, id_vars=['Analyst'], var_name='Month', value_name='Value')

# Convert 'Month' to a datetime object
data_long['Month'] = pd.to_datetime(data_long['Month'], format='%y-%b')

# Sort the data by Analyst and Month
data_long.sort_values(by=['Analyst', 'Month'], inplace=True)

# Function to forecast using linear regression
def forecast_linear_regression(data, periods=7):
    # Prepare the data
    data = data.dropna()
    data = data.reset_index(drop=True)
    data['Index'] = range(len(data))
    
    # Prepare the training data
    X = data['Index'].values.reshape(-1, 1)
    y = data['Value'].values
    
    # Fit the linear regression model
    model = LinearRegression()
    model.fit(X, y)
    
    # Predict future values
    future_indices = np.arange(len(data), len(data) + periods).reshape(-1, 1)
    future_values = model.predict(future_indices)
    
    # Ensure no negative values
    future_values[future_values < 0] = 0
    
    # Round to whole numbers
    future_values = np.round(future_values)
    
    # Create a DataFrame with future values
    last_date = data['Month'].iloc[-1]
    future_dates = pd.date_range(last_date, periods=periods + 1, freq='M')[1:]
    forecast_df = pd.DataFrame({'Month': future_dates, 'Value': future_values})
    
    return forecast_df

# Forecast the next 7 months for each analyst
forecasts = {}
for analyst in data['Analyst'].unique():
    analyst_data = data_long[data_long['Analyst'] == analyst][['Month', 'Value']]
    forecast = forecast_linear_regression(analyst_data)
    forecast.set_index('Month', inplace=True)
    forecasts[analyst] = forecast['Value']

# Combine the forecasts into a DataFrame
forecast_df = pd.DataFrame(forecasts)

# Convert the forecasted data back to wide format
forecast_wide = forecast_df.T
forecast_wide.columns = [f"{date.strftime('%b-%y')}" for date in forecast_df.index]

# Combine original and forecasted data
combined_df = pd.concat([data.set_index('Analyst'), forecast_wide], axis=1)

# Prepare the data for the table
combined_df.reset_index(inplace=True)
table_data = combined_df.values.tolist()
header = combined_df.columns.tolist()

# Determine which cells are forecasted
forecast_columns = forecast_wide.columns.tolist()

# Create color-scaled table with subtle color for forecasted cells
fig = go.Figure(data=[go.Table(
    header=dict(values=header,
                fill_color='paleturquoise',
                align='left'),
    cells=dict(values=[combined_df[col] for col in combined_df.columns],
               fill_color=[
                   ['#FFFFFF'] * len(combined_df) if col not in forecast_columns else ['#E0FFFF'] * len(combined_df)
                   for col in combined_df.columns
               ],
               align='left'))
])

fig.update_layout(
    title="Analyst Performance Forecast",
    title_font=dict(size=24, family='Arial, sans-serif', color='black'),
    template="plotly_white"
)

fig.show()
