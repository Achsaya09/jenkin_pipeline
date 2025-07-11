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
                // Alternative using conda if available
                script {
                    try {
                        bat 'conda --version'
                        bat 'conda create -n jenkins_env python=3.11 -y'
                        bat 'conda activate jenkins_env && conda install pip -y'
                        if (fileExists('requirements.txt')) {
                            bat 'conda activate jenkins_env && pip install -r requirements.txt'
                        }
                    } catch (Exception e) {
                        echo "Conda not available, falling back to system Python"
                        if (fileExists('requirements.txt')) {
                            bat 'python -m pip install -r requirements.txt --user'
                        }
                    }
                }
            }
        }
        
        stage('Lint') {
            steps {
                script {
                    try {
                        bat 'conda activate jenkins_env && pip install flake8 black'
                        bat 'conda activate jenkins_env && python -m flake8 . --count --select=E9,F63,F7,F82 --show-source --statistics'
                    } catch (Exception e) {
                        echo "Using system Python for linting"
                        bat 'python -m pip install flake8 black --user'
                        bat 'python -m flake8 . --count --select=E9,F63,F7,F82 --show-source --statistics'
                    }
                }
            }
        }
        
        stage('Test') {
            steps {
                script {
                    try {
                        bat 'conda activate jenkins_env && pip install pytest pytest-cov'
                        bat 'conda activate jenkins_env && python -m pytest --cov=./ --cov-report=term'
                    } catch (Exception e) {
                        echo "Using system Python for testing"
                        bat 'python -m pip install pytest pytest-cov --user'
                        bat 'python -m pytest --cov=./ --cov-report=term'
                    }
                }
            }
        }
        
        stage('Security Scan') {
            steps {
                script {
                    try {
                        bat 'conda activate jenkins_env && pip install bandit'
                        bat 'conda activate jenkins_env && python -m bandit -r . -f html -o bandit_report.html'
                    } catch (Exception e) {
                        echo "Using system Python for security scan"
                        bat 'python -m pip install bandit --user'
                        bat 'python -m bandit -r . -f html -o bandit_report.html'
                    }
                }
            }
        }
        
        stage('Build') {
            steps {
                echo 'Building the application...'
                bat 'if not exist build mkdir build'
                script {
                    try {
                        bat 'copy *.py build\\ 2>nul'
                    } catch (Exception e) {
                        echo "No Python files to copy or copy failed"
                    }
                    try {
                        bat 'copy requirements.txt build\\ 2>nul'
                    } catch (Exception e) {
                        echo "No requirements.txt to copy or copy failed"
                    }
                }
                echo 'Build completed'
            }
        }
        
        stage('Deploy') {
            when {
                not { 
                    anyOf {
                        equals expected: 'FAILURE', actual: currentBuild.result
                        equals expected: 'ABORTED', actual: currentBuild.result
                    }
                }
            }
            steps {
                echo 'Deploying application...'
                echo 'Deployment completed'
            }
        }
    }
    
    post {
        always {
            script {
                try {
                    bat 'conda deactivate'
                    bat 'conda env remove -n jenkins_env -y'
                } catch (Exception e) {
                    echo "Conda cleanup not needed"
                }
            }
            cleanWs()
        }
        success {
            echo 'Pipeline completed successfully!'
        }
        unstable {
            echo 'Pipeline completed with warnings. Check the logs for details.'
        }
        failure {
            echo 'Pipeline failed. Check the logs for errors.'
        }
    }
}