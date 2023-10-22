# Importing necessary modules
import tkinter as tk
from tkinter import messagebox, font
from statWindow import MainWindow 

class SignInWindow:
    """
    A class used to represent the SignInWindow.

    ...

    Attributes
    ----------
    root : Tk
        The root window of the application.
    username : Entry
        The entry widget for the username.
    password : Entry
        The entry widget for the password (masked).
    sign_in_button : Button
        The button that triggers the sign-in functionality.

    Methods
    -------
    sign_in():
        Checks the credentials and displays a message.
    """

    def __init__(self, root):
        """
        Constructs all the necessary attributes for the SignInWindow object.

        Parameters
        ----------
            root : Tk
                The root window of the application.
        """

        self.root = root
        self.root.title('Sign In')

        # Set the geometry for the window (width x height)
        self.root.geometry('300x400')  # You might want to adjust the size

        # Set the background color of the window
        bgColor = "#f4f4f4"  # Light grey background, easier on the eyes and more professional
        self.root.configure(bg=bgColor)

        # Define a style for the labels and buttons
        labelFont = font.Font(family="Helvetica", size=12)
        buttonFont = font.Font(family="Helvetica", size=12, weight="bold")

        # Creating the username and password labels and entry boxes
        tk.Label(self.root, text="Username", bg=bgColor, fg="black", font=labelFont).pack(pady=(20, 0))
        self.username = tk.Entry(self.root, bd=2, relief="flat")  # flat relief with border creates a modern text field style
        self.username.pack(pady=10, padx=20, fill='x')  # fill x-axis, more space to type

        tk.Label(self.root, text="Password", bg=bgColor, fg="black", font=labelFont).pack(pady=(10, 0))
        self.password = tk.Entry(self.root, show="*", bd=2, relief="flat")
        self.password.pack(pady=10, padx=20, fill='x')

        # Creating the sign-in button
        self.sign_in_button = tk.Button(self.root, text="Sign In", command=self.sign_in, bg="#28a745", fg="black", font=buttonFont, bd=0, relief="flat", padx=10, pady=5)
        self.sign_in_button.pack(pady=20)

    def sign_in(self):
        """
        Handles the sign-in functionality by checking the credentials.
        If the credentials match, it displays a successful login message; otherwise, it shows an error.
        """

        username = self.username.get()
        password = self.password.get()

        # Placeholder for actual authentication logic (e.g., checking a database)
        if username == "admin" and password == "password":
            # messagebox.showinfo("Success", "Sign-in successful!")

            # Close the current sign-in window
            self.root.destroy()

            # Open the main application window
            new_root = tk.Tk()  # Create a new Tk instance
            main_app = MainWindow(new_root)  # Create an instance of the MainWindow
            new_root.mainloop()  # Run the main application event loop
        else:
            messagebox.showerror("Error", "Invalid credentials. Please try again.")


# Usage: Creating a window and running the application
if __name__ == "__main__":
    root = tk.Tk()  # Create a standard Tk instance
    SignInWindow(root)  # Create an instance of the SignInWindow
    root.mainloop()  # Run the tkinter event loop
