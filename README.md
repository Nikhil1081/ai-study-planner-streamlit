# 🎓 AI Study Planner - Streamlit Edition

An intelligent AI-powered study planner chatbot built with **Streamlit** and **Google Gemini API**. Create personalized study schedules for 10th, 12th, B.Tech, and MBA students with smart AI assistance.

![Powered by Gemini API](https://img.shields.io/badge/Powered%20by-Gemini%20API-blue)
![Built with Streamlit](https://img.shields.io/badge/Built%20with-Streamlit-FF4B4B)
![Python 3.8+](https://img.shields.io/badge/Python-3.8%2B-blue)

## 🌟 Features

### 📅 Smart Study Plan Generator
- **Personalized Schedules**: AI-generated hour-by-hour study plans
- **Multiple Education Levels**: Support for 10th, 12th, B.Tech, MBA
- **Weak Subject Focus**: Extra time allocation for challenging topics
- **Revision Sessions**: Automated revision scheduling
- **Flexible Timing**: Customize daily study hours

### 💬 AI Chat Assistant
- **24/7 Study Help**: Get instant answers to study-related questions
- **Subject Doubts**: Clarify concepts across all subjects
- **Study Techniques**: Learn effective memory and learning methods
- **Motivation**: Get encouragement and productivity tips
- **Context-Aware**: Remembers previous conversation

### 📊 Progress Dashboard
- **Task Management**: Create and track study tasks
- **Priority System**: High, Medium, Low priority levels
- **Subject-wise Tracking**: Monitor progress by subject
- **Analytics**: Visualize completion rates and insights
- **Data Export**: Download tasks and plans

## 🚀 Quick Start

### Prerequisites
- Python 3.8 or higher
- Google Gemini API key ([Get it here](https://makersuite.google.com/app/apikey))

### Installation

1. **Clone the repository:**
```bash
git clone https://github.com/Nikhil1081/ai-study-planner-streamlit.git
cd ai-study-planner-streamlit
```

2. **Install dependencies:**
```bash
pip install -r requirements.txt
```

3. **Configure API Key:**
   - Open `Home.py` and update the `GEMINI_API_KEY` with your API key
   - Or use Streamlit secrets (recommended for deployment)

4. **Run the app:**
```bash
streamlit run Home.py
```

5. **Open your browser:**
   - Navigate to `http://localhost:8501`

## 📁 Project Structure

```
ai-study-planner-streamlit/
│
├── Home.py                      # Main landing page
├── pages/
│   ├── 1_📅_Study_Planner.py   # Study plan generator
│   ├── 2_💬_Chat.py             # AI chat assistant
│   └── 3_📊_Dashboard.py        # Progress dashboard
│
├── .streamlit/
│   └── config.toml              # Streamlit configuration
│
├── requirements.txt             # Python dependencies
├── README.md                    # This file
└── .gitignore                   # Git ignore rules
```

## 🎯 Usage Guide

### 1. Generate Study Plan
1. Navigate to **📅 Study Planner** page
2. Fill in your details:
   - Name
   - Education level
   - Subjects to study
   - Exam date
   - Daily study hours
   - Weak subjects (optional)
3. Click **Generate Study Plan**
4. Download your personalized plan

### 2. Chat with AI Assistant
1. Go to **💬 Chat** page
2. Type your study-related questions
3. Use quick topic buttons for common queries
4. Export chat history if needed

### 3. Track Progress
1. Open **📊 Dashboard** page
2. Add tasks with priority levels
3. Mark tasks as complete
4. View progress analytics
5. Export data for backup

## 🔑 API Configuration

### Using Environment Variables (Recommended)
Create `.streamlit/secrets.toml`:
```toml
GEMINI_API_KEY = "your_api_key_here"
```

Then in your code:
```python
import streamlit as st
GEMINI_API_KEY = st.secrets["GEMINI_API_KEY"]
```

## 🌐 Deploy to Streamlit Cloud

1. **Push to GitHub:**
```bash
git init
git add .
git commit -m "Initial commit"
git remote add origin https://github.com/Nikhil1081/ai-study-planner-streamlit.git
git push -u origin main
```

2. **Deploy on Streamlit Cloud:**
   - Go to [share.streamlit.io](https://share.streamlit.io)
   - Sign in with GitHub
   - Select your repository
   - Add `GEMINI_API_KEY` in secrets
   - Click Deploy!

## 💡 Tips for Best Results

### Study Plans
- Be specific with subjects (e.g., "Physics - Thermodynamics" instead of just "Physics")
- Include all weak subjects for better time allocation
- Set realistic exam dates and study hours
- Use advanced options to customize intensity

### Chat Assistant
- Ask specific questions for detailed answers
- Mention your education level for tailored advice
- Use follow-up questions to dig deeper
- Try the quick topic buttons for common queries

### Dashboard
- Add tasks immediately after creating a study plan
- Set priorities based on exam proximity
- Review progress weekly
- Clear completed tasks regularly

## 🛠️ Tech Stack

- **Frontend:** Streamlit
- **AI Engine:** Google Gemini API (gemini-flash-latest)
- **Language:** Python 3.8+
- **State Management:** Streamlit Session State
- **HTTP Client:** Requests

## 📊 Supported Education Levels

| Level | Subjects Covered |
|-------|------------------|
| **10th Standard** | Math, Science, Social Studies, Languages |
| **12th Science** | Physics, Chemistry, Math, Biology |
| **12th Commerce** | Accountancy, Business Studies, Economics |
| **12th Arts** | History, Political Science, English |
| **B.Tech (CS)** | DSA, OS, DBMS, Networks, Programming |
| **B.Tech (Other)** | Core Engineering Subjects |
| **MBA** | Finance, Marketing, Operations, HR |

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📝 License

This project is open source and available under the [MIT License](LICENSE).

## 👤 Author

**Nikhil**
- GitHub: [@Nikhil1081](https://github.com/Nikhil1081)

## 🙏 Acknowledgments

- **Google Gemini API** for powering the AI features
- **Streamlit** for the amazing framework
- All students who use this tool for their studies

## 📞 Support

If you find this project helpful, please give it a ⭐ on GitHub!

For issues or questions:
- Open an issue on GitHub
- Contact via GitHub profile

---

**Built with ❤️ for students worldwide | Powered by Gemini API**
