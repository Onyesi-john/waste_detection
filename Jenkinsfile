pipeline {
    agent any

    environment {
        DOCKER_IMAGE = 'ghcr.io/Onyesi-john/waste_detection:latest'
        GDRIVE_FILE_ID = '1BV-HLBtKluSgiwpPbAxv6Zh1lCAsZ1XO'  // Replace with Google Drive File ID
    }

    stages {
        stage('Clone Repo') {
            steps {
                git branch: 'stage', url: 'https://github.com/Onyesi-john/waste_detection.git'
            }
        }
        stage('Set Up Python') {
            steps {
                sh 'python3 -m venv venv && source venv/bin/activate && pip install -r requirements.txt'
            }
        }

        stage('Download Dataset') {
            steps {
                sh 'python download_data.py'
            }
        }

        stage('Train Model') {
            steps {
                sh 'python train.py'
            }
        }

        stage('Docker Build & Push') {
            steps {
                withDockerRegistry([credentialsId: 'github-token', url: 'https://ghcr.io']) {
                    sh 'docker build -t ${DOCKER_IMAGE} .'
                    sh 'docker push ${DOCKER_IMAGE}'
                }
            }
        }

        stage('Deploy App') {
            steps {
                sh 'docker run -d -p 8000:8000 ${DOCKER_IMAGE}'
            }
        }
    }
}
