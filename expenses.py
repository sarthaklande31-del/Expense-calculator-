import json
import os
from datetime import datetime

DATA_FILE = "expenses.json"

def load_expenses():
    if not os.path.exists(DATA_FILE):
        return []
    with open(DATA_FILE, "r", encoding="utf-8") as f:
        try:
            return json.load(f)
        except json.JSONDecodeError:
            return []

def save_expenses(expenses):
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(expenses, f, indent=2, ensure_ascii=False)

def add_expense(expenses, amount, category, note=""):
    entry = {
        "id": int(datetime.utcnow().timestamp() * 1000),
        "amount": float(amount),
        "category": category.strip(),
        "note": note.strip(),
        "date": datetime.utcnow().isoformat()
    }
    expenses.append(entry)
    save_expenses(expenses)
    print("✅ Expense added.")

def list_expenses(expenses, category=None):
    filtered = [e for e in expenses if (category is None or e["category"].lower() == category.lower())]
    if not filtered:
        print("No expenses found.")
        return
    for e in filtered:
        print(f'{e["id"]} | {e["date"][:19]} | {e["category"]:<12} | {e["amount"]:8.2f} | {e["note"]}')
    print(f"\nTotal ({len(filtered)} items): {sum(e['amount'] for e in filtered):.2f}")

def delete_expense(expenses, id_value):
    before = len(expenses)
    expenses[:] = [e for e in expenses if str(e["id"]) != str(id_value)]
    if len(expenses) < before:
        save_expenses(expenses)
        print("✅ Deleted.")
    else:
        print("⚠️ Not found.")

def export_csv(expenses, filename="expenses_export.csv"):
    lines = ["id,date,category,amount,note"]
    for e in expenses:
        note = e["note"].replace('"', '""')
        lines.append(f'{e["id"]},{e["date"]},{e["category"]},{e["amount"]},"{note}"')
    with open(filename, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))
    print(f"✅ Exported {len(expenses)} rows to {filename}")

def show_summary(expenses):
    if not expenses:
        print("No expenses yet.")
        return
    total = sum(e["amount"] for e in expenses)
    per_cat = {}
    for e in expenses:
        per_cat.setdefault(e["category"], 0.0)
        per_cat[e["category"]] += e["amount"]
    print(f"Total expenses: {total:.2f}")
    print("By category:")
    for cat, amt in per_cat.items():
        print(f"  {cat:<12} : {amt:.2f}")

def get_nonempty(prompt):
    while True:
        v = input(prompt).strip()
        if v:
            return v

def main():
    expenses = load_expenses()
    menu = """
Choose:
1. Add expense
2. List all expenses
3. List by category
4. Delete expense (by id)
5. Summary (totals)
6. Export CSV
7. Clear all data (danger!)
8. Exit
"""
    while True:
        print(menu)
        choice = input("Enter choice: ").strip()
        if choice == "1":
            amt = get_nonempty("Amount: ")
            cat = get_nonempty("Category: ")
            note = input("Note (optional): ")
            try:
                add_expense(expenses, amt, cat, note)
            except ValueError:
                print("⚠️ Invalid amount. Use numbers like 120.50")
        elif choice == "2":
            list_expenses(expenses)
        elif choice == "3":
            cat = get_nonempty("Category to filter: ")
            list_expenses(expenses, category=cat)
        elif choice == "4":
            idv = get_nonempty("Enter ID to delete: ")
            delete_expense(expenses, idv)
        elif choice == "5":
            show_summary(expenses)
        elif choice == "6":
            filename = input("Filename (default expenses_export.csv): ").strip() or "expenses_export.csv"
            export_csv(expenses, filename)
        elif choice == "7":
            confirm = input("Type YES to permanently delete all data: ")
            if confirm == "YES":
                expenses.clear()
                save_expenses(expenses)
                print("✅ All data cleared.")
            else:
                print("Cancelled.")
        elif choice == "8":
            print("Bye.")
            break
        else:
            print("Invalid choice, try again.")

if __name__ == "__main__":
    main()