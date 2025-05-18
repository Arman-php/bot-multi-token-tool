# Multi-Bot Discord Spammer

> **WARNING:** This tool is for educational purposes only.  
> Using it to spam, harass, or violate Discord's Terms of Service will get you and your bots banned.  
> You are fully responsible for your actions.

---

## 🚀 What is this?

**Multi-Bot Discord Spammer** is a Python tool that lets you control a fleet of Discord bots to:

- Spam DMs to a user
- Spam mention tags in a channel
- Showcase (for demonstration) the base64-encoded user ID as a token stub
- All via easy commands in Discord, with neat black-embedded responses

Perfect for stress-testing your own server or, you know, showing your friends how NOT to piss you off.  
(But seriously, use responsibly.)

---

## 💻 Features

- **Multi-token support:** Run a whole army of bots from one script
- **Whitelist:** Only you (or specified user IDs) can run commands
- **Black-themed embeds:** All response messages look clean and pro
- **No-nonsense UI:** No clutter, no noise, just the commands you want
- **Single-bot help:** Only one bot responds to `a!help`/`a!commands` so you don't get flooded

---

## 🛠️ Commands

```text
a!help
```
Shows the embedded help menu.

```text
a!spamdm @user [times] [message]
```
Sends DMs to a user from all bots.  
*times* defaults to 10, *message* defaults to "Hello".

```text
a!spamtag @user [times]
```
Mentions the user in the current channel from all bots.  
*times* defaults to 10.

```text
a!gettoken @user
```
Displays the base64-encoded user ID plus `*` for the rest, to mimic a token stub (for demonstration).

---

## ⚙️ Setup / Config

1. **Install requirements:**
    ```sh
    pip install discord.py httpx
    ```

2. **Fill `tokens.txt`:**  
   Put each bot token on a new line.

3. **Edit your whitelist:**  
   Change the `allowed_user_command` set in the script to your Discord user ID.

4. **Run it:**
    ```sh
    main.py
    ```

---

## ⚠️ Disclaimer

- Again, **do not** use this for malicious purposes.
- You will get banned if you abuse this.
- For learning, testing, and fun with your own bots.  
  Not for annoying strangers.

---
