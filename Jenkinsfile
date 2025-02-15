pipeline {
    agent any  // Runs on any available agent

    environment {
        PATH = "$PATH:/var/lib/jenkins/.local/bin"
        DOCKER_IMAGE = 'ghcr.io/Onyesi-john/yolo-app:latest'  // Update with your repo
        MODEL_PATH = '/home/john/runs/detect/train3/weights/best.pt'  // Path to trained model
    }

    stages {
        stage('Clone Repository') {
            steps {
                git branch: 'stage', url: 'https://github.com/Onyesi-john/waste_detection.git'  // Change repo URL
            }
        }

        stage('Install Dependencies') {
            steps {
                sh 'pip install -r requirements.txt'
            }
        }

        stage('Ensure Model Exists') {
            steps {
                script {
                    if (!fileExists(MODEL_PATH)) {
                        error "Model file not found at ${MODEL_PATH}. Make sure training is complete!"
                    }
                    sh "cp ${MODEL_PATH} ./best.pt"  // Copy model to project directory
                }
            }
        }

        stage('Build Docker Image') {
            steps {
                sh 'docker build -t $DOCKER_IMAGE .'
            }
        }

        stage('Push to GitHub Container Registry') {
            steps {
                withCredentials([string(credentialsId: 'ghcr-token', variable: 'GITHUB_TOKEN')]) {
                    sh 'echo $GITHUB_TOKEN | docker login ghcr.io -u Onyesi-john --password-stdin'
                    sh 'docker push $DOCKER_IMAGE'
                }
            }
        }

        stage('Deploy Container') {
            steps {
                sh 'docker run -d -p 5000:5000 --name yolo-app $DOCKER_IMAGE'
            }
        }
    }
}
