# 🕵️‍♂️ Crime Rate Prediction Dashboard

An end-to-end machine learning pipeline to analyze and predict crime rates using clustering and regression techniques.  
The project features a fully interactive Streamlit dashboard, CI/CD integration, and security/static code analysis.

---

## 🚀 Project Overview

This project leverages real-world crime datasets to:

- Perform data preprocessing, clustering, and regression-based prediction.
- Visualize insights using Plotly interactive charts.
- Enable filtering and data exploration through an intuitive Streamlit UI.

---

## ✨ Features

- 📊 **Dynamic Dashboard**: Built with Streamlit & Plotly for seamless interaction.
- 🤖 **ML-Powered Predictions**: Scikit-learn models for clustering & forecasting crime.
- 🐳 **Containerized**: Packaged with Docker for portable deployment.
- 🔁 **CI/CD Integration**: Jenkins pipeline with stages for testing, Docker build, Trivy scan, and DockerHub push.
- ✅ **Quality & Security**:
  - SonarQube for static code analysis
  - Snyk for Python dependency vulnerability scanning

---

## 🛠️ Tech Stack

| Category           | Tools/Libraries                     |
|--------------------|--------------------------------------|
| **Language**        | Python 3.11                          |
| **Frontend**        | Streamlit, Plotly                    |
| **ML/DS Libraries** | Scikit-learn, Pandas, Seaborn        |
| **DevOps**          | Docker, Jenkins, GitHub              |
| **Code Analysis**   | SonarQube, Snyk                      |

---

## ⚙️ Setup Instructions

### 🔁 Clone Repository
```bash
git clone https://github.com/<your-username>/crime-rate-prediction.git
cd crime-rate-prediction

```

📦 Install Dependencies
<pre> <code>pip install -r requirements.txt</code> </pre>

▶️ Run Streamlit Dashboard
<pre> <code>streamlit run app.py</code> </pre>

🧪 Run Unit Tests
<pre> <code>python3 -m unittest discover</code> </pre>

🐳 Docker Usage
🔨 Build Docker Image
<pre> <code>docker build -t crime-rate-app .</code> </pre>

▶️ Run Docker Container
<pre> <code>docker run -d -p 8501:8501 crime-rate-app</code> </pre>

🧬 CI/CD Pipeline (Jenkins)

✅ SonarQube code quality analysis

🧪 Python unit testing

🐳 Docker image build & scan with Trivy

🚀 DockerHub push

🔐 Security scan using Snyk

📁 Project Structure
<pre> <code> crime-rate-prediction/ ├── app.py ├── requirements.txt ├── Dockerfile ├── Jenkinsfile ├── data/ ├── models/ ├── notebooks/ ├── tests/ └── README.md </code> </pre>

📄 License

Licensed under the MIT License.




