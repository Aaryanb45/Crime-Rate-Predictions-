pipeline {
    agent any

    stages {
        stage('Clone Repo') {
            steps {
                git 'https://github.com/Aaryanb45/Crime-Rate-Predictions-.git'
            }
        }

        stage('Build Docker Image') {
            steps {
                sh 'docker build -t crime-rate-app .'
            }
        }

        stage('Run Docker Container') {
            steps {
                sh 'docker run -d -p 8501:8501 crime-rate-app'
            }
        }
    }

    post {
        failure {
            echo "❌ Something went wrong!"
        }
    }
}
