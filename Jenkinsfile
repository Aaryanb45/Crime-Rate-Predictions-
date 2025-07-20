pipeline {
    agent any

    environment {
        DOCKER_IMAGE = 'crime-rate-app'
        SONAR_SCANNER_HOME = tool 'SonarQubeScanner'
        SONAR_HOST_URL = 'http://localhost:9000'
        SONAR_PROJECT_KEY = 'crime-rate-app'
        PYTHON_BIN = '/Library/Frameworks/Python.framework/Versions/3.11/bin/python3'
    }

    stages {
        stage('Checkout') {
            steps {
                checkout scm
            }
        }

        stage('SonarQube Analysis') {
            steps {
                withCredentials([string(credentialsId: 'sonarqube-token1', variable: 'SONAR_AUTH_TOKEN')]) {
                    withSonarQubeEnv('SonarQubeScanner') {
                        sh """
                        \$SONAR_SCANNER_HOME/bin/sonar-scanner \\
                          -Dsonar.projectKey=\$SONAR_PROJECT_KEY \\
                          -Dsonar.sources=. \\
                          -Dsonar.exclusions=**/venv/**,**/tests/**,**/*.csv \\
                          -Dsonar.host.url=\$SONAR_HOST_URL \\
                          -Dsonar.token=\$SONAR_AUTH_TOKEN
                        """
                    }
                }
            }
        }

        stage('Run Tests') {
            steps {
                sh '${PYTHON_BIN} -m pip install -r requirements.txt'
                sh '${PYTHON_BIN} -m unittest discover || true'
            }
        }

        stage('Snyk Scan') {
            steps {
                withCredentials([string(credentialsId: 'snyk-token', variable: 'SNYK_TOKEN')]) {
                    sh '''
                    docker run --rm -v $(pwd):/project -w /project node:20 bash -c "
                        npm install -g snyk && \
                        snyk auth $SNYK_TOKEN && \
                        snyk test --file=requirements.txt --package-manager=pip --all-projects --no-update-notifier || true
                    "
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
                    sh 'docker tag ${DOCKER_IMAGE} $DOCKER_USER/${DOCKER_IMAGE}:latest'
                    sh 'docker push $DOCKER_USER/${DOCKER_IMAGE}:latest'
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
