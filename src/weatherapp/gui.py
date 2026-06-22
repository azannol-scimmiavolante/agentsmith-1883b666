"""Tkinter GUI for WeatherApp."""

import tkinter as tk
from tkinter import ttk, messagebox
from typing import Optional

from weatherapp.client import WeatherClient
from weatherapp.exceptions import WeatherError
from weatherapp.config import DEFAULT_CITY


class App:
    """Main application GUI for WeatherApp."""

    def __init__(self, root: tk.Tk):
        """Initialize the WeatherApp GUI.

        Args:
            root: The root Tkinter window
        """
        self.root = root
        self.root.title("WeatherApp")
        self.root.geometry("700x500")
        self.root.resizable(True, True)

        # Initialize the weather client
        try:
            self.client = WeatherClient()
        except WeatherError as e:
            messagebox.showerror("Configuration Error", str(e))
            self.root.destroy()
            return

        # Create the GUI components
        self._create_widgets()

        # Load default city weather
        self._search_weather(DEFAULT_CITY)

    def _create_widgets(self):
        """Create and layout all GUI widgets."""
        # Top frame for search
        search_frame = ttk.Frame(self.root, padding="10")
        search_frame.pack(fill=tk.X, side=tk.TOP)

        # City entry
        ttk.Label(search_frame, text="City:").pack(side=tk.LEFT, padx=(0, 5))
        self.city_entry = ttk.Entry(search_frame, width=30)
        self.city_entry.pack(side=tk.LEFT, padx=(0, 10))
        self.city_entry.insert(0, DEFAULT_CITY)
        self.city_entry.bind("<Return>", lambda e: self._on_search())

        # Search button
        self.search_button = ttk.Button(
            search_frame, text="Search", command=self._on_search
        )
        self.search_button.pack(side=tk.LEFT)

        # Notebook for tabs
        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        # Create tabs
        self._create_current_tab()
        self._create_forecast_tab()

    def _create_current_tab(self):
        """Create the 'Current' weather tab."""
        current_frame = ttk.Frame(self.notebook, padding="20")
        self.notebook.add(current_frame, text="Current")

        # Create a grid for current weather information
        # Location label at the top
        self.location_label = ttk.Label(
            current_frame, text="", font=("TkDefaultFont", 14, "bold")
        )
        self.location_label.grid(row=0, column=0, columnspan=2, pady=(0, 20), sticky=tk.W)

        # Weather details
        row = 1
        self.current_labels = {}

        # Temperature
        ttk.Label(current_frame, text="Temperature:", font=("TkDefaultFont", 10, "bold")).grid(
            row=row, column=0, sticky=tk.W, pady=5, padx=(0, 10)
        )
        self.current_labels["temp"] = ttk.Label(current_frame, text="--")
        self.current_labels["temp"].grid(row=row, column=1, sticky=tk.W, pady=5)
        row += 1

        # Condition
        ttk.Label(current_frame, text="Condition:", font=("TkDefaultFont", 10, "bold")).grid(
            row=row, column=0, sticky=tk.W, pady=5, padx=(0, 10)
        )
        self.current_labels["condition"] = ttk.Label(current_frame, text="--")
        self.current_labels["condition"].grid(row=row, column=1, sticky=tk.W, pady=5)
        row += 1

        # Humidity
        ttk.Label(current_frame, text="Humidity:", font=("TkDefaultFont", 10, "bold")).grid(
            row=row, column=0, sticky=tk.W, pady=5, padx=(0, 10)
        )
        self.current_labels["humidity"] = ttk.Label(current_frame, text="--")
        self.current_labels["humidity"].grid(row=row, column=1, sticky=tk.W, pady=5)
        row += 1

        # Wind
        ttk.Label(current_frame, text="Wind:", font=("TkDefaultFont", 10, "bold")).grid(
            row=row, column=0, sticky=tk.W, pady=5, padx=(0, 10)
        )
        self.current_labels["wind"] = ttk.Label(current_frame, text="--")
        self.current_labels["wind"].grid(row=row, column=1, sticky=tk.W, pady=5)
        row += 1

        # UV Index
        ttk.Label(current_frame, text="UV Index:", font=("TkDefaultFont", 10, "bold")).grid(
            row=row, column=0, sticky=tk.W, pady=5, padx=(0, 10)
        )
        self.current_labels["uv"] = ttk.Label(current_frame, text="--")
        self.current_labels["uv"].grid(row=row, column=1, sticky=tk.W, pady=5)
        row += 1

        # Last updated
        self.last_updated_label = ttk.Label(
            current_frame, text="", font=("TkDefaultFont", 8), foreground="gray"
        )
        self.last_updated_label.grid(
            row=row, column=0, columnspan=2, pady=(20, 0), sticky=tk.W
        )

    def _create_forecast_tab(self):
        """Create the 'Forecast' weather tab."""
        forecast_frame = ttk.Frame(self.notebook, padding="10")
        self.notebook.add(forecast_frame, text="Forecast")

        # Create Treeview for forecast data
        columns = ("day", "temp_c", "condition")
        self.forecast_tree = ttk.Treeview(
            forecast_frame, columns=columns, show="headings", height=10
        )

        # Define column headings
        self.forecast_tree.heading("day", text="Date")
        self.forecast_tree.heading("temp_c", text="Temperature (°C)")
        self.forecast_tree.heading("condition", text="Condition")

        # Define column widths
        self.forecast_tree.column("day", width=150, anchor=tk.W)
        self.forecast_tree.column("temp_c", width=150, anchor=tk.CENTER)
        self.forecast_tree.column("condition", width=300, anchor=tk.W)

        # Add scrollbar
        scrollbar = ttk.Scrollbar(
            forecast_frame, orient=tk.VERTICAL, command=self.forecast_tree.yview
        )
        self.forecast_tree.configure(yscroll=scrollbar.set)

        # Pack the treeview and scrollbar
        self.forecast_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

    def _on_search(self):
        """Handle search button click."""
        city = self.city_entry.get().strip()
        if not city:
            messagebox.showwarning("Input Required", "Please enter a city name.")
            return

        self._search_weather(city)

    def _search_weather(self, city: str):
        """Search for weather data for the given city.

        Args:
            city: Name of the city to search for
        """
        # Disable search button during request
        self.search_button.config(state=tk.DISABLED)
        self.root.config(cursor="watch")
        self.root.update()

        try:
            # Get current weather
            current = self.client.get_current(city)
            self._update_current_tab(current)

            # Get forecast
            forecast = self.client.get_forecast(city, days=5)
            self._update_forecast_tab(forecast)

        except WeatherError as e:
            messagebox.showerror("Weather Error", str(e))
        except Exception as e:
            messagebox.showerror("Unexpected Error", f"An unexpected error occurred: {e}")
        finally:
            # Re-enable search button
            self.search_button.config(state=tk.NORMAL)
            self.root.config(cursor="")

    def _update_current_tab(self, current):
        """Update the current weather tab with new data.

        Args:
            current: CurrentWeather object
        """
        # Update location label
        if current.location:
            location_text = f"{current.location.name}, {current.location.region}, {current.location.country}"
            self.location_label.config(text=location_text)
        else:
            self.location_label.config(text="")

        # Update weather details
        self.current_labels["temp"].config(
            text=f"{current.temp_c}°C / {current.temp_f}°F"
        )
        self.current_labels["condition"].config(text=current.condition)
        self.current_labels["humidity"].config(text=f"{current.humidity}%")
        self.current_labels["wind"].config(text=f"{current.wind_kph} kph")
        self.current_labels["uv"].config(text=str(current.uv_index))

        # Update last updated time
        if current.last_updated:
            self.last_updated_label.config(text=f"Last updated: {current.last_updated}")
        else:
            self.last_updated_label.config(text="")

    def _update_forecast_tab(self, forecast):
        """Update the forecast tab with new data.

        Args:
            forecast: List of ForecastDay objects
        """
        # Clear existing items
        for item in self.forecast_tree.get_children():
            self.forecast_tree.delete(item)

        # Add new forecast data
        for day in forecast:
            # Format temperature range
            if day.maxtemp_c is not None and day.mintemp_c is not None:
                temp_str = f"{day.mintemp_c}°C - {day.maxtemp_c}°C"
            else:
                temp_str = f"{day.temp_c}°C"

            self.forecast_tree.insert(
                "",
                tk.END,
                values=(day.date, temp_str, day.condition)
            )
