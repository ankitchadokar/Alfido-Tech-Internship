import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import sqlite3


class PersonalFinanceTracker:
    def __init__(self):
        self.data = pd.DataFrame(columns=['Date', 'Category', 'Type', 'Amount'])
        self.budget = {}
        self.db_conn = None

    def add_transaction(self, date, category, transaction_type, amount):
        if transaction_type not in ['Income', 'Expense']:
            print("Transaction type must be either 'Income' or 'Expense'.")
            return
        new_transaction = {'Date': date, 'Category': category, 'Type': transaction_type, 'Amount': amount}
        self.data = pd.concat([self.data, pd.DataFrame([new_transaction])], ignore_index=True)
        print("Transaction added successfully!")

    def set_budget_goal(self, category, budget):
        self.budget[category] = budget
        print(f"Budget goal of {budget} set for {category}.")

    def visualize_data(self):
        if self.data.empty:
            print("No data available to visualize.")
            return

        # Spending by category
        expense_data = self.data[self.data['Type'] == 'Expense']
        category_summary = expense_data.groupby('Category')['Amount'].sum()

        if not category_summary.empty:
            plt.figure(figsize=(10, 5))
            category_summary.plot(kind='bar', color='skyblue')
            plt.title('Expenses by Category')
            plt.xlabel('Category')
            plt.ylabel('Amount')
            plt.show()
        else:
            print("No expense data available for visualization.")

        # Income vs. Expenses
        summary = self.data.groupby('Type')['Amount'].sum()
        if len(summary) > 0:
            plt.figure(figsize=(6, 6))
            summary.plot(kind='pie', autopct='%1.1f%%', startangle=90, colors=['green', 'red'])
            plt.title('Income vs. Expenses')
            plt.ylabel('')  # Hides y-label for pie chart
            plt.show()

    def visualize_budget_progress(self):
        if not self.budget:
            print("No budget goals set.")
            return

        progress = {category: self.data[self.data['Category'] == category]['Amount'].sum()
                    for category in self.budget.keys()}
        budget_df = pd.DataFrame({'Category': self.budget.keys(),
                                  'Spent': progress.values(),
                                  'Budget': self.budget.values()})
        budget_df.set_index('Category', inplace=True)
        budget_df.plot(kind='bar', figsize=(10, 5), color=['orange', 'blue'])
        plt.title('Budget Progress')
        plt.xlabel('Category')
        plt.ylabel('Amount')
        plt.show()

    def export_to_csv(self, filename='finance_data.csv'):
        self.data.to_csv(filename, index=False)
        print(f"Data exported to {filename}")

    def connect_to_db(self, db_name='finance_tracker.db'):
        self.db_conn = sqlite3.connect(db_name)
        self.data.to_sql('transactions', self.db_conn, if_exists='replace', index=False)
        print(f"Data saved to database {db_name}")

    def close_db(self):
        if self.db_conn:
            self.db_conn.close()
            print("Database connection closed.")

    def summary_report(self):
        if self.data.empty:
            print("No data available to summarize.")
            return

        print("\nSummary Report:")
        total_income = self.data[self.data['Type'] == 'Income']['Amount'].sum()
        total_expense = self.data[self.data['Type'] == 'Expense']['Amount'].sum()
        print(f"Total Income: {total_income}")
        print(f"Total Expenses: {total_expense}")
        print(f"Net Savings: {total_income - total_expense}")


# Interactive Menu
if __name__ == "__main__":
    tracker = PersonalFinanceTracker()

    while True:
        print("\nPersonal Finance Tracker")
        print("1. Add Transaction")
        print("2. Set Budget Goal")
        print("3. Visualize Data")
        print("4. Visualize Budget Progress")
        print("5. Generate Summary Report")
        print("6. Export to CSV")
        print("7. Save to Database")
        print("8. Exit")

        choice = input("Enter your choice: ")
        if choice == '1':
            date = input("Enter date (YYYY-MM-DD): ")
            category = input("Enter category: ")
            transaction_type = input("Enter type (Income/Expense): ")
            amount = float(input("Enter amount: "))
            tracker.add_transaction(date, category, transaction_type, amount)
        elif choice == '2':
            category = input("Enter category: ")
            budget = float(input("Enter budget amount: "))
            tracker.set_budget_goal(category, budget)
        elif choice == '3':
            tracker.visualize_data()
        elif choice == '4':
            tracker.visualize_budget_progress()
        elif choice == '5':
            tracker.summary_report()
        elif choice == '6':
            filename = input("Enter filename (default: finance_data.csv): ") or 'finance_data.csv'
            tracker.export_to_csv(filename)
        elif choice == '7':
            db_name = input("Enter database name (default: finance_tracker.db): ") or 'finance_tracker.db'
            tracker.connect_to_db(db_name)
        elif choice == '8':
            tracker.close_db()
            print("Exiting... Goodbye!")
            break
        else:
            print("Invalid choice. Please try again.")
