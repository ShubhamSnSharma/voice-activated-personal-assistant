from __future__ import annotations
import re
import requests
from datetime import datetime
from config import OPENWEATHER_API_KEY, NEWS_API_KEY, DEFAULT_CITY, DEFAULT_NEWS_COUNTRY
from core.logger import logger
from core import reminder


def _get_time_response() -> str:
    current_time = datetime.now().strftime("%I:%M %p")
    return f"The current time is {current_time}."

def _get_date_response() -> str:
    current_date = datetime.now().strftime("%A, %B %d, %Y")
    return f"Today's date is {current_date}."

def _get_weather_response(text: str) -> str:
    if not OPENWEATHER_API_KEY:
        return "OpenWeather API key is not configured. Please add it to your .env file."
        
    city = None
    match = re.search(r'\b(?:in|for|at)\s+([a-zA-Z\s]+)', text, re.IGNORECASE)
    if match:
        city = match.group(1).strip()
        city = re.sub(r'[^\w\s]', '', city).strip()
        
        # Trim common trailing conversational words
        trailing_words = ["today", "now", "please", "currently"]
        city_words = city.split()
        if city_words:
            while city_words and city_words[-1].lower() in trailing_words:
                city_words.pop()
            city = " ".join(city_words).strip()
            
    target_city = city if city else DEFAULT_CITY
    logger.info(f"Fetching weather for: {target_city}")
    
    try:
        url = "https://api.openweathermap.org/data/2.5/weather"
        params = {
            "q": target_city,
            "appid": OPENWEATHER_API_KEY,
            "units": "metric"
        }
        response = requests.get(url, params=params, timeout=5)
        if response.status_code == 200:
            data = response.json()
            temp = data["main"]["temp"]
            desc = data["weather"][0]["description"]
            name = data["name"]
            logger.info("Weather returned")
            return f"The weather in {name} is currently {temp:.1f}°C with {desc}."
        elif response.status_code == 401:
            return "OpenWeather API key is invalid or unauthorized."
        elif response.status_code == 404:
            return f"Sorry, I could not find the city '{target_city}'."
        elif response.status_code == 429:
            return "OpenWeather API rate limit reached. Please try again in a moment."
        else:
            return "Sorry, I had trouble retrieving the weather details."
    except Exception as e:
        logger.exception("Weather request failed.")
        return "Unable to check the weather due to a network connection issue."

def _get_news_response(text: str) -> str:
    if not NEWS_API_KEY:
        return "News API key is not configured. Please add it to your .env file."
        
    categories = ["technology", "sports", "business", "science", "health", "entertainment", "general"]
    category = "general"
    text_lower = text.lower()
    for cat in categories:
        if cat in text_lower:
            category = cat
            break
            
    logger.info(f"Fetching news headlines for category: {category}")
    
    try:
        url = "https://newsapi.org/v2/top-headlines"
        params = {
            "apiKey": NEWS_API_KEY,
            "category": category,
            "country": DEFAULT_NEWS_COUNTRY,
            "pageSize": 3
        }
        response = requests.get(url, params=params, timeout=5)
        
        # NewsAPI can return 200 with an error state inside JSON payload
        data = response.json()
        if data.get("status") != "ok":
            error_msg = data.get("message", "Unable to retrieve the latest news.")
            logger.error(f"News API returned error: {error_msg}")
            if response.status_code == 401 or "apiKeyInvalid" in str(data.get("code")):
                return "News API key is invalid or unauthorized."
            elif response.status_code == 429 or "rateLimited" in str(data.get("code")):
                return "News API limit reached or quota exceeded."
            return f"News API error: {error_msg}"
            
        articles = data.get("articles", [])
        if not articles:
            return f"I could not find any current headlines for {category}."
        
        headlines = []
        for i, art in enumerate(articles[:3], 1):
            headlines.append(f"{i}. {art['title']}")
        
        headlines_str = "\n".join(headlines)
        logger.info("News returned")
        return f"Here are the top {category} headlines:\n{headlines_str}"
    except Exception as e:
        logger.exception("News request failed.")
        return "Unable to check the news due to a network connection issue."

def execute(text: str) -> tuple[bool, str | None]:
    """
    Parse and execute voice/system commands from input text.
    """
    if not text:
        return False, None
        
    text_lower = text.lower().strip()
    
    # 1. Weather Command
    if "weather" in text_lower or "temperature" in text_lower:
        logger.info("Recognized weather command")
        return True, _get_weather_response(text)
        
    # 2. News Command
    if "news" in text_lower:
        logger.info("Recognized news command")
        return True, _get_news_response(text)
        
    # 3. Time Command
    if "time" in text_lower:
        logger.info("Recognized time command")
        return True, _get_time_response()
        
    # 4. Date Command
    if "date" in text_lower or "what day is today" in text_lower:
        logger.info("Recognized date command")
        return True, _get_date_response()
        
    # 5. Reminder Command
    handled, response = reminder.handle(text)
    if handled:
        return True, response
        
    return False, None

