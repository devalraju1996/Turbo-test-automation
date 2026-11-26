
pipeline {
    agent any

    stages {

        stage('Checkout') {
            steps {
                checkout scm
            }
        }

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

        stage('Docker - Verify Engine') {
            steps {
                bat '''
                    "C:\\Users\\deval\\AppData\\Local\\Programs\\DockerDesktop\\resources\\bin\\docker.exe" --version
                    "C:\\Users\\deval\\AppData\\Local\\Programs\\DockerDesktop\\resources\\bin\\docker.exe" info
                '''
            }
        }

        stage('Docker - Build Images') {
            steps {
                bat '''
                    "C:\\Users\\deval\\AppData\\Local\\Programs\\DockerDesktop\\resources\\bin\\docker-compose.exe" build
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
