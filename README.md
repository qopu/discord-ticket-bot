# Discord Ticket Bot
This is my implementation of a discord ticket bot

## Installation
> **[Python](https://www.python.org/) 3.9 or newer is required**

- **Insert token in token.txt**
- **Run program in non-stop mode** (recommended)
  ```shell
  python3 main.py &
  ```

## Commands
- **Create ticket system**

  Insert command in ticket category:
  ```shell
  /create_ticket_system
  ```
- **Clear messages**
  
  Insert command in any text channel:
  ```shell
  /clear [amount]
  ```
  
## Features
1. **Configurable.** You can fully configure the text by changing fields in `conf.json`
2. **Simple.** No useless commands and processes.
3. **Reliable.** Bot is written on discord.py API wrapper
