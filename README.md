# Portfolio & Blog Website

Professional portfolio website built with Django, featuring a blog system and contact functionality.

## 🚀 Features

- **Portfolio Management**: Showcase projects with multiple images
- **Blog System**: Create and manage blog posts with categories and tags
- **About Me Section**: Display education, experience, and skills
- **Contact Form**: Telegram bot integration for receiving messages
- **Admin Panel**: Full Django admin interface for content management
- **Responsive Design**: Mobile-friendly interface

## 🛠️ Tech Stack

- **Backend**: Django 5.2.9
- **Database**: PostgreSQL
- **Rich Text Editor**: TinyMCE
- **Deployment**: Render.com
- **Static Files**: WhiteNoise

## 📦 Installation

### Prerequisites
- Python 3.10+
- PostgreSQL

### Local Setup

1. Clone the repository:
```bash
git clone <your-repo-url>
cd <project-folder>
```

2. Create virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Create `.env` file:
```env
SECRET_KEY=your-secret-key
DEBUG=True
NAME=your_db_name
USER=your_db_user
PASSWORD=your_db_password
HOST=localhost
PORT=5432
BOT_TOKEN=your_telegram_bot_token
TELEGRAM_CHAT_ID=your_chat_id
```

5. Run migrations:
```bash
python manage.py migrate
python manage.py createsuperuser
```

6. Collect static files:
```bash
python manage.py collectstatic
```

7. Run development server:
```bash
python manage.py runserver
```

Visit: `http://127.0.0.1:8000`

## 🚀 Deployment (Render.com)

1. Push code to GitHub
2. Create new Web Service on Render
3. Connect GitHub repository
4. Configure:
   - **Build Command**: `./build.sh`
   - **Start Command**: `gunicorn config.wsgi:application`
5. Add Environment Variables (SECRET_KEY, BOT_TOKEN, etc.)
6. Create PostgreSQL database and connect

## 📁 Project Structure

```
.
├── config/          # Project settings
├── portfolio/       # Portfolio app
├── blog/            # Blog app
├── templates/       # HTML templates
├── static/          # CSS, JS, images
├── media/           # User uploaded files
├── manage.py
└── requirements.txt
```

## 🔑 Environment Variables

| Variable | Description |
|----------|-------------|
| `SECRET_KEY` | Django secret key |
| `DEBUG` | Debug mode (True/False) |
| `DATABASE_URL` | PostgreSQL connection string |
| `BOT_TOKEN` | Telegram bot token |
| `TELEGRAM_CHAT_ID` | Telegram chat ID |

## 📝 Apps

### Portfolio App
- Custom User model
- About Me section
- Education & Experience
- Projects with image gallery
- Skills management
- Services showcase

### Blog App
- Blog posts with categories and tags
- Rich text content (TinyMCE)
- Comments system
- Draft/Published status

## 🤝 Contributing

This is a personal portfolio project. Feel free to fork and customize for your own use.

## 📄 License

This project is open source and available under the MIT License.

## 👤 Author

**Your Name**
- Portfolio: [Dentist site]
- GitHub: [Seymonbek]
- LinkedIn: [Seymonbek Ikromov]

## 📧 Contact

For any inquiries, please use the contact form on the website or reach out via email.

---

Made with ❤️ using Django