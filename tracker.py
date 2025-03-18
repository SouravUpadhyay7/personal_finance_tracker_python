# tracker.py

import sqlite3
import pandas as pd
from datetime import datetime

# Connect to SQLite database (or create it if it doesn't exist)
conn = sqlite3.connect('finance.db')
cursor = conn.cursor()

# Create table if not exists
cursor.execute('''
CREATE TABLE IF NOT EXISTS transactions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    type TEXT,
    amount REAL,
    category TEXT,
    date TEXT
)
''')
conn.commit()

def add_transaction(transaction_type):
    amount = float(input(f"Enter {transaction_type} amount: "))
    category = input(f"Enter {transaction_type} category: ")
    date = datetime.now().strftime("%Y-%m-%d")
    cursor.execute("INSERT INTO transactions (type, amount, category, date) VALUES (?, ?, ?, ?)",
                   (transaction_type, amount, category, date))
    conn.commit()
    print(f"{transaction_type.capitalize()} added successfully!\n")

def view_balance():
    cursor.execute("SELECT SUM(amount) FROM transactions WHERE type='Income'")
    total_income = cursor.fetchone()[0] or 0
    cursor.execute("SELECT SUM(amount) FROM transactions WHERE type='Expense'")
    total_expense = cursor.fetchone()[0] or 0
    print(f"Total Income: ₹{total_income}")
    print(f"Total Expenses: ₹{total_expense}")
    print(f"Net Savings: ₹{total_income - total_expense}\n")

def monthly_report():
    df = pd.read_sql_query("SELECT * FROM transactions", conn)
    if df.empty:
        print("No transactions found.\n")
        return
    df['date'] = pd.to_datetime(df['date'])
    df['month'] = df['date'].dt.strftime('%B %Y')
    report = df.groupby(['month', 'type'])['amount'].sum().unstack().fillna(0)
    report['Net Savings'] = report.get('Income', 0) - report.get('Expense', 0)
    print("\nMonthly Report:")
    print(report)
    print()

def main():
    while True:
        print("==== Personal Finance Tracker ====")
        print("1. Add Income")
        print("2. Add Expense")
        print("3. View Balance")
        print("4. Monthly Report")
        print("5. Exit")
        choice = input("Choose an option: ")

        if choice == '1':
            add_transaction('Income')
        elif choice == '2':
            add_transaction('Expense')
        elif choice == '3':
            view_balance()
        elif choice == '4':
            monthly_report()
        elif choice == '5':
            print("Exiting... Goodbye!")
            break
        else:
            print("Invalid option. Please try again.\n")

    conn.close()

if __name__ == "__main__":
    main()
