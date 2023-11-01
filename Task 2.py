import sqlite3
import datetime

# Connect to the SQLite database
conn = sqlite3.connect("budget.db")
cursor = conn.cursor()

# Create the transactions table if it doesn't exist
cursor.execute("""
    CREATE TABLE IF NOT EXISTS transactions (
        id INTEGER PRIMARY KEY,
        category TEXT NOT NULL,
        amount REAL NOT NULL,
        date DATE NOT NULL,
        type TEXT CHECK (type IN ('Income', 'Expense')) NOT NULL
    )
""")
conn.commit()

def record_transaction(category, amount, transaction_type):
    cursor.execute("""
        INSERT INTO transactions (category, amount, date, type)
        VALUES (?, ?, ?, ?)
    """, (category, amount, datetime.date.today(), transaction_type))
    conn.commit()

def calculate_budget():
    cursor.execute("SELECT SUM(amount) FROM transactions WHERE type='Income'")
    income = cursor.fetchone()[0] or 0

    cursor.execute("SELECT SUM(amount) FROM transactions WHERE type='Expense'")
    expenses = cursor.fetchone()[0] or 0

    return income - expenses

def analyze_expenses():
    cursor.execute("SELECT category, SUM(amount) FROM transactions WHERE type='Expense' GROUP BY category")
    expenses_by_category = cursor.fetchall()

    if not expenses_by_category:
        print("No expense data available.")
    else:
        print("Expense Analysis:")
        for category, amount in expenses_by_category:
            print(f"{category}: ${amount:.2f}")

def main():
    while True:
        print("\nBudget Tracker Menu:")
        print("1. Record Income")
        print("2. Record Expense")
        print("3. Calculate Budget")
        print("4. Expense Analysis")
        print("5. Quit")

        choice = input("Enter your choice (1/2/3/4/5): ")

        if choice == "1":
            category = input("Enter income category: ")
            amount = float(input("Enter income amount: "))
            record_transaction(category, amount, "Income")
            print("Income recorded successfully!")
        elif choice == "2":
            category = input("Enter expense category: ")
            amount = float(input("Enter expense amount: "))
            record_transaction(category, amount, "Expense")
            print("Expense recorded successfully!")
        elif choice == "3":
            budget = calculate_budget()
            print(f"Remaining Budget: ${budget:.2f}")
        elif choice == "4":
            analyze_expenses()
        elif choice == "5":
            print("Goodbye!")
            break
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()
