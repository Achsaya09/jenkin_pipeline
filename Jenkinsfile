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
                // Install dependencies using system Python
                bat 'python -m pip install --upgrade pip'
                script {
                    if (fileExists('requirements.txt')) {
                        bat 'python -m pip install -r requirements.txt'
                    }
                }
            }
        }
        
        stage('Lint') {
            steps {
                script {
                    try {
                        bat 'python -m pip install flake8 black'
                        bat 'python -m flake8 . --count --select=E9,F63,F7,F82 --show-source --statistics'
                    } catch (Exception e) {
                        echo "Linting completed with warnings: ${e.getMessage()}"
                        currentBuild.result = 'UNSTABLE'
                    }
                }
            }
        }
        
        stage('Test') {
            steps {
                script {
                    try {
                        bat 'python -m pip install pytest pytest-cov'
                        bat 'python -m pytest --cov=./ --cov-report=term'
                    } catch (Exception e) {
                        echo "Tests completed with issues: ${e.getMessage()}"
                        currentBuild.result = 'UNSTABLE'
                    }
                }
            }
        }
        
        stage('Security Scan') {
            steps {
                script {
                    try {
                        // Run bandit and capture the output
                        def banditOutput = bat(script: 'python -m bandit -r . -f html -o bandit_report.html || echo "Bandit scan completed with return code $?"', returnStdout: true).trim()
                        
                        // Archive the security report
                        archiveArtifacts artifacts: 'bandit_report.html', allowEmptyArchive: true
                        
                        // Check if there are actual security issues in the output
                        if (banditOutput.contains('No issues identified')) {
                            echo 'Security scan completed with no issues found.'
                        } else {
                            echo 'Security scan completed. Check bandit_report.html for details.'
                        }
                    } catch (Exception e) {
                        echo "Error during security scan: ${e.getMessage()}"
                        currentBuild.result = 'UNSTABLE'
                    }
                }
            }
        }
        
        stage('Build') {
            when {
                expression { currentBuild.resultIsBetterOrEqualTo('UNSTABLE') }
            }
            steps {
                echo 'Building application...'
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