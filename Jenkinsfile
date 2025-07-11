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
                        
                        // Run flake8 for code style checking - EXCLUDE venv directory
                        sh "${VENV_ACTIVATE} && flake8 . --exclude=venv --count --select=E9,F63,F7,F82 --show-source --statistics"
                        sh "${VENV_ACTIVATE} && flake8 . --exclude=venv --count --max-complexity=10 --max-line-length=127 --statistics"
                        
                        // Run black for code formatting - EXCLUDE venv directory
                        sh "${VENV_ACTIVATE} && black --check --diff --exclude=venv ."
                    } else {
                        bat "${VENV_ACTIVATE} && python -m pip install flake8 black"
                        
                        // Run flake8 for code style checking using Python module syntax - EXCLUDE venv directory
                        bat "${VENV_ACTIVATE} && python -m flake8 . --exclude=venv --count --select=E9,F63,F7,F82 --show-source --statistics"
                        bat "${VENV_ACTIVATE} && python -m flake8 . --exclude=venv --count --max-complexity=10 --max-line-length=127 --statistics"
                        
                        // Run black for code formatting - EXCLUDE venv directory
                        bat "${VENV_ACTIVATE} && python -m black --check --diff --exclude=venv ."
                    }
                }
            }
            post {
                failure {
                    echo 'Linting failed, but continuing with other stages...'
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
                    
                    // Archive test results (only if test reports exist)
                    script {
                        if (fileExists('**/test-reports/*.xml')) {
                            junit '**/test-reports/*.xml'
                        }
                    }
                    
                    // Publish coverage report (only if htmlcov directory exists)
                    script {
                        if (fileExists('htmlcov/index.html')) {
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
            }
            post {
                failure {
                    echo 'Tests failed, but continuing with other stages...'
                }
            }
        }
        
        stage('Security Scan') {
            steps {
                script {
                    // Run bandit for security scanning
                    if (isUnix()) {
                        sh "${VENV_ACTIVATE} && pip install bandit"
                        sh "${VENV_ACTIVATE} && bandit -r . -f html -o bandit_report.html --exclude=venv || true"
                    } else {
                        bat "${VENV_ACTIVATE} && python -m pip install bandit"
                        bat "${VENV_ACTIVATE} && bandit -r . -f html -o bandit_report.html --exclude=venv || true"
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
                    if (isUnix()) {
                        sh 'mkdir -p build'
                        // Example: Copy required files to build directory
                        sh 'cp -r app.py requirements.txt build/ || true'
                        // Copy templates if they exist
                        sh 'cp -r templates/ build/ || true'
                    } else {
                        bat 'if not exist build mkdir build'
                        // Example: Copy required files to build directory
                        bat 'copy app.py build\\ || echo "app.py not found"'
                        bat 'copy requirements.txt build\\ || echo "requirements.txt not found"'
                        // Copy templates if they exist
                        bat 'xcopy templates build\\templates\\ /E /I || echo "templates directory not found"'
                    }
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
                    if (isUnix()) {
                        sh 'pkill -f "python app.py" || true'
                        sh 'nohup python app.py > app.log 2>&1 &'
                    } else {
                        bat 'taskkill /F /IM python.exe || echo "No python processes found"'
                        bat 'start /B python app.py > app.log 2>&1'
                    }
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