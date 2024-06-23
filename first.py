import requests
import csv
from datetime import datetime

def get_weather_data(location, api_key):
    base_url = "http://api.weatherapi.com/v1/current.json"
    url = f"{base_url}?key={api_key}&q={location}"

    response = requests.get(url)
    
    if response.status_code == 200:
        data = response.json()
        # Extract date and time separately
        last_updated = data['current']['last_updated']
        date_time = datetime.strptime(last_updated, '%Y-%m-%d %H:%M')
        
        return {
            'date': date_time.strftime('%Y-%m-%d'),
            'time': date_time.strftime('%H:%M'),
            'city': data['location']['name'],
            'country': data['location']['country'],
            'temperature': data['current']['temp_c'],
            'humidity': data['current']['humidity'],
            'wind_speed': data['current']['wind_kph'],
            'wind_direction': data['current']['wind_dir'],
            'precipitation': data['current']['precip_mm'],
            'condition': data['current']['condition']['text']
        }
    else:
        print(f"Error fetching data for {location}: {response.status_code}")
        return None

def save_to_csv(data, filename='weather_data.csv'):
    fieldnames = ['date', 'time', 'city', 'country', 'temperature', 'humidity',
                  'wind_speed', 'wind_direction', 'precipitation', 'condition'] 

    with open(filename, 'a', newline='') as csvfile: # Remove quoting argument here
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames, quoting=csv.QUOTE_MINIMAL) # Apply quoting to the DictWriter

        if csvfile.tell() == 0:
            writer.writeheader()

        writer.writerow(data)

# Your API key (replace with your actual key)
api_key = "384490ee69f74c59a9e182400242306" 

# Main loop to repeatedly ask for locations
weather_data_list = []
while True:
    location = input("Enter a location to get weather data (or type 'exit' to quit): ")
    if location.lower() == 'exit':
        break

    weather_data = get_weather_data(location, api_key)
    if weather_data:
        weather_data_list.append(weather_data)
        print(f"Weather data for {location} fetched.")

# Save all collected data to CSV when the user exits the loop
for data in weather_data_list:
    save_to_csv(data)
print("All weather data saved to weather_data.csv")