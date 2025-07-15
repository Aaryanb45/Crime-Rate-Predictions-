pipeline {
    agent any

    environment {
        DOCKER_IMAGE = 'crime-rate-app'
    }

    stages {
        stage('Clone Repo') {
            steps {
                git 'https://github.com/Aaryanb45/Crime-Rate-Predictions-.git'
            }
        }

        stage('Build Docker Image') {
            steps {
                script {
                    sh 'docker build -t $DOCKER_IMAGE .'
                }
            }
        }

        stage('Run Docker Container') {
            steps {
                script {
                    // Stop any running container on 8501
                    sh 'docker rm -f crime-rate-container || true'

                    // Run new container
                    sh 'docker run -d -p 8501:8501 --name crime-rate-container $DOCKER_IMAGE'
                }
            }
        }
    }

    post {
        success {
            echo "🚀 App deployed on http://localhost:8501"
        }
        failure {
            echo "❌ Something went wrong!"
        }
    }
}
