# Enterprise Policy Management System

An AI-powered enterprise policy management system that helps organizations keep their policies aligned with government regulations, reducing compliance risks and ensuring seamless policy updates.

## 🚀 Why It Matters
Managing enterprise policies is a complex, time-consuming process. Policies frequently change due to government regulations, and ensuring compliance can be a major challenge. This system automates policy tracking, AI-powered analysis, and approval workflows, making policy management effortless and efficient.

## 🔍 How It Works
1. **AI-Powered Analysis** – The system leverages Google's Gemini AI to analyze policies, detect inconsistencies, and recommend improvements.
2. **Automated Updates** – Government regulation changes are automatically incorporated into relevant policies.
3. **Policy Version Control** – Track all policy modifications and maintain an auditable history.
4. **Approval Workflow** – Policy changes go through an approval pipeline to ensure compliance before implementation.
5. **Enterprise Dashboard** – A user-friendly interface to manage policies, approvals, and compliance tracking in one place.

## 🛠 Built With
- **Python 3.11+** – Backend logic and AI integration.
- **Streamlit** – Interactive frontend UI.
- **PostgreSQL** – Database for policy storage and version control.
- **Google Gemini AI** – AI-powered policy recommendations.
- **Google Cloud Platform** – OAuth authentication and API hosting.
- **Alembic** – Database migration tool.

---

## 🌟 Features
- ✅ Google Sign-In and username/password authentication.
- ✅ Enterprise policy management dashboard.
- ✅ AI-powered policy analysis and recommendations using Google's Gemini AI.
- ✅ Automatic policy updates based on government regulation changes.
- ✅ Policy version control and history tracking.
- ✅ Policy approval workflow.

## 📌 Prerequisites
Before you begin, ensure you have the following:
- **Python 3.11+** installed on your system.
- **PostgreSQL database** set up and running.
- **Google Cloud Platform account** for authentication.
- **Google API Key** to access Gemini AI services.

## 🔑 Environment Variables
Set up the following environment variables:
```env
DATABASE_URL=postgresql://your_database_url
GOOGLE_API_KEY=your_gemini_api_key
GOOGLE_CLIENT_ID=your_google_oauth_client_id
```

---

## ⚡ Installation & Setup

1️⃣ **Clone the repository:**
```bash
git clone https://github.com/yourusername/enterprise-policy-manager.git
cd enterprise-policy-manager
```

2️⃣ **Install dependencies:**
```bash
pip install -r requirements.txt
```

3️⃣ **Run database migrations:**
```bash
alembic upgrade head
```

4️⃣ **Start the application:**
```bash
streamlit run main.py
```
The application will be available at `http://localhost:5000`

---

## 📂 Project Structure
```
├── .streamlit/       # Streamlit configuration
├── auth/            # Authentication modules
├── components/      # UI components
├── migrations/      # Database migrations
├── models/         # Database models
├── static/         # Static assets
├── utils/          # Utility functions
└── main.py         # Main application file
```

---

## 🎯 Usage
1. **Sign in** using your Google account or create a username/password.
2. **Upload enterprise policies** for AI-powered analysis.
3. **Receive AI-driven policy recommendations** and suggested updates.
4. **Review and approve/reject changes** via the dashboard.
5. **Track policy versions and changes** over time.

---

## 🤝 Contributing
We welcome contributions! 🚀 If you’d like to enhance this project:
- Fork the repository
- Create a new feature branch (`git checkout -b feature-branch`)
- Commit your changes (`git commit -m "Added a new feature"`)
- Push to your branch (`git push origin feature-branch`)
- Open a Pull Request

---

### 📜 License
This project is licensed under the [MIT License](LICENSE).

💡 *Have ideas to improve this project? Feel free to contribute!*

