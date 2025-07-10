import tkinter as tk
from tkinter import messagebox, ttk
import pandas as pd
from prophet import Prophet
import matplotlib.pyplot as plt
from datetime import datetime

# Data initialization
try:
    df = pd.read_csv("finance_data.csv", parse_dates=["Date"])
except FileNotFoundError:
    try:
        df = pd.read_csv("supermarket_sales.csv", parse_dates=["Date"])
    except FileNotFoundError:
        df = pd.DataFrame(columns=["Date", "Revenue", "Expenses"])

# GUI Functions

def add_entry():
    try:
        date = datetime.strptime(date_entry.get(), "%Y-%m-%d")
        revenue = float(revenue_entry.get())
        expenses = float(expenses_entry.get())
        global df
        new_row = pd.DataFrame({"Date": [date], "Revenue": [revenue], "Expenses": [expenses]})
        df = pd.concat([df, new_row], ignore_index=True)
        df.to_csv("finance_data.csv", index=False)
        messagebox.showinfo("Success", "Entry added successfully.")
    except Exception as e:
        messagebox.showerror("Error", f"Invalid entry: {e}")

def show_summary(period="W"):
    global df
    if df.empty:
        messagebox.showinfo("No Data", "No entries available.")
        return
    df["Profit"] = df["Revenue"] - df["Expenses"]
    summary = df.groupby(pd.Grouper(key="Date", freq=period)).agg({"Revenue":"sum", "Expenses":"sum", "Profit":"sum"}).reset_index()
    summary_window = tk.Toplevel(root)
    summary_window.title("Summary")
    text = tk.Text(summary_window)
    text.pack()
    text.insert(tk.END, summary.to_string(index=False))

def forecast_profit(months=3):
    global df
    if df.empty:
        messagebox.showinfo("No Data", "No data for forecasting.")
        return
    df["Profit"] = df["Revenue"] - df["Expenses"]
    monthly = df.groupby(pd.Grouper(key="Date", freq="M")).agg({"Profit":"sum"}).reset_index()
    print("Monthly Profit:")
    print(monthly)
    
    if monthly.shape[0] < 2:
        messagebox.showwarning("Not enough data", "Need at least 2 months of data for forecasting.")
        return
    
    prophet_df = monthly.rename(columns={"Date": "ds", "Profit": "y"})
    m = Prophet()
    m.fit(prophet_df)
    future = m.make_future_dataframe(periods=months, freq="M")
    forecast = m.predict(future)
    print("Forecast:")
    print(forecast[["ds", "yhat", "yhat_lower", "yhat_upper"]].tail(months))
    m.plot(forecast)
    plt.title(f"Predicted Profit for Next {months} Months")
    plt.show()

def check_alerts():
    global df
    if df.empty:
        return
    last_week = df[df["Date"] >= df["Date"].max() - pd.Timedelta(days=7)]
    if not last_week.empty:
        avg_exp = last_week["Expenses"].mean()
        avg_profit = (last_week["Revenue"] - last_week["Expenses"]).mean()
        if avg_exp > 10000:
            messagebox.showwarning("Expense Alert", f"High expenses detected in last week: ₹{avg_exp:.2f}")
        if avg_profit < 0:
            messagebox.showwarning("Profit Alert", "Warning: Profit is negative in the last week.")

# Tkinter GUI 

root = tk.Tk()
root.title("Supermarket Finance Tracker")

# Inputs
tk.Label(root, text="Date (YYYY-MM-DD):").pack()
date_entry = tk.Entry(root)
date_entry.pack()

tk.Label(root, text="Revenue:").pack()
revenue_entry = tk.Entry(root)
revenue_entry.pack()

tk.Label(root, text="Expenses:").pack()
expenses_entry = tk.Entry(root)
expenses_entry.pack()

tk.Button(root, text="Add Entry", command=add_entry).pack(pady=5)
tk.Button(root, text="View Weekly Summary", command=lambda: show_summary("W")).pack()
tk.Button(root, text="View Monthly Summary", command=lambda: show_summary("M")).pack()
tk.Button(root, text="Forecast Profit (next 3 months)", command=lambda: forecast_profit(3)).pack()
tk.Button(root, text="Check Alerts", command=check_alerts).pack()

root.mainloop()

if __name__ == "__main__":
    launch_gui()