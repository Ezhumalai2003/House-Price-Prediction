import tkinter as tk
from tkinter import messagebox
import numpy as np
from sklearn.linear_model import LinearRegression

# Dummy model training data
X_train = np.array([
    [2000, 1, 3, 1500, 1],  # Urban
    [1995, 1, 2, 1200, 0],  # Rural
    [2010, 1, 4, 2000, 1],  # Urban
    [1985, 0, 3, 1600, 0],  # Rural
    [2020, 1, 5, 2500, 1],  # Urban
    [1975, 0, 2, 1000, 0]   # Rural
])
y_train = np.array([500000, 150000, 600000, 180000, 700000, 120000])  # Example prices in USD

# Create and train a simple linear regression model
model = LinearRegression()
model.fit(X_train, y_train)

# Static exchange rate from USD to INR
exchange_rate = 83.0  # Example rate: 1 USD = 83 INR

def predict_price(when_built, condition, bedrooms, sqft, location):
    condition_flag = 1 if condition.lower() == 'usable' else 0
    location_flag = 1 if location.lower() == 'urban' else 0
    features = np.array([[when_built, condition_flag, bedrooms, sqft, location_flag]])
    predicted_price_usd = model.predict(features)[0]
    
    # Apply a discount if condition is "Not Usable"
    if condition.lower() == 'not usable':
        discount_factor = 0.7  # Example discount factor, adjust as needed
        predicted_price_usd *= discount_factor
    
    predicted_price_inr = predicted_price_usd * exchange_rate
    return predicted_price_inr

def on_predict():
    try:
        when_built = int(entry_when_built.get())
        condition = entry_condition.get()
        bedrooms = int(entry_bedrooms.get())
        sqft = int(entry_sqft.get())
        location = entry_location.get()
        
        price_inr = predict_price(when_built, condition, bedrooms, sqft, location)
        label_result.config(text=f"Predicted Price: ₹{price_inr:,.2f}")
    except ValueError as e:
        messagebox.showerror("Input Error", f"Invalid input: {e}")

def on_refresh():
    entry_when_built.delete(0, tk.END)
    entry_condition.delete(0, tk.END)
    entry_bedrooms.delete(0, tk.END)
    entry_sqft.delete(0, tk.END)
    entry_location.delete(0, tk.END)
    label_result.config(text="Predicted Price: ₹0.00")

# Create the main window
root = tk.Tk()
root.title("House Price Predictor")

# Create and place widgets
tk.Label(root, text="When was the house built (Year):").grid(row=0, column=0, padx=10, pady=10)
entry_when_built = tk.Entry(root)
entry_when_built.grid(row=0, column=1, padx=10, pady=10)

tk.Label(root, text="Condition of the house (Usable/Not Usable):").grid(row=1, column=0, padx=10, pady=10)
entry_condition = tk.Entry(root)
entry_condition.grid(row=1, column=1, padx=10, pady=10)

tk.Label(root, text="Number of Bedrooms:").grid(row=2, column=0, padx=10, pady=10)
entry_bedrooms = tk.Entry(root)
entry_bedrooms.grid(row=2, column=1, padx=10, pady=10)

tk.Label(root, text="Total Square Feet:").grid(row=3, column=0, padx=10, pady=10)
entry_sqft = tk.Entry(root)
entry_sqft.grid(row=3, column=1, padx=10, pady=10)

tk.Label(root, text="Location (Urban/Rural):").grid(row=4, column=0, padx=10, pady=10)
entry_location = tk.Entry(root)
entry_location.grid(row=4, column=1, padx=10, pady=10)

tk.Button(root, text="Predict Price", command=on_predict).grid(row=5, column=0, padx=10, pady=10)
tk.Button(root, text="Refresh", command=on_refresh).grid(row=5, column=1, padx=10, pady=10)

label_result = tk.Label(root, text="Predicted Price: ₹0.00")
label_result.grid(row=6, column=0, columnspan=2, padx=10, pady=10)

root.mainloop()
