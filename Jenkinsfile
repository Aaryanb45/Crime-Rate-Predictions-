pipeline {
    agent any

    environment {
        DOCKER_IMAGE = 'crime-rate-app'
        SONAR_SCANNER_HOME = tool 'SonarQubeScanner' // Jenkins tool name
        SONAR_HOST_URL = 'http://localhost:9000'
        SONAR_PROJECT_KEY = 'crime-rate-app'
    }

    stages {
        stage('Checkout') {
            steps {
                checkout scm
            }
        }

        stage('SonarQube Analysis') {
            steps {
                withSonarQubeEnv('SonarQubeScanner') {
                    sh '''
                    ${SONAR_SCANNER_HOME}/bin/sonar-scanner \
                    -Dsonar.projectKey=${SONAR_PROJECT_KEY} \
                    -Dsonar.sources=. \
                    -Dsonar.host.url=${SONAR_HOST_URL} \
                    -Dsonar.login=$SONAR_AUTH_TOKEN
                    '''
                }
            }
        }

        stage('Run Tests') {
            steps {
                sh 'pip install -r requirements.txt'
                sh 'python3 -m unittest discover tests'
            }
        }

        stage('Snyk Scan') {
            steps {
                withCredentials([string(credentialsId: 'snyk-token', variable: 'SNYK_TOKEN')]) {
                    sh '''
                    npm install -g snyk || true
                    snyk auth $SNYK_TOKEN
                    snyk test --file=requirements.txt || true
                    '''
                }
            }
        }

        stage('Build Docker Image') {
            steps {
                sh "docker build -t ${DOCKER_IMAGE} ."
            }
        }

        stage('Trivy Scan') {
            steps {
                sh '''
                trivy image --exit-code 0 --severity HIGH,CRITICAL ${DOCKER_IMAGE} || true
                '''
            }
        }

        stage('Run Docker Container') {
            steps {
                sh "docker run -d -p 8501:8501 ${DOCKER_IMAGE}"
            }
        }

        stage('Push to Docker Hub') {
            steps {
                withCredentials([usernamePassword(credentialsId: 'dockerhub-creds', usernameVariable: 'DOCKER_USER', passwordVariable: 'DOCKER_PASS')]) {
                    sh 'docker login -u $DOCKER_USER -p $DOCKER_PASS'
                    sh 'docker tag crime-rate-app $DOCKER_USER/crime-rate-app:latest'
                    sh 'docker push $DOCKER_USER/crime-rate-app:latest'
                }
            }
        }
    }

    post {
        always {
            echo '📦 Pipeline Completed'
        }
        success {
            echo '✅ Build Succeeded!'
        }
        failure {
            echo '❌ Build Failed!'
        }
    }
}
