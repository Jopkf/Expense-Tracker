import tkinter as tk
from tkinter import ttk, messagebox
import json
from datetime import datetime

FILE_NAME = "expenses.json"

expenses = []

# --- Работа с файлами ---
def save_data():
    with open(FILE_NAME, "w", encoding="utf-8") as f:
        json.dump(expenses, f, ensure_ascii=False, indent=4)

def load_data():
    global expenses
    try:
        with open(FILE_NAME, "r", encoding="utf-8") as f:
            expenses = json.load(f)
            refresh_table(expenses)
    except FileNotFoundError:
        expenses = []

# --- Проверка данных ---
def validate_input(amount, date):
    try:
        amount = float(amount)
        if amount <= 0:
            return False
        datetime.strptime(date, "%Y-%m-%d")
        return True
    except:
        return False

# --- Добавление расхода ---
def add_expense():
    amount = amount_entry.get()
    category = category_combo.get()
    date = date_entry.get()

    if not validate_input(amount, date):
        messagebox.showerror("Ошибка", "Введите корректные данные")
        return

    expense = {
        "amount": float(amount),
        "category": category,
        "date": date
    }

    expenses.append(expense)
    refresh_table(expenses)
    save_data()

# --- Обновление таблицы ---
def refresh_table(data):
    for row in tree.get_children():
        tree.delete(row)

    for exp in data:
        tree.insert("", tk.END, values=(exp["amount"], exp["category"], exp["date"]))

# --- Фильтрация ---
def filter_data():
    category = filter_category.get()
    date_from = date_from_entry.get()
    date_to = date_to_entry.get()

    filtered = expenses

    if category != "Все":
        filtered = [e for e in filtered if e["category"] == category]

    try:
        if date_from:
            d1 = datetime.strptime(date_from, "%Y-%m-%d")
            filtered = [e for e in filtered if datetime.strptime(e["date"], "%Y-%m-%d") >= d1]

        if date_to:
            d2 = datetime.strptime(date_to, "%Y-%m-%d")
            filtered = [e for e in filtered if datetime.strptime(e["date"], "%Y-%m-%d") <= d2]
    except:
        messagebox.showerror("Ошибка", "Неверный формат даты")
        return

    refresh_table(filtered)

# --- Подсчёт суммы ---
def calculate_total():
    total = 0
    for row in tree.get_children():
        total += float(tree.item(row)["values"][0])

    total_label.config(text=f"Итого: {total:.2f}")

# --- GUI ---
root = tk.Tk()
root.title("Expense Tracker")

# Ввод данных
tk.Label(root, text="Сумма").pack()
amount_entry = tk.Entry(root)
amount_entry.pack()

tk.Label(root, text="Категория").pack()
category_combo = ttk.Combobox(root, values=["Еда", "Транспорт", "Развлечения"], state="readonly")
category_combo.pack()

tk.Label(root, text="Дата (YYYY-MM-DD)").pack()
date_entry = tk.Entry(root)
date_entry.pack()

tk.Button(root, text="Добавить расход", command=add_expense).pack(pady=5)

# Таблица
tree = ttk.Treeview(root, columns=("Amount", "Category", "Date"), show="headings")
tree.heading("Amount", text="Сумма")
tree.heading("Category", text="Категория")
tree.heading("Date", text="Дата")
tree.pack(pady=10)

# Фильтры
tk.Label(root, text="Фильтр категория").pack()
filter_category = ttk.Combobox(root, values=["Все", "Еда", "Транспорт", "Развлечения"], state="readonly")
filter_category.set("Все")
filter_category.pack()

tk.Label(root, text="Дата от").pack()
date_from_entry = tk.Entry(root)
date_from_entry.pack()

tk.Label(root, text="Дата до").pack()
date_to_entry = tk.Entry(root)
date_to_entry.pack()

tk.Button(root, text="Фильтровать", command=filter_data).pack(pady=5)

# Подсчёт
tk.Button(root, text="Посчитать сумму", command=calculate_total).pack()
total_label = tk.Label(root, text="Итого: 0")
total_label.pack()

# Загрузка данных при старте
load_data()

root.mainloop()