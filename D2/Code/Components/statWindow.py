import tkinter as tk
from tkinter import filedialog, messagebox, simpledialog, ttk
import pandas as pd
from calculator import Statistics
from statistics import mean, median, mode, StatisticsError, stdev, variance
import numpy as np

class MainWindow:
    
    """
    Main Application Window Class.

    This class is responsible for creating and managing the main application window.
    It includes the UI setup, event handling, and statistical calculations based on user input or uploaded files.

    Attributes
    ----------
    root : tk.Tk
        The root window of the application.
    instruction_label : tk.Label
        Label widget providing instructions for the number input.
    number_entry : tk.Entry
        Entry widget for inputting numbers.
    upload_button : tk.Button
        Button that triggers the file upload dialog.
    stats_button : tk.Button
        Button that initiates the calculation of statistics based on the input data.
    reset_button : tk.Button
        Button that resets the input fields and statistics table.
    tree : ttk.Treeview
        Table for displaying the calculated statistics.
    numbers : list
        A list that stores the numeric data entered by the user or read from a file.
    file_content : various types
        Content of the uploaded file, stored in the most appropriate format (e.g., DataFrame for CSV).

    Methods
    -------
    get_numbers():
        Retrieves and validates the numbers from the number_entry widget.
    upload_file():
        Handles the file upload process and reads the content of the file.
    calculate_statistics():
        Performs statistical calculations and updates the Treeview widget with the results.
    reset_fields():
        Clears all input fields, internal data storage, and the statistics table.
    """
        
    def __init__(self, root):
        """
        Initialize the MainWindow object.

        This constructor creates all the necessary UI elements and sets their properties and event bindings.

        Parameters:
        root (tk.Tk): The root window of the application.
        """

        self.root = root
        self.root.title('Statistical Data Calculator')
        self.root.geometry('800x600')
        self.root.configure(bg="#f0f0f0")

        # Instruction label
        self.instruction_label = tk.Label(self.root, text="Enter numbers separated by commas (e.g., 1,2,3,4,5):", bg="#f0f0f0")
        self.instruction_label.pack(pady=10)

        # Text box for inputting numbers
        self.number_entry = tk.Entry(self.root)
        self.number_entry.pack(pady=10)

        # Button for uploading files
        self.upload_button = tk.Button(self.root, text="Upload File", command=self.upload_file, bg="#2196F3", fg="black")
        self.upload_button.pack(pady=10)

        # Button for calculating and displaying statistics
        self.stats_button = tk.Button(self.root, text="Calculate Statistics", command=self.calculate_statistics, bg="#4CAF50", fg="black")
        self.stats_button.pack(pady=20)

        # Button for resetting the inputs and table
        self.reset_button = tk.Button(self.root, text="Reset", command=self.reset_fields, bg="#FF5722", fg="black")
        self.reset_button.pack(pady=20)

        # Table to display the statistics
        # Styling the table for a better appearance
        style = ttk.Style()
        style.configure("Treeview", 
                        background="#D3D3D3",  # Light Gray
                        foreground="black",
                        rowheight=25,  # increased row height for readability
                        fieldbackground="#D3D3D3")  # Light Gray
        style.map('Treeview', background=[('selected', 'blue')])  # highlight selection

        # Table to display the statistics
        self.tree = ttk.Treeview(self.root, column=("c1", "c2"), show='headings')
        self.tree.column("#1", anchor=tk.CENTER, width=300)  # increased width for better spacing
        self.tree.heading("#1", text="Statistic")
        self.tree.column("#2", anchor=tk.CENTER, width=300)  # increased width for better spacing
        self.tree.heading("#2", text="Value")
        self.tree.pack(pady=20, expand=True, fill='both')  # make table expandable

        self.numbers = []
        self.file_content = None

    def get_numbers(self):
        """
        Retrieve and validate numbers from the entry widget.

        This method extracts the string from the number_entry widget, splits it to form a list of numbers,
        and checks for any invalid input. If the input is valid, it updates the 'numbers' attribute.

        Returns:
        bool: True if the input is valid, False otherwise.
        """
                
        numbers_str = self.number_entry.get().strip()
        if numbers_str:
            try:
                self.numbers = [float(num.strip()) for num in numbers_str.split(',')]
            except ValueError:
                messagebox.showerror("Error", "Please ensure you've entered valid numbers separated by commas.")
                return False
        return True

    def upload_file(self):
        """
        Handle file upload functionality.

        This method opens a file dialog, allows the user to select a file, and attempts to read its content.
        It supports various file types like .txt, .csv, and .xlsx. The content of the file is read accordingly
        and stored in the 'file_content' attribute, and the numeric data is extracted to the 'numbers' attribute.

        Returns:
        None
        """
        file_path = filedialog.askopenfilename(filetypes=(("Text files", "*.txt"), ("CSV files", "*.csv"), ("Excel files", "*.xlsx"), ("All files", "*.*")))
        if file_path:
            try:
                if file_path.endswith('.csv') or file_path.endswith('.xlsx'):
                    self.file_content = pd.read_csv(file_path) if file_path.endswith('.csv') else pd.read_excel(file_path)
                    if not self.file_content.empty:
                        self.numbers = self.file_content.iloc[:, 0].tolist()  # considering the first column has the data
                else:
                    with open(file_path, 'r') as file:
                        numbers_str = file.read().strip().replace('\n', ',')
                        self.numbers = [float(num) for num in numbers_str.split(',') if num]
                self.number_entry.delete(0, tk.END)  # Clear the entry box when a file is uploaded
                self.number_entry.insert(0, ','.join(map(str, self.numbers)))  # Show the numbers from the file in the entry box
            except Exception as e:
                messagebox.showerror("Error", f"An error occurred while reading the file: {str(e)}")

    def calculate_statistics(self):
        """
        Calculate and display statistical data.

        This method uses the 'numbers' attribute to calculate various statistics, including the mean, median, mode,
        minimum, maximum, mean absolute deviation, and standard deviation. It then updates the 'tree' Treeview widget,
        populating it with the calculated statistical data.

        Returns:
        None
        """

        if not self.get_numbers():  # Validate and get numbers from entry
            return

        if not self.numbers:
            messagebox.showerror("Error", "No data available for calculations. Please input numbers or upload a file.")
            return

        try:
            # Calculate statistics
            numbers_mean = Statistics.calculate_mean(self.numbers)
            numbers_median = Statistics.calculate_median(self.numbers)
            numbers_mode = Statistics.calculate_mode(self.numbers)
            numbers_min = Statistics.calculate_min(self.numbers)
            numbers_max = Statistics.calculate_max(self.numbers)
            mean_abs_deviation = Statistics.calculate_mean_absolute_deviation(self.numbers)
            numbers_stdev = Statistics.calculate_standard_deviation(self.numbers)

            # Clear previous stats
            for _ in self.tree.get_children():
                self.tree.delete(_)

            # Inserting each statistic in the table
            stats = [("Minimum", numbers_min), ("Maximum", numbers_max), ("Mode", numbers_mode), ("Median", numbers_median),
                     ("Arithmetic Mean", numbers_mean), ("Mean Absolute Deviation", mean_abs_deviation), ("Standard Deviation", numbers_stdev)]

            for stat, value in stats:
                self.tree.insert("", tk.END, values=(stat, value))

        except StatisticsError as e:
            messagebox.showerror("Error", str(e))
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred while calculating statistics: {str(e)}")

    def reset_fields(self):
        """
        Reset all fields and internal storage.

        This method clears the number_entry widget, the 'tree' Treeview widget, and resets the 'numbers' and
        'file_content' attributes, effectively resetting the state of the application for new data.

        Returns:
        None
        """
                
        # Clear the entry box
        self.number_entry.delete(0, tk.END)

        # Clear the table
        for record in self.tree.get_children():
            self.tree.delete(record)

        # Reset the numbers list and file content
        self.numbers = []
        self.file_content = None

if __name__ == "__main__":
    root = tk.Tk()
    MainWindow(root)
    root.mainloop()
