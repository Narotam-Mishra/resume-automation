pipeline {
    agent any
    triggers {
        cron('30 3,9,15 * * *')
    }
    environment {
        PATH = "/Users/narotamkumarmishra/.nvm/versions/node/v22.20.0/bin:${env.PATH}"
    }
    stages {
        stage('Checkout') {
            steps {
                git branch: 'main',
                    url: 'https://github.com/Narotam-Mishra/resume-automation.git',
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
