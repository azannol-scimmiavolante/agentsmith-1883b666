"""Entry point for WeatherApp."""

import tkinter as tk
from weatherapp.gui import App


def main():
    """Main entry point for the WeatherApp application."""
    root = tk.Tk()
    app = App(root)
    root.mainloop()


if __name__ == "__main__":
    main()
