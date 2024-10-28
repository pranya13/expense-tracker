import tkinter as tk
from tkinter import ttk, messagebox, Scrollbar
import pandas as pd
from matplotlib import pyplot as plt
from datetime import datetime

# tkinter window
root = tk.Tk()
root.geometry("800x600")
root.title("💸 Expense Tracker")
root.configure(background="#F5F5F5")

item_list = []
category_budget = {
    "Food": 3000,
    "Transport": 2000,
    "Entertainment": 1500,
    "Others": 1000
}

def add_item():
    item = item_txt.get()
    cost = cost_txt.get()
    category = category_combo.get()
    date = date_txt.get()
    
    if not item or not cost or not category or not date:
        messagebox.showerror("Input Error", "Please fill in all fields before adding an item! 🚫")
        return

    try:
        cost_value = int(cost)
    except ValueError:
        messagebox.showerror("Invalid Cost", "Please enter a valid cost amount! 💲")
        return

    try:
        date_obj = datetime.strptime(date, "%Y-%m-%d")
    except ValueError:
        messagebox.showerror("Invalid Date", "Please enter the date in YYYY-MM-DD format 🗓️")
        return

    single_item = {"Date": date, "Item": item, "Cost": cost_value, "Category": category}
    item_list.append(single_item)
    
    single_item_lbl = tk.Label(frame2_inner, text=f"{date}   {item}     {cost_value}     {category} 🏷️",
                               bg="#F5F5F5", fg="#424242", font=("Verdana", 10))
    single_item_lbl.pack(pady=1)

    update_budget_overview()
    
def clear_item():
    item_txt.delete(0, "end")
    cost_txt.delete(0, "end")
    category_combo.set("")
    date_txt.delete(0, "end")

def analyse():
    if not item_list:
        messagebox.showinfo("Analysis", "No expenses to analyze! Please add some items first. 📝")
        return

    df = pd.DataFrame(item_list)

    # Bar chart for expenditure by items
    plt.figure(figsize=(8, 4))
    plt.bar(df["Item"], df["Cost"], color="#42A5F5", width=0.4)
    plt.ylabel("💲 Cost of Items")
    plt.xlabel("🛍️ Items Purchased")
    plt.title("📊 Expenditure Tracker Analysis")
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()

    # Budget vs Expenses per category
    plt.figure(figsize=(8, 4))
    spent_per_category = df.groupby("Category")["Cost"].sum()
    categories = spent_per_category.index
    budget_values = [category_budget.get(cat, 0) for cat in categories]
    expenses = spent_per_category.values

    plt.bar(categories, budget_values, color="#66BB6A", width=0.4, label="Budget")
    plt.bar(categories, expenses, color="#EF5350", width=0.4, label="Spent", alpha=0.7)
    plt.ylabel("💵 Amount")
    plt.title("Budget vs Expenses by Category")
    plt.legend()
    plt.tight_layout()
    plt.show()

    # Datewise expenditure analysis
    plt.figure(figsize=(8, 4))
    date_totals = df.groupby("Date")["Cost"].sum()
    plt.plot(date_totals.index, date_totals.values, color="#29B6F6", marker="o", linestyle="-")
    plt.ylabel("💸 Total Expenditure")
    plt.xlabel("📅 Date")
    plt.title("📈 Daily Expenditure Over Time")
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()

    # Pie chart for expenses by category
    plt.figure(figsize=(6, 6))
    plt.pie(expenses, labels=categories, autopct='%1.1f%%', startangle=140, colors=["#42A5F5", "#66BB6A", "#FF7043", "#FFCA28"])
    plt.title("🧁 Expense Distribution by Category")
    plt.axis('equal')
    plt.tight_layout()
    plt.show()

def update_budget_overview():
    budget_summary_text.config(state="normal")  # Enable editing to update text
    budget_summary_text.delete("1.0", "end")
    df = pd.DataFrame(item_list)
    spent_per_category = df.groupby("Category")["Cost"].sum()
    
    for category, budget in category_budget.items():
        spent = spent_per_category.get(category, 0)
        remaining = budget - spent
        status = "🔥 Over Budget" if remaining < 0 else "✅ Within Budget"
        
        budget_summary_text.insert("end", f"{category} - Budget: {budget}, Spent: {spent}, Remaining: {remaining} ({status})\n")
    
    budget_summary_text.config(state="disabled")  # Disable editing again

# Screen details
title_lbl = tk.Label(root, text="💸 EXPENSE TRACKER", bg="#F5F5F5", fg="#1A237E", font=("Verdana Bold", 16))
title_lbl.pack(pady=10)

