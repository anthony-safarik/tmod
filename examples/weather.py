import requests
from bs4 import BeautifulSoup

def get_weather():
    """
    Scrapes the current temperature for South Pasadena, CA from a weather website.
    """
    url = "https://www.timeanddate.com/weather/@11788947"  # Example URL for South Pasadena weather
    try:
        response = requests.get(url)
        response.raise_for_status()  # Check for request errors
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Find the temperature element (this depends on the website's structure)
        temperature_element = soup.find('div', class_='h2')  # Adjust the class or tag as needed
        if temperature_element:
            temperature = temperature_element.text.strip()
            print(f"The current temperature in South Pasadena, CA is {temperature}.")
        else:
            print("Could not find the temperature on the page.")
    except Exception as e:
        print(f"Error: {e}")

# Example usage
get_weather()
