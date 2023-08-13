



=========================================================================================================
MESSAGE DELETE
=========================================================================================================
To delete a message using the Telegram Bot API, you can use the `deleteMessage` method. Here's a basic overview of how to use this method:

1. **API Method**: The method you'd use is `deleteMessage`.
2. **Parameters**:
   - `chat_id`: Unique identifier for the target chat or username of the target channel.
   - `message_id`: Unique message identifier.

Here's a basic example using Python's `requests` library:

```python
import requests

TOKEN = 'YOUR_TELEGRAM_BOT_TOKEN'
BASE_URL = f'https://api.telegram.org/bot{TOKEN}/'

def delete_message(chat_id, message_id):
    endpoint = f"{BASE_URL}deleteMessage"
    data = {
        "chat_id": chat_id,
        "message_id": message_id
    }
    response = requests.post(endpoint, data=data)
    return response.json()

# Usage
chat_id = "@yourchannel_or_chat_id"
message_id = 12345678  # ID of the message you want to delete
result = delete_message(chat_id, message_id)
print(result)
```

If you're using a library like `python-telegram-bot`, the process would be more streamlined. For instance:

```python
from telegram import Bot

TOKEN = 'YOUR_TELEGRAM_BOT_TOKEN'
bot = Bot(token=TOKEN)

# To delete a message
bot.delete_message(chat_id="@yourchannel_or_chat_id", message_id=12345678)
```

Keep in mind the following restrictions when deleting messages:

- A bot can only delete its own messages or messages in supergroups and channels where it has the `Delete messages` permission.
- It is not possible to delete messages older than 48 hours in supergroups and channels.