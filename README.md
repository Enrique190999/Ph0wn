# 🕷️ Ph0wn

> Clone. Hook. Own.  
> Educational phishing framework for local red-team simulations.

## 💀 What is Ph0wn?

Ph0wn is a local-use-only phishing toolkit designed for **ethical hacking** and **web security training**. It allows you to:

- Clone any webpage's frontend with `create_phishing/clone_page.py`.
- Inject customizable login forms using `create_form.py`.
- Launch a backend server to capture POST credentials in a controlled environment.
- Log data locally for analysis and educational review.

⚠️ **This tool is for educational and authorized use only. Misuse will get you burned. 🔥**

---

## 🧠 Features

- 🔗 Webpage cloning via `requests` + `BeautifulSoup`
- 🎭 Fake login form generation with field mapping
- 📡 Local server to capture POST requests (`post_server.py`)
- 🕵️ Credential logging in plain text (`logs/post_logs.txt`)
- 📦 Lightweight and standalone (no Docker or fancy setup)

---

## ⚙️ How to Use (Local Lab)

```bash
# 1. Clone target site
python create_phishing/clone_page.py -u https://example.com -o cloned_site.html

# 2. Inject a login form
python create_phishing/create_form.py -i cloned_site.html -o phishing_site.html

# 3. Start the backend sniffer
python server/post_server.py

# 4. Open phishing_site.html locally and test login submission
    