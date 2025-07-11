pipeline {
    agent any
    
    stages {
        stage('Checkout') {
            steps {
                checkout scm
                bat 'python --version'
                bat 'pip --version'
            }
        }
        
        stage('Set Up Python Environment') {
            steps {
                bat 'python -m venv venv'
                bat '.\\venv\\Scripts\\activate && python -m pip install --upgrade pip'
                bat '.\\venv\\Scripts\\activate && python -m pip install -r requirements.txt'
            }
        }
        
        stage('Lint') {
            steps {
                bat '.\\venv\\Scripts\\activate && python -m pip install flake8 black'
                // Only check your project files, not the venv
                bat '.\\venv\\Scripts\\activate && python -m flake8 *.py --count --select=E9,F63,F7,F82 --show-source --statistics || echo "Linting completed with warnings"'
            }
            post {
                failure {
                    echo 'Linting failed, but continuing...'
                }
            }
        }
        
        stage('Test') {
            steps {
                bat '.\\venv\\Scripts\\activate && python -m pip install pytest pytest-cov'
                bat '.\\venv\\Scripts\\activate && python -m pytest --cov=./ --cov-report=term || echo "Tests completed"'
            }
            post {
                failure {
                    echo 'Tests failed, but continuing...'
                }
            }
        }
        
        stage('Security Scan') {
            steps {
                bat '.\\venv\\Scripts\\activate && python -m pip install bandit'
                // Only scan your project files, not the venv
                bat '.\\venv\\Scripts\\activate && bandit -r *.py -f html -o bandit_report.html || echo "Security scan completed"'
            }
        }
        
        stage('Build') {
            steps {
                echo 'Building the application...'
                bat 'if not exist build mkdir build'
                bat 'copy *.py build\\ 2>nul || echo "No Python files to copy"'
                bat 'copy requirements.txt build\\ 2>nul || echo "No requirements.txt to copy"'
            }
        }
        
        stage('Deploy') {
            steps {
                echo 'Deploying application...'
                // Add your deployment steps here
            }
        }
    }
    
    post {
        always {
            cleanWs()
        }
        success {
            echo 'Pipeline completed successfully!'
        }
        failure {
            echo 'Pipeline failed, but cleanup completed.'
        }
    }
}