input_frame = tk.Frame(root, bg="#E3F2FD")
input_frame.pack(pady=5)

# Date input
date_lbl = tk.Label(input_frame, text="📅 Date (YYYY-MM-DD):", bg="#F5F5F5", fg="#424242", font=("Verdana", 10))
date_lbl.grid(row=0, column=0, padx=5, sticky="e")
date_txt = tk.Entry(input_frame, font=("Verdana", 10), width=20)
date_txt.grid(row=0, column=1, padx=5, pady=5)

# Item input
item_lbl = tk.Label(input_frame, text="🛍️ Item:", bg="#F5F5F5", fg="#424242", font=("Verdana", 10))
item_lbl.grid(row=1, column=0, padx=5, sticky="e")
item_txt = tk.Entry(input_frame, font=("Verdana", 10), width=20)
item_txt.grid(row=1, column=1, padx=5, pady=5)

# Cost input
cost_lbl = tk.Label(input_frame, text="💵 Cost:", bg="#F5F5F5", fg="#424242", font=("Verdana", 10))
cost_lbl.grid(row=2, column=0, padx=5, sticky="e")
cost_txt = tk.Entry(input_frame, font=("Verdana", 10), width=20)
cost_txt.grid(row=2, column=1, padx=5, pady=5)

# Category dropdown
category_lbl = tk.Label(input_frame, text="🏷️ Category:", bg="#F5F5F5", fg="#424242", font=("Verdana", 10))
category_lbl.grid(row=3, column=0, padx=5, sticky="e")
category_combo = ttk.Combobox(input_frame, values=["Food", "Transport", "Entertainment", "Others"], font=("Verdana", 10), width=18)
category_combo.grid(row=3, column=1, padx=5, pady=5)

# Button Frame
button_frame = tk.Frame(root, bg="#F5F5F5")
button_frame.pack(pady=10)

add_btn = tk.Button(button_frame, text="➕ ADD ITEM", bg="#1E88E5", fg="#ffffff", font=("Verdana", 10), command=add_item)
add_btn.pack(padx=5, pady=5, side=tk.LEFT)
clear_btn = tk.Button(button_frame, text="🧹 CLEAR", bg="#1E88E5", fg="#ffffff", font=("Verdana", 10), command=clear_item)
clear_btn.pack(side=tk.RIGHT)

# Analyse Button
analyse_btn = tk.Button(button_frame, text="📊 ANALYSE", bg="#3949AB", fg="#ffffff", font=("Verdana Bold", 10), command=analyse)
analyse_btn.pack(pady=5)

display_lbl = tk.Label(root, text="🧾 Expenses", bg="#F5F5F5", fg="#1A237E", font=("Verdana Bold", 12))
display_lbl.pack(pady=10)

# Expense display frame with scroll bar
frame2 = tk.Frame(root, bg="#F5F5F5")
frame2.pack(fill=tk.BOTH, expand=True, pady=5)

canvas = tk.Canvas(frame2, bg="#F5F5F5")
canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

scrollbar = Scrollbar(frame2, orient="vertical", command=canvas.yview)
scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

frame2_inner = tk.Frame(canvas, bg="#F5F5F5")
canvas.create_window((0, 0), window=frame2_inner, anchor="nw")

canvas.configure(yscrollcommand=scrollbar.set)

def on_frame_configure(event):
    canvas.configure(scrollregion=canvas.bbox("all"))

frame2_inner.bind("<Configure>", on_frame_configure)

heading_lbl = tk.Label(frame2_inner, text="Date       Item       Cost       Category",
                       bg="#F5F5F5", fg="#1A237E", font=("Verdana Bold", 8))
heading_lbl.pack(pady=1)

# Budget Summary
budget_summary_lbl = tk.Label(root, text="💰 Budget Overview", bg="#E8F0F2", fg="#1A237E", font=("Verdana Bold", 14))
budget_summary_lbl.pack(pady=5)

# Enhanced Budget Summary Text Widget
budget_summary_text = tk.Text(root, width=70, height=6, font=("Verdana", 11), bg="#FFE0B2", fg="#D84315", relief="flat", wrap="word")
budget_summary_text.insert("1.0", "Budget Overview will appear here after adding items.")
budget_summary_text.tag_configure("center", justify="center")
budget_summary_text.tag_add("center", "1.0", "end")
budget_summary_text.config(state="disabled")  # Initial state disabled to prevent edits
budget_summary_text.pack(pady=10, padx=10)

root.mainloop()
