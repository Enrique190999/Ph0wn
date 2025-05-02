# Ph0wn
> Clone. Hook. Own.  
> Ethical Phishing Toolkit for Local Red Team Training

Ph0wn is a lightweight, local-use-only phishing framework designed for **ethical hacking** and **web security training**. With Ph0wn you can clone public websites, inject custom login forms, and capture credentials in a controlled lab environment—all without touching live servers.

## 🧠 Key Features

- **Website Cloning**: Mirror any public site’s HTML, CSS, JS, images and media with `clone_page.py`.
- **Form Injection**: Inject custom login forms or hijack existing ones using `create_form.py` and `inject_script`.
- **Backend Capture**: Spin up a simple POST server (`post_server.py`) to log credential submissions.
- **Frontend Deployment**: Serve cloned pages locally via a socket-based web server (`start_socket_web`).
- **Rich CLI**: Interactive, styled terminal interface powered by **Rich** and **PyFiglet**.
- **Modular Design**: Tweak or extend each step—cloning, form creation, script injection, serving, and logging—independently.

## ⚙️ Prerequisites

- Python 3.8+
- Git (for cloning this repo)

Install dependencies:

```bash
pip install -r requirements.txt
```

The `requirements.txt` includes:

```txt
beautifulsoup4
requests
rich
pyfiglet
```

## 🛠️ Installation

```bash
git clone https://github.com/youruser/Ph0wn.git
cd Ph0wn
pip install -r requirements.txt
```

## 🚀 Usage

Launch the main menu:

```bash
python main.py
```

You’ll see this menu:

```
 ____  _      ___
|  _ \| |__  / _ \__      ___ __  
| |_) | '_ \| | | \ \ /\ / / '_ \ 
|  __/| | | | |_| |\ V  V /| | | |
|_|   |_| |_|\___/  \_/\_/ |_| |_|

Powered by kikedev

[Menu]
1. Create new phishing project
2. Select existing project
3. Deploy front-end
4. Deploy backend server
5. Exit
```

### 1. Create New Phishing Project

- **Step 1**: Choose a target URL:  
  ```bash
  python main.py → 1 → https://example.com
  ```
- **Step 2**: (Optional) Name your project folder or press Enter to use the domain name.  
- **Step 3**: Let Ph0wn clone assets into `www/<project_folder>/`.  
- **Step 4**: Select the `index.html` file and configure your fake login form:  
  - CSS selectors for username, password fields, and submit button.  
  - HTTP method (`GET`/`POST`/`PUT`).  
  - Target URL and JSON body template (for POST/PUT).  
- **Step 5**: Ph0wn injects a JavaScript payload to hijack credentials.

### 2. Select Existing Project

Re-inject forms or tweak settings in previously cloned sites:

```bash
python main.py → 2
```

Navigate through your `www/` folder, choose the project and file, then run `create_form` and `inject_script` again.

### 3. Deploy Front-end Server

Serve your cloned site on `http://localhost:8000`:

```bash
python main.py → 3
```

Choose your project and entry file; Ph0wn will start a socket web server for local testing.

### 4. Deploy Backend Server

Run the credential-sniffing endpoint:

```bash
python main.py → 4
```

A simple HTTP server listens on port 5000 and writes all incoming POST bodies to `logs/post_logs.txt`.

### 5. Exit

Gracefully quits the tool.

## 📂 Project Structure

```bash
Ph0wn/
├── main.py                 # Entry point / interactive menu
├── create_phishing/        # Cloning + form injection logic
│   ├── clone_page.py       # scrape & download all assets
│   ├── create_form.py      # parse HTML, prompt selectors, build payload config
│   └── utils_phishing.py   # helper functions & project navigation
├── server/                 # Local servers
│   ├── socket.py           # simple frontend host (HTTP over sockets)
│   └── post_server.py      # HTTP POST listener for credential capture
├── www/                    # Cloned sites (created at runtime)
├── logs/                   # Captured credential logs
│   └── post_logs.txt       # plain-text record of submissions
├── requirements.txt        # Python dependencies
└── README.md               # This file
```

## 🎯 Use Cases

- **Red Team Training**: Practice phishing workflows in offline labs.  
- **Education**: Teach web security concepts, XSS, form hijacking, and network forensics.  
- **Proof of Concept**: Quickly prototype phishing scams to study defense strategies.

## ⚖️ Ethical Disclaimer

**For education and authorized security assessments only.**  
Unauthorized use or deployment against live targets is strictly prohibited and may be illegal. By using Ph0wn, you **agree to comply** with all applicable laws and regulations.

Ph0wn comes with **no warranty**—use at your own risk.

---

*Hack the planet—ethically.*  
🕷️ Ph0wn
