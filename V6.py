import tkinter as tk
from tkinter import filedialog
import pandas as pd

# =========================
# APP
# =========================
app = tk.Tk()
app.title("Excel Analyzer PRO (Single File)")
app.geometry("650x550")

file_path = tk.StringVar()
action = tk.StringVar()
action.set("Analyze")

# =========================
# LOG BOX
# =========================
log_box = tk.Text(app, height=18, width=75)
log_box.pack(pady=10)

def log(msg):
    log_box.insert(tk.END, str(msg) + "\n")
    log_box.see(tk.END)

# =========================
# CORE FUNCTIONS
# =========================
def detect_column(df):
    possible = ["domain", "category", "tag", "class", "label"]
    for col in df.columns:
        if col.strip().lower() in possible:
            return col
    return None


def browse_file():
    path = filedialog.askopenfilename(filetypes=[("Excel files", "*.xlsx")])
    file_path.set(path)
    log("📁 File selected")


def run_analysis():
    path = file_path.get()

    if not path:
        log("❌ No file selected")
        return

    log("⏳ Loading file...")

    df = pd.read_excel(path)
    df.columns = df.columns.str.strip()

    log(f"✅ Loaded rows: {len(df)}")
    log(f"📊 Columns: {list(df.columns)}")

    col = detect_column(df)

    if not col:
        log("❌ No valid column found (domain/category/tag)")
        return

    log(f"🎯 Using column: {col}")
    log(f"🚀 Action: {action.get()}")

    # =========================
    # ANALYZE
    # =========================
    if action.get() == "Analyze":
        result = df[col].value_counts()
        log(result)

    # =========================
    # PERCENTAGE
    # =========================
    elif action.get() == "Percentage":
        result = df[col].value_counts(normalize=True) * 100
        log(result.round(2))

    # =========================
    # TOP 10
    # =========================
    elif action.get() == "Top10":
        result = df[col].value_counts().head(10)
        log(result)

    # =========================
    # CLEAN DATA
    # =========================
    elif action.get() == "Clean":
        before = len(df)
        df2 = df.dropna()
        after = len(df2)

        log(f"🧹 Removed rows: {before - after}")

# =========================
# UI
# =========================
tk.Label(app, text="Excel Analyzer PRO", font=("Arial", 18)).pack()

tk.Button(app, text="📂 Load Excel", command=browse_file).pack(pady=5)

actions = ["Analyze", "Percentage", "Top10", "Clean"]
tk.OptionMenu(app, action, *actions).pack(pady=5)

tk.Button(app, text="🚀 RUN", bg="green", fg="white", command=run_analysis).pack(pady=10)

app.mainloop()