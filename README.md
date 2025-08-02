# 🌍 Air Quality Risk Analysis Dashboard

This project is a Streamlit-based web application that visualizes air quality, EV adoption, population risks, and health data across Indian states using MySQL as the backend database.

---

## 📊 Features

- ✅ Interactive table previews for key datasets (AQI, IDSP, Vahan, Population)
- 📈 Visualizations:
  - Top/Bottom 5 states by AQI
  - State-wise AQI trends (weekends vs weekdays)
  - EV adoption vs AQI comparison
  - Risk scores based on AQI × population density
- 🔍 Google Trends integration for purifier search behavior"
- 🧠 Stored procedures for advanced analysis
- 📍 Sidebar navigation and interactive filtering

--
## 🏗️ Tech Stack

| Tool/Library       | Purpose                         |
|--------------------|---------------------------------|
| `Streamlit`        | Web app UI                      |
| `MySQL`            | Backend database                |
| `Pandas`           | Data processing                 |
| `Altair` / `Plotly`| Data visualization              |
| `dotenv`           | Load environment variables      |
| `pytrends`         | Google search trends            |

---

## 📁 Folder Structure

```bash
├── app.py                    # Main Streamlit app
├── requirements.txt          # Python dependencies
├── .env                      # Environment variables (MySQL creds)
├── queries/
│   ├── aqi1.sql
│   ├── aqi6.sql
│   └── ev_count.sql
└── README.md                 # This file
