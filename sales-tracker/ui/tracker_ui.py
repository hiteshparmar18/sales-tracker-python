import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from core.analysis import (
    load_sales_data,
    get_total_sales,
    get_growth,
    get_best_seller,
    get_weekly_totals
)
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

class SalesTrackerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("📊 Sales Performance Tracker")
        self.root.geometry("800x600")
        self.root.minsize(700, 500)

        self.sales_data = None
        self.product_names = []
        self.week_labels = []

        self.setup_ui()

    def setup_ui(self):
        main_frame = ttk.Frame(self.root, padding=15)
        main_frame.pack(fill=tk.BOTH, expand=True)

        title = ttk.Label(main_frame, text="📊 Sales Performance Tracker", font=("Helvetica", 18, "bold"))
        title.pack(pady=10)

        button_frame = ttk.Frame(main_frame)
        button_frame.pack(pady=5, fill=tk.X)

        ttk.Button(button_frame, text="📁 Load CSV", command=self.load_file).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="📈 Analyze", command=self.analyze_data).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="📊 Show Charts", command=self.show_charts).pack(side=tk.LEFT, padx=5)

        search_frame = ttk.Frame(main_frame)
        search_frame.pack(pady=10, fill=tk.X)

        ttk.Label(search_frame, text="🔍 Search Product:").pack(side=tk.LEFT, padx=5)
        self.product_entry = ttk.Entry(search_frame)
        self.product_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=5)
        ttk.Button(search_frame, text="Get Stats", command=self.get_product_stats).pack(side=tk.LEFT, padx=5)

        self.output = tk.Text(main_frame, height=18, wrap=tk.WORD, font=("Courier New", 10))
        self.output.pack(fill=tk.BOTH, expand=True, pady=10)

    def load_file(self):
        file_path = filedialog.askopenfilename(title="Select CSV File", filetypes=[("CSV Files", "*.csv")])
        if file_path:
            try:
                self.product_names, self.sales_data, self.week_labels = load_sales_data(file_path)
                messagebox.showinfo("Success", "CSV loaded successfully!")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to load file:\n{e}")

    def analyze_data(self):
        if self.sales_data is None:
            messagebox.showerror("Error", "Please load a CSV file first.")
            return

        total_sales = get_total_sales(self.sales_data)
        best_index = get_best_seller(total_sales)
        best_product = self.product_names[best_index]

        self.output.delete(1.0, tk.END)
        self.output.insert(tk.END, f"📊 Total Sales for each Product:\n")
        for name, total in zip(self.product_names, total_sales):
            self.output.insert(tk.END, f"{name}: {total}\n")

        self.output.insert(tk.END, f"\n⭐ Best Selling Product: {best_product} ({total_sales[best_index]} sales)\n")

    def get_product_stats(self):
        if self.sales_data is None:
            messagebox.showerror("Error", "Load CSV first.")
            return

        product_name = self.product_entry.get().strip()
        if product_name not in self.product_names:
            messagebox.showwarning("Not Found", "Product not found in data.")
            return

        index = self.product_names.index(product_name)
        sales = self.sales_data[index]
        growth = get_growth(self.sales_data)[index]

        self.output.delete(1.0, tk.END)
        self.output.insert(tk.END, f"📦 Stats for {product_name}:\n")
        self.output.insert(tk.END, f"Weekly Sales: {sales.tolist()}\n")
        self.output.insert(tk.END, f"Growth per Week: {growth.tolist()}\n")
        self.output.insert(tk.END, f"Total Sales: {sum(sales)}\n")

    def show_charts(self):
        if self.sales_data is None:
            messagebox.showerror("Error", "Please load a CSV file first.")
            return

        totals = get_total_sales(self.sales_data)
        weekly_totals = get_weekly_totals(self.sales_data)

        chart_win = tk.Toplevel(self.root)
        chart_win.title("📊 Sales Charts")
        chart_win.geometry("1000x500")

        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 4))
        fig.suptitle("📈 Sales Insights", fontsize=14, fontweight='bold')

        ax1.bar(self.product_names, totals, color='skyblue')
        ax1.set_title("Total Sales per Product")
        ax1.set_ylabel("Sales")
        ax1.set_xticks(range(len(self.product_names)))
        ax1.set_xticklabels(self.product_names, rotation=45)
        ax1.grid(axis='y', linestyle='--', alpha=0.5)

        ax2.plot(self.week_labels, weekly_totals, marker='o', color='orange')
        ax2.set_title("Total Sales per Week")
        ax2.set_ylabel("Sales")
        ax2.set_xticks(range(len(self.week_labels)))
        ax2.set_xticklabels(self.week_labels)
        ax2.grid(True, linestyle='--', alpha=0.5)

        plt.tight_layout()
        canvas = FigureCanvasTkAgg(fig, master=chart_win)
        canvas.draw()
        canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

if __name__ == "__main__":
    root = tk.Tk()
    app = SalesTrackerApp(root)
    root.mainloop()
