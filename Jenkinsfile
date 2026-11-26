
pipeline {
    agent any

    stages {

        // Stage 1: Checkout source code from GitHub
        stage('Checkout') {
            steps {
                checkout scm
            }
        }

        // Stage 2: Install dependencies and run backend tests
        stage('Backend - Install and Test') {
            steps {
                dir('backend') {
                    bat '''
                        py -3.12 -m venv .venv
                        .venv\\Scripts\\python.exe -m pip install --upgrade pip
                        .venv\\Scripts\\python.exe -m pip install -r requirements.txt
                        .venv\\Scripts\\python.exe -m pytest -v --junitxml=test-results.xml
                    '''
                }
            }

            post {
                always {
                    junit testResults: 'backend/test-results.xml',
                          allowEmptyResults: true
                }
            }
        }

        // Stage 3: Install frontend dependencies and build React
        stage('Frontend - Install and Build') {
            steps {
                dir('frontend') {
                    bat '''
                        npm install
                        npm run build
                    '''
                }
            }
        }

        // Stage 4: Verify Docker Engine
        stage('Docker - Verify Engine') {
            steps {
                bat '''
                    "C:\\Users\\deval\\AppData\\Local\\Programs\\DockerDesktop\\resources\\bin\\docker.exe" --version
                    "C:\\Users\\deval\\AppData\\Local\\Programs\\DockerDesktop\\resources\\bin\\docker.exe" info
                '''
            }
        }

        // Stage 5: Build backend and frontend Docker images
        stage('Docker - Build Images') {
            steps {
                bat '''
                    "C:\\Users\\deval\\AppData\\Local\\Programs\\DockerDesktop\\resources\\bin\\docker.exe" compose build
                '''
            }
        }
    }

    post {
        success {
            echo 'Turbo practice CI pipeline passed.'
        }

        failure {
            echo 'Turbo practice CI pipeline failed. Inspect stage logs.'
        }

        always {
            echo 'Pipeline finished.'
        }
    }
}
