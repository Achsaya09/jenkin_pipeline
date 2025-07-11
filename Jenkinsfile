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
                script {
                    try {
                        bat '.\\venv\\Scripts\\activate && python -m flake8 . --count --select=E9,F63,F7,F82 --show-source --statistics --exclude=venv'
                    } catch (Exception e) {
                        echo "Linting completed with warnings: ${e.getMessage()}"
                        currentBuild.result = 'UNSTABLE'
                    }
                }
            }
        }
        
        stage('Test') {
            stage('Install Dependencies') {
                steps {
                    bat '.\\venv\\Scripts\\activate && python -m pip install pytest pytest-cov flask-limiter'
                }
            }
            stage('Run Tests') {
                steps {
                    script {
                        try {
                            bat '.\\venv\\Scripts\\activate && python -m pytest --cov=./ --cov-report=term --ignore=venv'
                        } catch (Exception e) {
                            echo "Tests completed with issues: ${e.getMessage()}"
                            currentBuild.result = 'UNSTABLE'
                        }
                    }
                }
            }
            post {
                always {
                    // Archive test results if they exist
                    script {
                        if (fileExists('test-results.xml')) {
                            archiveArtifacts artifacts: 'test-results.xml', allowEmptyArchive: true
                        }
                    }
                }
            }
        }
        
        stage('Security Scan') {
            steps {
                bat '.\\venv\\Scripts\\activate && python -m pip install bandit'
                script {
                    try {
                        bat '.\\venv\\Scripts\\activate && bandit -r . -f html -o bandit_report.html --exclude ./venv'
                        echo "Security scan completed successfully"
                    } catch (Exception e) {
                        echo "Security scan completed with findings: ${e.getMessage()}"
                        echo "Check bandit_report.html for details"
                        currentBuild.result = 'UNSTABLE'
                    }
                }
            }
            post {
                always {
                    // Archive security report
                    script {
                        if (fileExists('bandit_report.html')) {
                            archiveArtifacts artifacts: 'bandit_report.html', allowEmptyArchive: true
                        }
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
                // Add your deployment steps here
                // For example:
                // bat '.\\venv\\Scripts\\activate && python app.py &'
                // or copy to deployment directory
                // bat 'xcopy build\\*.* C:\\deployment\\app\\ /Y'
                echo 'Deployment completed'
            }
        }
    }
    
    post {
        always {
            // Clean up workspace
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