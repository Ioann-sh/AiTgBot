### Telegram bot based on ChatGPT-3.5 TURBO  

The bot was created to interact with ChatGPT via the Telegram messenger

### Setup to start project

1) Create a "Settings.py" file with the "SETTINGS" object
 ```
   SETTINGS = {
    'TG': {
        'TOKEN': '' // telegram token
    },
    # настройки БД
    'DB': {
        'PATH': 'manager/DB/IoannAIBotDB.db'

    },
    'AI': {
        'API_KEY': '' // key from OpenAI
    }
  }
  ```
2) Run: ```pip install```
3) Run main.py
4) Enjoy
