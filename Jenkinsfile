pipeline {
    agent any
    triggers {
        cron('30 3,9,15 * * *')
    }
    environment {
        PATH = "/Users/narotamkumarmishra/.nvm/versions/node/v22.20.0/bin:${env.PATH}"
        NAUKRI_USERNAME = credentials('NAUKRI_EMAIL')      // ← credential ID from Jenkins
        NAUKRI_PASSWORD = credentials('NAUKRI_PASSWORD')   // ← credential ID from Jenkins
    }
    stages {
        stage('Checkout') {
            steps {
                checkout scm
            }
        }
        stage('Install Dependencies') {
            steps {
                sh 'npm install'
            }
        }
        stage('Upload Resume') {
            steps {
                sh 'node NaukriResumeScript.js'
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