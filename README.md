A bot for the Discord server of ALGOSUP, a French school of Computer Science.

## Setup Guide

### 1. Create a Discord Bot
If you haven't created a bot yet, follow these steps:

1. Head over to the [Discord Developer Portal](https://discord.com/developers/applications).
2. In the top-right corner, click **"New Application"**, give it a name, and proceed.
3. In the left-hand menu, click on **"Bot"**.
4. Click **"Reset Token"**, then confirm. 
5. A new **"Copy"** button with a token code will appear. Click it to copy the token and **save it securely for later** (e.g., in a text file). **Never share this token publicly**.
6. Further down, switch on the **"Message Content Intent"**.
7. Optional: Set up additional bot details such as profile picture and description.

### 2. Invite Your Bot to a Server
To invite the bot to a server:

1. Go back to the **"General Informations"** tab and copy your application ID from there.
3. Copy the following URL and paste it into your browser.
   - `https://discord.com/oauth2/authorize?client_id=YOUR_APPLICATION_ID&permissions=68027441213137&scope=bot%20identify`
   - Make sure to replace `YOUR_APPLICATION_ID` with the value you copied before.
4. Select the server where you want to add the bot, then authorize it.

### 3. Clone the Repository
Next, download the bot's code by either:

- Cloning the repository:
  ```bash
  git clone https://github.com/leo-chartier/Algobot
  ```
- Or downloading the ZIP:
  - Go to the [repository](https://github.com/leo-chartier/Algobot) and click the **"Code"** dropdown.
  - Select **"Download ZIP"** and extract it.

### 4. Install Python (if needed)
If you haven't installed Python, download it from the [official website](https://www.python.org/downloads/). Make sure to install the latest stable version and enable the option to add Python to your system's PATH during installation.

### 5. Set Up a Virtual Environment
To manage dependencies, create and activate a virtual environment:

1. In your project folder, run:
   ```bash
   python -m venv .venv
   ```
2. Activate the virtual environment:
   - On Windows:
     ```bash
     .venv\Scripts\activate
     ```
   - On MacOS or Linux:
     ```bash
     source .venv/bin/activate
     ```

3. Install the required libraries using:
   ```bash
   pip install -r requirements.txt
   ```

### 6. Configure the Bot
Set up the bot configuration:

1. Create a new folder called **`config`** in the root directory of the project.
2. Inside the `config` folder, create a file named **`bot.json`** with the following content:
   ```json
   {
       "token": "YOUR-TOKEN-HERE"
   }
   ```
3. Replace `"YOUR-TOKEN-HERE"` with the bot token you saved earlier. **Make sure not to share this token publicly.**

### 7. Run the Bot
Now that everything is set up, you can run the bot:

1. In the terminal, execute:
   ```bash
   python main.py
   ```

Your bot should now be running and connected to your Discord server.

### 8. Deactivate the Virtual Environment (Optional)
When you’re finished, you can deactivate the virtual environment with:
```bash
deactivate
```
