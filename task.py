import requests
from bs4 import BeautifulSoup
import matplotlib.pyplot as plt
import time
from datetime import datetime, timedelta
import pytz

# Function to scrape temperature and rain presence from the website
def scrape_weather():
    try:
        url = "https://www.metoffice.gov.uk/weather/forecast/gcpvjvs94"
        response = requests.get(url)
        soup = BeautifulSoup(response.text, "html.parser")
        
        temperature_element = soup.find("span", {"class": "wr-value--temperature--c"})
        rain_element = soup.find("span", {"class": "wr-value--wx-type"})
        
        if temperature_element and rain_element:
            temperature = temperature_element.text.strip()
            rain_presence = 1 if "rain" in rain_element.text.lower() else 0
            return temperature, rain_presence
        else:
            raise Exception("Temperature or rain data not found on the webpage.")
    except Exception as e:
        print("Error scraping weather data:", e)
        return None, None


# Function to plot the data
def plot_weather_data(timestamps, temperatures, rain_presence):
    plt.figure(figsize=(10, 6))
    plt.plot(timestamps, temperatures, label="Temperature (°C)", color='r')
    plt.plot(timestamps, rain_presence, label="Rain Presence", color='b')
    plt.xlabel("Time (MST)")
    plt.ylabel("Temperature (°C) / Rain Presence")
    plt.title("Weather Data for London")
    plt.legend()
    plt.xticks(rotation=45)
    plt.grid(True)
    plt.tight_layout()
    plt.show()

# Function to save weather data to a text file
def save_weather_data(timestamps, temperatures, rain_presence, error_message=None):
    with open("weather_data.txt", "w") as file:
        file.write("Timestamp\tTemperature (°C)\tRain Presence\n")
        if error_message:
            file.write(f"Error: {error_message}\n")
        else:
            for i in range(len(timestamps)):
                file.write(f"{timestamps[i]}\t{temperatures[i]}\t{rain_presence[i]}\n")

# Main function
def main():
    # Lists to store data
    timestamps = []
    temperatures = []
    rain_presence = []
    error_message = None
    
    # Start time
    start_time = datetime.now()
    
    # Timezone setup
    mst = pytz.timezone('MST')
    
    # Collect data for 10 minutes at 2-second intervals
    while (datetime.now() - start_time).total_seconds() < 600:
        temperature, rain = scrape_weather()
        if temperature is not None:
            temperatures.append(float(temperature))
            rain_presence.append(rain)
            timestamps.append(datetime.now(pytz.utc).astimezone(mst).strftime('%H:%M:%S'))
        else:
            error_message = "Temperature or rain data not found on the webpage."
        time.sleep(2)
    
    # Save the data to a text file
    save_weather_data(timestamps, temperatures, rain_presence, error_message)

    # Plot the data
    plot_weather_data(timestamps, temperatures, rain_presence)

if __name__ == "__main__":
    main()
