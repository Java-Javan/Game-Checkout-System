# 🎲 Game Management System

A Python-based web application designed to manage a large collection of board games and streamline the process of lending and borrowing games among friends and neighbors.

⚠️ **Disclaimer**: This project is currently for **personal use and learning purposes only**. The admin login system uses a simple hardcoded username/password in the codebase, which is not secure for production. Future versions will implement proper authentication.

🌐 **Deployment**: The app is hosted on [Render](https://render.com), making it accessible from any device via a single QR code link.

---

## 🚀 Features (current + planned)
- Keep track of all owned games.
- Track which games are **available** vs **checked out**.
- QR code support:
  - Users can scan a single QR code to access the site.
  - Direct access to the **checkout page** from mobile.
- User checkout form:
  - Select a game from a searchable dropdown list.
  - Enter name and checkout date.
- Admin page (restricted access):
  - Login with a hardcoded username/password (**learning placeholder**).
  - Add new games to the system.
  - View all games in the collection.
  - Filter by **available** vs **checked out**.

---

## 🛠️ Tech Stack
- **Backend**: Flask (Python)
- **Database**: SQLite
- **Frontend**: HTML/CSS + simple JavaScript
- **Deployment**: Render (cloud hosting)
- **Other tools**: QR Code integration for quick mobile access

---

## 📦 Installation (Local Dev)
Clone the repo and set up a virtual environment:
```bash
git clone https://github.com/Java-Javan/game-management-system.git
cd game-management-system
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt