pipeline {
    agent any
    
    environment {
        // Load environment variables from .env file
        ENV_FILE = '.env'
        // Python version can be changed based on your requirements
        PYTHON_VERSION = '3.9'
        // Set VENV_ACTIVATE based on the OS
        VENV_ACTIVATE = "${isUnix() ? 'source venv/bin/activate' : '.\\venv\\Scripts\\activate'}"
    }
    
    stages {
        stage('Checkout') {
            steps {
                // Checkout code from your version control system
                checkout scm
                
                // Print Python version for debugging
                sh 'python --version'
                sh 'pip --version'
            }
        }
        
        stage('Set Up Python Environment') {
            steps {
                script {
                    // Create and activate virtual environment
                    sh "python -m venv venv"
                    
                    // Use the appropriate activation command based on OS
                    if (isUnix()) {
                        sh "${VENV_ACTIVATE} && pip install --upgrade pip"
                        sh "${VENV_ACTIVATE} && pip install -r requirements.txt"
                        sh "${VENV_ACTIVATE} && pip install pytest pytest-cov"
                    } else {
                        bat "${VENV_ACTIVATE} && python -m pip install --upgrade pip"
                        bat "${VENV_ACTIVATE} && python -m pip install -r requirements.txt"
                        bat "${VENV_ACTIVATE} && python -m pip install pytest pytest-cov"
                    }
                }
            }
        }
        
        stage('Lint') {
            steps {
                script {
                    // Install linters
                    if (isUnix()) {
                        sh "${VENV_ACTIVATE} && pip install flake8 black"
                    } else {
                        bat "${VENV_ACTIVATE} && python -m pip install flake8 black"
                    }
                    
                    // Run flake8 for code style checking
                    sh "flake8 . --count --select=E9,F63,F7,F82 --show-source --statistics"
                    sh "flake8 . --count --max-complexity=10 --max-line-length=127 --statistics"
                    
                    // Run black for code formatting
                    sh "black --check --diff ."
                }
            }
        }
        
        stage('Test') {
            steps {
                script {
                    // Run pytest with coverage
                    if (isUnix()) {
                        sh "${VENV_ACTIVATE} && pytest --cov=./ --cov-report=xml --cov-report=term"
                    } else {
                        bat "${VENV_ACTIVATE} && python -m pytest --cov=./ --cov-report=xml --cov-report=term"
                    }
                    
                    // Archive test results
                    junit '**/test-reports/*.xml'
                    
                    // Publish coverage report
                    publishHTML(target: [
                        allowMissing: false,
                        alwaysLinkToLastBuild: false,
                        keepAll: true,
                        reportDir: 'htmlcov',
                        reportFiles: 'index.html',
                        reportName: 'HTML Report',
                        reportTitles: 'Coverage Report'
                    ])
                }
            }
        }
        
        stage('Security Scan') {
            steps {
                script {
                    // Run bandit for security scanning
                    if (isUnix()) {
                        sh "${VENV_ACTIVATE} && pip install bandit"
                        sh "${VENV_ACTIVATE} && bandit -r . -f html -o bandit_report.html || true"
                    } else {
                        bat "${VENV_ACTIVATE} && python -m pip install bandit"
                        bat "${VENV_ACTIVATE} && bandit -r . -f html -o bandit_report.html || true"
                    }
                    
                    // Archive security report
                    publishHTML(target: [
                        allowMissing: true,
                        alwaysLinkToLastBuild: true,
                        keepAll: true,
                        reportDir: '.',
                        reportFiles: 'bandit_report.html',
                        reportName: 'Security Report',
                        reportTitles: 'Bandit Security Report'
                    ])
                }
            }
        }
        
        stage('Build') {
            steps {
                script {
                    // Any build steps specific to your project
                    echo 'Building the application...'
                    
                    // Example: Create necessary directories
                    sh 'mkdir -p build'
                    
                    // Example: Copy required files to build directory
                    sh 'cp -r app.py requirements.txt templates/ build/'
                }
            }
        }
        
        stage('Deploy (Staging)') {
            when {
                // Only deploy to staging if not on main branch
                not { branch 'main' }
            }
            steps {
                script {
                    // Add your staging deployment steps here
                    echo 'Deploying to staging environment...'
                    // Example: Deploy to a staging server or container registry
                }
            }
        }
        
        stage('Deploy (Production)') {
            when {
                // Only deploy to production from main branch
                branch 'main'
            }
            steps {
                script {
                    // Add your production deployment steps here
                    echo 'Deploying to production environment...'
                    // Example: Deploy to production server or container registry
                    
                    // Example: Restart the Flask application
                    sh 'pkill -f "python app.py" || true'
                    sh 'nohup python app.py > app.log 2>&1 &'
                }
            }
        }
    }
    
    post {
        always {
            // Clean up workspace after build
            cleanWs()
            
            // Send notification about build status
            script {
                def subject = "${currentBuild.currentResult}: Job '${env.JOB_NAME} [${env.BUILD_NUMBER}]'"
                def details = "${currentBuild.currentResult}: Job '${env.JOB_NAME} [${env.BUILD_NUMBER}]'\n" +
                             "Check console output at ${env.BUILD_URL}console"
                
                // Send email notification
                emailext (
                    subject: subject,
                    body: details,
                    to: 'aachsaya@gmail.com',
                    from: 'jenkins@yourdomain.com'
                )
            }
        }
    }
}
