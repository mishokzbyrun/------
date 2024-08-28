import tkinter as tk
from tkinter import messagebox
import requests
import datetime

def get_weather():
    city = city_entry.get()
    if not city:
        messagebox.showwarning("error", "enter the name of the town.")
    else:
        api_key = "YOUR_API_KEY"  # Replace with your actual API key
        url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric"
        
        try:
            response = requests.get(url)
            response.raise_for_status()
            weather_data = response.json()

            if weather_data["cod"] != 200:
                messagebox.showerror("error", weather_data["message"])
            else:
                temp = weather_data["main"]["temp"]
                condition = weather_data["weather"][0]["description"].capitalize()
                humidity = weather_data["main"]["humidity"]
                wind_speed = weather_data["wind"]["speed"]

                result_label.config(
                    text=f"Temp: {temp}°C\n"
                         f"Condition: {condition}\n"
                         f"Humidity: {humidity}%\n"
                         f"Wind Speed: {wind_speed} m/s"
                )
                
                save_history(city, temp, condition, humidity, wind_speed)

        except requests.exceptions.RequestException as e:
            messagebox.showerror("error", f"Connection problem: {e}")

def save_history(city, temp, condition, humidity, wind_speed):
    current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open("history.txt", "a") as file:
        file.write(f"{current_time} - {city}: Temp: {temp}°C, Condition: {condition}, "
                   f"Humidity: {humidity}%, Wind Speed: {wind_speed} m/s\n")

def clear_history():
    with open("history.txt", "w") as file:
        file.write("")
    messagebox.showinfo("information", "History cleaned")

root = tk.Tk()
root.title("Weather Forecast")

city_label = tk.Label(root, text="Enter the name of the town:")
city_label.pack()

city_entry = tk.Entry(root)
city_entry.pack()

get_weather_button = tk.Button(root, text="Get Weather", command=get_weather)
get_weather_button.pack()

result_label = tk.Label(root, text="", justify="left")
result_label.pack()

clear_history_button = tk.Button(root, text="Clean History", command=clear_history)
clear_history_button.pack()

root.mainloop()