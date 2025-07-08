# 🧠 AI Navigator

**AI Navigator** is an interactive Django web application designed to visually demonstrate and compare pathfinding algorithms such as **A*** and **Dijkstra's**. It serves as both an educational tool and a fully functional game platform where users can create custom maze environments and observe real-time algorithmic decision-making.

---

## 🌐 Live Demo

https://ai-navigator-ttli.onrender.com/

---

## 🔄 Project Overview

AI Navigator enables users to:
- Create and customize game grids
- Place start/end points and obstacles
- Visualize pathfinding in real-time
- Track game statistics and performance

The system supports:
- User authentication and profile tracking
- Admin dashboard with analytics and user management
- Light/Dark mode toggling
- PostgreSQL database integration via Django ORM

---

## 🚀 Key Features

- ✨ **Interactive Grid Editor**: Drag, drop, and edit cells to simulate different maze configurations.
- 🧰 **Pathfinding Visualization**: Step-by-step animation of A* and Dijkstra's algorithm in action.
- 👤 **User Profiles**: Track game history, preferred algorithms, fastest time, and more.
- 📈 **Admin Analytics**: View user data, game stats, and system logs in a robust admin interface.
- 🔖 **Theme Toggling**: Seamless switch between light and dark modes.

---

## 🌐 Tech Stack

- **Backend**: Django, Python 3
- **Frontend**: HTML5, CSS3, JavaScript, Django Templates
- **Database**: PostgreSQL
- **Deployment**: Gunicorn, Nginx (Production Ready)

---

## 📚 Directory Structure (Simplified)

```
ai_navigator/
├── manage.py
├── ai_navigator/        # Project config
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
├── game/                # Pathfinding logic and views
│   ├── models.py
│   └── pathfinding_algorithms.py
├── users/               # Authentication and profiles
│   ├── models.py
│   └── views.py
├── templates/           # HTML templates
├── static/              # CSS, JS, images
├── requirements/        # Dependencies
├── .env                 # Sample environment config
└── README.md
```

---

## 🔄 Algorithms Implemented

### ⭐ A* Algorithm
- Uses heuristic (e.g., Manhattan distance) + path cost
- Efficient for optimal and shortest path in weighted graphs

### ♻️ Dijkstra's Algorithm
- Guarantees shortest path
- Explores all nodes based on path cost alone

---

## 🛠️ Setup Instructions
### 1. Clone Repository

```bash
git clone https://github.com/your-username/ai_navigator.git
cd ai_navigator
```

### 2. Setup Environment
```bash
python -m venv venv
source venv/bin/activate  # or venv\Scripts\activate on Windows
pip install -r requirements/production.txt
```

### 3. Database Configuration

- Set your environment variables based on `.env`
- Update `settings.py` for PostgreSQL connection
```bash
python manage.py makemigrations
python manage.py migrate
```

### 4. Run Server
```bash
python manage.py runserver
```

---

## 📊 User Statistics & Admin Interface

- Track usage of algorithms, maze complexity, time taken
- Admin dashboard: `/admin/`
- Customize views and models with filters/search
- Visualize progress with charts (Chart.js/D3.js)

---

## 🌟 Future Enhancements

- 🤖 Multi-agent coordination (CBS, prioritized planning)
- 🎨 Drag-and-drop terrain editor
- ⏱️ Performance benchmarking tools
- 🌍 Real-world map integrations (OpenStreetMap, live traffic APIs)
- ⚖️ Customizable maze generators (Prim's, Kruskal's)
- 🧰 Deep Reinforcement Learning for predictive optimization

---

## 🔒 Security Highlights

- Django ORM for SQL injection prevention
- CSRF and XSS protection enabled by default
- Passwords hashed and salted securely
- Environment variable-based configuration for secrets

---

## 👥 Contributing

Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

---

## 📧 Contact

Feel free to reach out for feedback or collaboration:
**Email**: [jbarathvishnu2005@gmail.com](mailto:jbarathvishnu2005@gmail.com)

---

## 👍 Acknowledgements

Thanks for exploring AI Navigator! We hope this project enhances your understanding of pathfinding algorithms and offers a rewarding hands-on learning experience.

---

_"Visualize the path. Learn the logic. Navigate the future."_

— Team AI Navigator
