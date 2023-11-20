# Importing necessary modules for creating the GUI
import tkinter as tk
from tkinter import messagebox, font
# Importing the Image modules from Pillow to handle background images
from PIL import Image, ImageTk
# Importing the main application window class
from startWindow import MainWindow

class SignInWindow:
    """A class to create and manage the sign-in window of the application."""
    #Username: admin ; Password: password

    def __init__(self, root):
        """Initialize the sign-in window with a background image, entry fields, and buttons."""
        # Set the root window and its properties
        self.root = root
        self.root.title('Sign In')  # Window title
        self.root.geometry('1024x768')  # Window size

        # Load and set the background image
        image = Image.open('image2.jpeg')
        self.background_image = ImageTk.PhotoImage(image)  # Convert to PhotoImage
        background_label = tk.Label(self.root, image=self.background_image)
        background_label.place(x=0, y=0, relwidth=1, relheight=1)  # Place the image
        background_label.lower()  # Ensure it's in the background

        # Define font styles for widgets
        labelFont = font.Font(family="Helvetica", size=18)
        headingFont = font.Font(family="Helvetica", size=50, weight="bold")
        buttonFont = font.Font(family="Helvetica", size=18, weight="bold")

        # Create and place the heading label
        heading_label = tk.Label(self.root, text="METRICSTICS", fg="cyan", font=headingFont, bg=self.root.cget('bg'))
        heading_label.pack(pady=(10, 20))

        # Create and place the username label and entry box
        tk.Label(self.root, text="Username", fg="white", font=labelFont).pack(pady=(20, 0))
        self.username = tk.Entry(self.root, bd=2, relief="flat", bg="white", fg="black", font=labelFont, width=30)
        self.username.pack(pady=(10, 20), padx=20)

        # Create and place the password label and entry box
        tk.Label(self.root, text="Password", fg="white", font=labelFont).pack(pady=(10, 0))
        self.password = tk.Entry(self.root, show="*", bd=2, relief="flat", bg="white", fg="black", font=labelFont, width=30)
        self.password.pack(pady=(10, 20), padx=20)

        # Create and place the sign-in button
        self.sign_in_button = tk.Button(self.root, text="Sign In", command=self.sign_in, bg="White", fg="Black",
                                        font=buttonFont, bd=0, relief="flat", padx=10, pady=5)
        self.sign_in_button.pack(pady=20)

    def sign_in(self):
        """Handle the sign-in action."""
        # Get username and password from the entry fields
        username = self.username.get()
        password = self.password.get()

        # Check credentials (placeholder for actual authentication logic)
        if username == "admin" and password == "password":
            # If login is successful, hide the sign-in window
            self.root.withdraw()

            # Open the main application window
            main_app_window = tk.Toplevel(self.root)
            main_app = MainWindow(main_app_window)
            main_app_window.mainloop()  # Start the main loop for the main application window
        else:
            # If credentials are incorrect, show an error message
            messagebox.showerror("Error", "Invalid credentials. Please try again.")

# The following code runs if this script is the main program and not a module imported by another script
if __name__ == "__main__":
    # Create the root window and pass it to the sign-in window class
    root = tk.Tk()
    SignInWindow(root)
    root.mainloop()  # Start the Tkinter event loop
