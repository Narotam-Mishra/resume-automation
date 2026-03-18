pipeline {
    agent any

    triggers {
        cron('30 2,8,13 * * *')
    }

    environment {
        // Pull .env secrets from Jenkins Credentials (set up in Step 4)
        NAUKRI_EMAIL    = credentials('NAUKRI_EMAIL')
        NAUKRI_PASSWORD = credentials('NAUKRI_PASSWORD')
    }

    stages {
        stage('Checkout') {
            steps {
                // Jenkins auto-clones from the configured GitHub repo
                checkout scm
            }
        }

        stage('Install Dependencies') {
            steps {
                sh '''
                    pip3 install -r requirements.txt
                '''
            }
        }

        stage('Upload Resume') {
            steps {
                sh '''
                    python3 naukari_resume_automation.py
                '''
            }
        }
    }

    post {
        success {
            echo "✅ Resume uploaded at ${new Date()}"
        }
        failure {
            echo "❌ Upload failed at ${new Date()}"
        }
    }
}