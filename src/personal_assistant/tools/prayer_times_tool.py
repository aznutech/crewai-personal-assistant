import requests
from datetime import date

def get_prayer_times_tool() -> str:
    """
    Retrieves today's iftar (Maghrib) time for the provided city using the Aladhan API.
    Defaults to Faisalabad if not provided.
    """
    today = date.today().strftime("%d-%m-%Y")
    country = "Pakistan"
    city = "Faisalabad"
    url = f"http://api.aladhan.com/v1/timingsByCity?city={city}&country={country}&method=2&date={today}"
    try:
        response = requests.get(url)
        response.raise_for_status()  # Raise exception for HTTP errors
        data = response.json()
        if "data" in data and "timings" in data["data"]:
            timings = data["data"]["timings"]
            iftar_time = timings.get("Maghrib", "Not available")
            return f"Today's iftar (Maghrib) time in {city} is: {iftar_time}"
        else:
            return "Unable to retrieve prayer times from the API response."
    except Exception as e:
        return f"An error occurred while fetching prayer times: {str(e)}"
