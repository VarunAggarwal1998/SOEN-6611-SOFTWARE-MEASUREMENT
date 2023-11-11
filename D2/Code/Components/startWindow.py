import tkinter as tk
from tkinter import filedialog, messagebox, simpledialog, ttk, font
import pandas as pd

from Components import randomValues
from METRICSTICS import metricstics
from PIL import Image, ImageTk
from statistics import StatisticsError
import numpy as np


class MainWindow:
    """Main Application Window for the METRICSTICS program."""

    def __init__(self, root):
        """Initialize the MainWindow with a background, labels, entry fields, buttons, and a treeview."""
        self.root = root
        self.root.title('METRICSTICS')  # Window title
        self.root.geometry('1024x768')  # Window size

        # Load and set the background image using Pillow
        image = Image.open('image2.jpeg')
        self.background_image = ImageTk.PhotoImage(image)  # Convert image for Tkinter
        background_label = tk.Label(self.root, image=self.background_image)
        background_label.place(x=0, y=0, relwidth=1, relheight=1)  # Place image to cover the whole window
        background_label.lower()  # Set the image behind other widgets

        # Set the font styles for widgets
        labelFont = font.Font(family="Helvetica", size=18)
        headingFont = font.Font(family="Helvetica", size=50, weight="bold")
        buttonFont = font.Font(family="Helvetica", size=18, weight="bold")

        # Place the heading label at the top of the window
        heading_label = tk.Label(self.root, text="METRICSTICS", fg="cyan", font=headingFont, bg=self.root.cget('bg'))
        heading_label.pack(pady=(10, 20))  # Add padding for aesthetics



        # Instruction label for user input
        self.instruction_label = tk.Label(self.root, text="Enter numbers separated by commas (e.g., 1,2,3,4,5):",
                                          fg="white", font=labelFont)
        self.instruction_label.pack(pady=(20, 0))

        # Entry field for user to input numbers
        self.number_entry = tk.Entry(self.root, font=labelFont, width=30)
        self.number_entry.pack(pady=(10, 20), padx=20)

        # Button for uploading files
        self.upload_button = tk.Button(self.root, text="Upload File", command=self.upload_file,
                                       bg="White", fg="Black", font=buttonFont)
        self.upload_button.pack(pady=10)
        self.generate_data_button = tk.Button(self.root, text="Generate Random Data",
                                              command=self.generate_random_data, bg="White",
                                              fg="Black", font=buttonFont)
        self.generate_data_button.pack(pady=10)
        # Button to calculate and display statistics
        self.stats_button = tk.Button(self.root, text="Calculate Statistics", command=self.calculate_statistics,
                                      bg="White", fg="Black", font=buttonFont)
        self.stats_button.pack(pady=20)

        # Button to reset the input fields and clear the statistics table
        self.reset_button = tk.Button(self.root, text="Reset", command=self.reset_fields,
                                      bg="White", fg="Black", font=buttonFont)
        self.reset_button.pack(pady=20)

        # Treeview table to display the statistics with custom styling
        style = ttk.Style()
        style.configure("Treeview", background="#D3D3D3", foreground="black",
                        rowheight=30, font=('Helvetica', 20))  # Light Gray background with black text
        style.map('Treeview', background=[('selected', 'blue')])  # Blue background for selected item

        style.configure("Treeview.Heading", font=('Helvetica', 16, 'bold'))  # Bold font for headings

        # Initialize the Treeview with two columns to show statistics and their values
        self.tree = ttk.Treeview(self.root, column=("c1", "c2"), show='headings')
        self.tree.column("#1", anchor=tk.CENTER, width=300)  # Define column #1 properties
        self.tree.heading("#1", text="Statistic")  # Define column #1 heading
        self.tree.column("#2", anchor=tk.CENTER, width=300)  # Define column #2 properties
        self.tree.heading("#2", text="Value")  # Define column #2 heading
        self.tree.pack(pady=20, expand=True, fill='both')  # Allow the table to expand with the window

        self.numbers = []  # List to store user-entered numbers
        self.file_content = None  # Variable to store content from uploaded files

    def generate_random_data(self):
        """Generate random data and populate the number_entry field with the data."""
        # Call the function to generate random data and save to 'text.txt'
        randomValues.save_random_numbers_to_file('text.txt')

        # Read the generated data from 'text.txt'
        with open('text.txt', 'r') as file:
            random_data = file.read()

        # Insert the random data into the number_entry field
        self.number_entry.delete(0, tk.END)
        self.number_entry.insert(0, random_data)
    def get_numbers(self):
        """Retrieve and validate the numbers entered by the user."""
        numbers_str = self.number_entry.get().strip()
        if numbers_str:
            try:
                # Convert the string of numbers to a list of floats
                self.numbers = [float(num.strip()) for num in numbers_str.split(',')]
            except ValueError:
                # Show error if the conversion fails
                messagebox.showerror("Error", "Please ensure you've entered valid numbers separated by commas.")
                return False
        return True

    def upload_file(self):
        """Open a file dialog for the user to upload a file and process its content."""
        file_path = filedialog.askopenfilename(parent=self.root, filetypes=(("Text files", "*.txt"),
                                                                            ("CSV files", "*.csv"),
                                                                            ("Excel files", "*.xlsx"),
                                                                            ("All files", "*.*")))
        if file_path:
            try:
                # Process different file types and extract numbers
                # If it's a CSV or an Excel file, use pandas to read it
                if file_path.endswith('.csv') or file_path.endswith('.xlsx'):
                    self.file_content = pd.read_csv(file_path) if file_path.endswith('.csv') else pd.read_excel(
                        file_path)
                    if not self.file_content.empty:
                        # Assuming the first column contains the numerical data
                        self.numbers = self.file_content.iloc[:, 0].tolist()
                else:
                    # If it's a text file, read the content and split by commas
                    with open(file_path, 'r') as file:
                        numbers_str = file.read().strip().replace('\n', ',')
                        self.numbers = [float(num) for num in numbers_str.split(',') if num]
                # Update the entry field with the numbers from the file
                self.number_entry.delete(0, tk.END)
                self.number_entry.insert(0, ','.join(map(str, self.numbers)))
            except Exception as e:
                # Show error if file reading fails
                messagebox.showerror("Error", f"An error occurred while reading the file: {str(e)}")

    def calculate_statistics(self):
        """Calculate and display statistics based on the numbers provided by the user."""
        if not self.get_numbers():
            return

        if not self.numbers:
            messagebox.showerror("Error", "No data available for calculations. Please input numbers or upload a file.")
            return

        try:
            # Calculate statistics using methods from the metricstics module
            numbers_mean = metricstics.calculate_mean(self.numbers)
            numbers_median = metricstics.calculate_median(self.numbers)
            numbers_mode = metricstics.calculate_mode(self.numbers)
            numbers_min = metricstics.calculate_min(self.numbers)
            numbers_max = metricstics.calculate_max(self.numbers)
            mean_abs_deviation = metricstics.calculate_mean_absolute_deviation(self.numbers)
            numbers_stdev = metricstics.calculate_standard_deviation(self.numbers)

            # Clear the treeview for the new set of statistics
            for _ in self.tree.get_children():
                self.tree.delete(_)

            # Populate the treeview with the calculated statistics
            stats = [("Minimum", numbers_min), ("Maximum", numbers_max), ("Mode", numbers_mode),
                     ("Median", numbers_median), ("Arithmetic Mean", numbers_mean),
                     ("Mean Absolute Deviation", mean_abs_deviation), ("Standard Deviation", numbers_stdev)]

            for stat, value in stats:
                self.tree.insert("", tk.END, values=(stat, value))
        except StatisticsError as e:
            messagebox.showerror("Error", str(e))
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred while calculating statistics: {str(e)}")

    def reset_fields(self):
        """Reset the entry field, clear the treeview, and reset the numbers list and file content."""
        self.number_entry.delete(0, tk.END)  # Clear the entry box
        for record in self.tree.get_children():
            self.tree.delete(record)  # Clear the treeview
        self.numbers = []  # Reset the numbers list
        self.file_content = None  # Reset the file content


if __name__ == "__main__":
    root = tk.Tk()  # Create the main window
    MainWindow(root)  # Instantiate the MainWindow class with the main window
    root.mainloop()  # Start the Tkinter event loop
