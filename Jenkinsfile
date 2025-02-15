pipeline {
    agent any  // Runs on any available agent

    environment {
        
        PATH = "$PATH:/var/lib/jenkins/.local/bin"
        DOCKER_IMAGE = 'ghcr.io/Onyesi-john/yolo-app:latest'  // Update with your repo
        MODEL_PATH = '/home/john/runs/detect/train3/weights/best.pt'  // Path to the model inside the project
        VENV_DIR = '.venv'  // Path to your virtual environment (update if needed)
    }

    stages {
        stage('Clone Repository') {
            steps {
                git branch: 'stage', url: 'https://github.com/Onyesi-john/waste_detection.git'  // Change repo URL
            }
        }

        stage('Set Up Virtual Environment') {
            steps {
                script {
                    // Check if virtual environment exists, if not, create it
                    if (!fileExists("${VENV_DIR}/bin/activate")) {
                        sh 'python3 -m venv .venv'
                    }
                    // Activate the virtual environment
                    sh 'source .venv/bin/activate'
                }
            }
        }

        stage('Install Dependencies') {
            steps {
                // Ensure we are in the virtual environment before installing dependencies
                sh '''
                    source .venv/bin/activate
                    pip install -r requirements.txt
                '''
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
                sh '''
                    source .venv/bin/activate
                    docker build -t $DOCKER_IMAGE .
                '''
            }
        }

        stage('Push to GitHub Container Registry') {
            steps {
                withCredentials([string(credentialsId: 'ghcr-token', variable: 'GITHUB_TOKEN')]) {
                    sh '''
                        source .venv/bin/activate
                        echo $GITHUB_TOKEN | docker login ghcr.io -u Onyesi-john --password-stdin
                        docker push $DOCKER_IMAGE
                    '''
                }
            }
        }

        stage('Deploy Container') {
            steps {
                sh '''
                    source .venv/bin/activate
                    docker run -d -p 5000:5000 --name yolo-app $DOCKER_IMAGE
                '''
            }
        }
    }
}
