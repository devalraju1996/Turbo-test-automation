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
                        py -3.11 -m venv .venv
                        .venv\\Scripts\\python.exe -m pip install --upgrade pip
                        .venv\\Scripts\\python.exe -m pip install -r requirements.txt
                        .venv\\Scripts\\python.exe -m pytest -v --junitxml=test-results.xml
                    '''
                }
            }
            post {
                always {
                    junit testResults: 'backend/test-results.xml', allowEmptyResults: true
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
    }

    post {
        success { echo 'Turbo practice CI pipeline passed.' }
        failure { echo 'Turbo practice CI pipeline failed. Inspect stage logs.' }
        always { echo 'Pipeline finished.' }
    }
}
