
---

# Mimi Peri LINE Bot

**Mimi Peri LINE Bot** is a chill and quirky chatbot built for the LINE messaging platform, powered by Flask, the LINE Bot SDK, and Google’s Gemini AI (`gemini-2.0-flash`). This bot, now rocking the persona "Mimi Peri," delivers a laid-back, informal vibe with a playful twist inspired by the iconic "Mimi Peri" style—think loud "SAHUUUUUUURRRR" wake-up calls and casual, non-standard Indonesian slang. Deployed using Pyngrok for public access, it supports both personal and group chats, storing up to 10 messages per user for context-aware replies. Users can toggle the bot on or off with `/on` and `/off` commands, and it greets new users or group invites with sassy lines like "Woi, sopan santunnya mana?" or "Ngapain invite gw bro?". With multiple Gemini API keys for failover, this bot ensures reliable, fun interactions—perfect for casual banter or a dose of personality-packed AI flair.

---

## Prerequisites

Before running the bot, make sure you have the following installed:
- **Python 3.8+**: The bot is built with Python.
- **pip**: Python package manager to install dependencies.
- **Ngrok Account**: For exposing the local server to the internet (get your auth token from [ngrok.com](https://ngrok.com)).

---

## Dependencies

Install the required Python packages using `pip`. Run the following command:

```bash
pip install flask line-bot-sdk google-generativeai pyngrok psutil requests
```

### Package Details
- **`flask`**: Web framework to handle HTTP requests.
- **`line-bot-sdk`**: LINE Messaging API SDK for Python.
- **`google-generativeai`**: Google Gemini AI SDK for generating responses.
- **`pyngrok`**: Python wrapper for Ngrok to create a public URL.
- **`psutil`**: Used for system monitoring (though not heavily utilized in this code).
- **`requests`**: For making HTTP requests (e.g., to Gemini API).

---

## Installation

1. **Clone the Repository**  
   Clone this project to your local machine:
   ```bash
   git clone https://github.com/your-username/mimiperi-line-bot.git
   cd mimiperi-line-bot
   ```

2. **Install Dependencies**  
   Install all required packages:
   ```bash
   pip install -r requirements.txt
   ```
   If you don’t have a `requirements.txt` yet, create one with:
   ```plaintext
   flask
   line-bot-sdk
   google-generativeai
   pyngrok
   psutil
   requests
   ```
   Then run the install command above.

3. **Set Up LINE Credentials**  
   - Get your `LINE_ACCESS_TOKEN` and `LINE_CHANNEL_SECRET` from the [LINE Developers Console](https://developers.line.biz/).
   - Replace the placeholders in the code:
     ```python
     LINE_ACCESS_TOKEN = "JzOsJ82qHSqnjA45laD5aLHwZBKhY9mY3tCG/EHp8o3EIxtLyf6zvtER1l2mslRZnkW1PNQ+cW4AOVGnRf5xg96GZUJ4kKC2PP6DHmpjtUXwsOvQ+aq9c5JlyFJW3dsSwoJz6SdL+6GL4Q+f0e8NcgdB04t89/1O/w1cDnyilFU="
     LINE_CHANNEL_SECRET = "632ef8b2bf62b8f20bb9e62eb33a0560"
     ```

4. **Set Up Gemini API Keys**  
   - Replace the `GEMINI_API_KEYS` list with valid Google Gemini API keys:
     ```python
     GEMINI_API_KEYS = [
         "YOUR_API_KEY_1",
         "YOUR_API_KEY_2",
         "YOUR_API_KEY_3",
         "YOUR_API_KEY_4"
     ]
     ```
   - Get your API keys from the [Google AI Studio](https://makersuite.google.com/).

5. **Set Up Ngrok**  
   - Sign up at [ngrok.com](https://ngrok.com) and get your auth token.
   - Replace the placeholder in the code:
     ```python
     ngrok.set_auth_token("YOUR_NGROK_AUTH_TOKEN")
     ```

---

## Running the Bot

1. **Start the Bot**  
   Run the script:
   ```bash
   python app.py
   ```
   - This will start the Flask server on port `8021` and launch Ngrok to create a public URL.

2. **Get the Public URL**  
   - Once running, check the terminal for the Ngrok public URL (e.g., `http://abc123.ngrok.io`).
   - Copy this URL.

3. **Configure LINE Webhook**  
   - Go to the LINE Developers Console.
   - Set the Webhook URL to your Ngrok URL plus `/callback` (e.g., `http://abc123.ngrok.io/callback`).
   - Enable "Use webhook" in the console.

4. **Test the Bot**  
   - Open LINE, add the bot as a friend, or invite it to a group.
   - Send a message and watch "Mimi Peri" respond with its santuy vibes!

---

## Features

- **Toggle AI**: Use `/on` to enable or `/off` to disable the bot.
- **Chat History**: Stores up to 10 messages per user for context-aware replies.
- **Group Support**: Works in both personal and group chats.
- **Failover**: Automatically switches between multiple Gemini API keys if one fails.
- **Personality**: Responds as "Mimi Peri" with casual, playful Indonesian slang.

---

## Troubleshooting

- **Ngrok URL Not Working**: Ensure your auth token is correct and restart the script.
- **No Response**: Check if the Gemini API keys are valid and not rate-limited.
- **Webhook Errors**: Verify the LINE channel secret and access token match the console settings.

---

## Credits

- Built with ❤️ by Arshad.

---
