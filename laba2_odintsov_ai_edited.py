from tkinter import Tk, VERTICAL, HORIZONTAL, font, messagebox
from tkinter import ttk, filedialog
import pandas as pd

root = Tk()
root.title("Data Analysis")
root.geometry("1538x825")
root.configure(bg="#f0f0f5")

screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()
x = (screen_width - 1538) // 2
y = (screen_height - 825) // 2
root.geometry(f'+{int(x)}+{int(y)}')

app_font = font.Font(family="Segoe UI", size=12)
style = ttk.Style()
style.theme_use("clam")
style.configure("TButton", font=app_font, padding=6, background="#4CAF50", foreground="white", relief="flat")
style.map("TButton", background=[("active", "#388E3C")], relief=[("pressed", "sunken")])
style.configure("TLabel", background="#f0f0f5", font=("Segoe UI", 12))
style.configure("Treeview", font=("Segoe UI", 10), rowheight=25)
style.configure("Treeview.Heading", font=("Segoe UI", 11, "bold"), background="#e0e0e0", foreground="black")
style.map("Treeview", background=[("selected", "#A5D6A7")], foreground=[("selected", "black")])

root.columnconfigure(0, weight=1)
root.rowconfigure(1, weight=1)

data = pd.DataFrame()
current_data = pd.DataFrame()

def load_csv():
    global data, current_data
    tree.delete(*tree.get_children())  # Clear Treeview table
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
        tree.column(col, stretch=False, anchor="center")
    for row in data.itertuples(index=False):
        tree.insert("", "end", values=row)
    label.config(text="Файл успешно загружен")

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
        if filter_value.isnumeric():
            messagebox.showinfo("Info", "Нет данных, соответствующих фильтру.")
        else:
            messagebox.showinfo("Info", "Неверный формат фильтра.")

# Reset filter function
def reset_filter():
    global current_data
    entry.delete(0, 'end')
    tree.delete(*tree.get_children())
    for row in data.itertuples(index=False):
        tree.insert("", "end", values=row)
    label.config(text="Фильтр сброшен")
    entry.insert(0, "Введите фильтр")
    current_data = data.copy()

label = ttk.Label(root, text="Выберите CSV файл", font=app_font)
label.grid(column=0, row=0, sticky="w", padx=(20, 0), pady=(20, 10))

open_button = ttk.Button(root, text="Открыть файл", command=load_csv)
open_button.grid(column=0, row=0, sticky="e", padx=(20, 0), pady=(20, 10))

tree = ttk.Treeview(root)
scrollbar_v = ttk.Scrollbar(root, orient=VERTICAL, command=tree.yview)
tree.configure(yscroll=scrollbar_v.set)
scrollbar_h = ttk.Scrollbar(root, orient=HORIZONTAL, command=tree.xview)
tree.configure(xscroll=scrollbar_h.set)

tree.grid(column=0, row=1, sticky="nsew", padx=(20, 0))
scrollbar_v.grid(column=1, row=1, sticky="ens", padx=(0, 20))
scrollbar_h.grid(column=0, row=2, sticky="ew", padx=(20, 0))

button_frame = ttk.Frame(root, padding=(10, 10))
button_frame.grid(column=0, row=3, pady=(10, 20), padx=(20, 0), sticky="ew")

open_button_mean = ttk.Button(button_frame, text="Среднее", command=mean, width=15)
open_button_min = ttk.Button(button_frame, text="Минимум", command=minimum, width=15)
open_button_max = ttk.Button(button_frame, text="Максимум", command=maximum, width=15)
entry = ttk.Entry(button_frame, font=app_font, width=20)
entry.insert(0, "Введите фильтр")
open_button_filter = ttk.Button(button_frame, text="Фильтр", command=filter_data, width=15)
reset_button = ttk.Button(button_frame, text="Сбросить фильтр", command=reset_filter, width=15)

open_button_mean.grid(row=0, column=0, padx=5)
open_button_min.grid(row=0, column=1, padx=5)
open_button_max.grid(row=0, column=2, padx=5)
entry.grid(row=0, column=3, padx=5)
open_button_filter.grid(row=0, column=4, padx=5)
reset_button.grid(row=0, column=5, padx=5)

root.mainloop()
