from tkinter import Tk, VERTICAL, HORIZONTAL, font, messagebox
from tkinter import ttk, filedialog
import pandas as pd

root = Tk()
root.title("Data Analysis")
root.geometry("1538x825")

screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()
x = (screen_width - 1538) // 2
y = (screen_height - 825) // 2
root.geometry(f'+{int(x)}+{int(y)}')

app_font = font.Font(family="Arial", size=15)
style = ttk.Style()
style.configure("TButton", font=app_font)

for c in range(5):
    root.columnconfigure(index=c, weight=1)
for r in range(4):
    root.rowconfigure(index=r, weight=1)

data = pd.DataFrame()
current_data = pd.DataFrame()

def load_csv():
    global data, current_data
    tree.delete(*tree.get_children())
    path = filedialog.askopenfilename(filetypes=[("CSV files", "*.csv")])
    if path:
        data = pd.read_csv(path, delimiter=';')
        current_data = data.copy()
        setup_treeview(data)

def setup_treeview(data):
    tree["columns"] = data.columns.tolist()
    tree["show"] = "headings"
    for col in data.columns:
        tree.heading(col, text=col)
        tree.column(col, stretch=False)
    for row in data.itertuples(index=False):
        tree.insert("", "end", values=row)
    label.config(text="Файл успешно загружен")
    arrange_widgets()

def arrange_widgets():
    tree.grid(column=1, row=1, sticky="nswe", columnspan=3, rowspan=2)
    scrollbar_v.grid(column=4, row=1, sticky="nsw", rowspan=2)
    scrollbar_h.grid(column=1, row=3, sticky="nwe", columnspan=3)
    open_button_mean.grid(column=1, row=3, sticky="w")
    open_button_min.grid(column=1, row=3)
    open_button_max.grid(column=1, row=3, sticky="e")
    entry.grid(column=2, row=3, padx=20, sticky="w")
    open_button_filter.grid(column=2, row=3, sticky="e")
    reset_button.grid(column=3, row=3, padx=4, sticky="w")

def calculate_and_display_stat(stat_func, title):
    numeric_data = current_data.apply(pd.to_numeric, errors='coerce')
    result = numeric_data.agg(stat_func).dropna()
    if not result.empty:
        result_message = "\n".join([f"{col}: {result[col]:.2f}" for col in result.index])
        messagebox.showinfo(title, result_message)
    else:
        messagebox.showwarning("Warning", "Нет числовых данных!")

def mean():
    calculate_and_display_stat('mean', 'Среднее')

def minimum():
    calculate_and_display_stat('min', 'Минимальное')

def maximum():
    calculate_and_display_stat('max', 'Максимальное')

def filter_data():
    global current_data
    filter_value = entry.get().strip()
    if not filter_value:
        messagebox.showwarning("Warning", "Введите значение для фильтрации!")
        return
    filtered_data = current_data[current_data.apply(
        lambda row: row.astype(str).str.contains(filter_value).any(), axis=1)]
    if not filtered_data.empty:
        tree.delete(*tree.get_children())
        for row in filtered_data.itertuples(index=False):
            tree.insert("", "end", values=row)
        current_data = filtered_data
        label.config(text="Таблица отфильтрована")
    else:
        label.config(text="Ошибка фильтрации")
        messagebox.showinfo("Info", "Нет данных, соответствующих фильтру.")

def reset_filter():
    global current_data
    entry.delete(0, 'end')
    tree.delete(*tree.get_children())
    for row in data.itertuples(index=False):
        tree.insert("", "end", values=row)
    label.config(text="Фильтр сброшен")
    entry.insert(0, "Введите фильтр")
    current_data = data.copy()

open_button = ttk.Button(text="Открыть файл", command=load_csv, width=13)
open_button.grid(column=1, row=0, sticky="w")

label = ttk.Label(text="Выберите CSV файл", font=app_font)
label.grid(column=1, row=0, padx=90)

tree = ttk.Treeview()
scrollbar_v = ttk.Scrollbar(orient=VERTICAL, command=tree.yview)
tree.configure(yscroll=scrollbar_v.set)
scrollbar_h = ttk.Scrollbar(orient=HORIZONTAL, command=tree.xview)
tree.configure(xscroll=scrollbar_h.set)

open_button_mean = ttk.Button(text="Среднее", width=13, command=mean)
open_button_min = ttk.Button(text="Минимум", width=13, command=minimum)
open_button_max = ttk.Button(text="Максимум", width=13, command=maximum)

entry = ttk.Entry(font=app_font)
entry.insert(0, "Введите фильтр")

open_button_filter = ttk.Button(text="Фильтр", width=13, command=filter_data)
reset_button = ttk.Button(text="Сбросить фильтр", width=15, command=reset_filter)

root.mainloop()
