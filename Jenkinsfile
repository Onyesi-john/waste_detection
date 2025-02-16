pipeline {
    agent any

    environment {
    DOCKER_IMAGE = 'latest'
    GITHUB_REGISTRY = 'ghcr.io'  // GitHub Container Registry
    GITHUB_REPO = 'onyesi-john/waste_detection'  // Replace with your actual GitHub repository name
   }


    stages {
        stage('Clone Repository') {
            steps {
               git branch: 'stage', url: 'https://github.com/Onyesi-john/waste_detection.git'
            }
        }

        stage('Set Up Python Environment') {
            steps {
                script {
                    // Set up the virtual environment and install dependencies
                    sh '''
                        python3 -m venv venv
                        . venv/bin/activate
                        pip install --upgrade pip
                        pip install -r requirements.txt 
                    '''
                }
            }
        }

        stage('Train Model') {
          steps {
            script {
               sh '''
                # Activate virtual environment and train model
                 source venv/bin/activate
                p   ython train.py

                # Ensure the app directory exists
                    mkdir -p ./app

                # Get the latest trained model directory
                    MODEL_DIR=$(ls -td runs/detect/train* | head -1)
                echo "Latest Model Directory: $MODEL_DIR"

                # Copy best.pt to the project root
                    cp $MODEL_DIR/weights/best.pt ./best.pt

                # Verify if best.pt exists
                 ls -lh ./best.pt
                '''
            }
        }
    }
        stage('Build Docker Image') {
             steps {
                  script {
                           // Authenticate to GitHub Container Registry using Jenkins credentials
                          withDockerRegistry([credentialsId: 'new_pipeline', url: "https://${GITHUB_REGISTRY}"]) {
                          // Build the Docker image with the correct tag format
                       sh 'docker build -t ${GITHUB_REGISTRY}/${GITHUB_REPO}:${DOCKER_IMAGE} .'
                  }
              }
           }
       }

        stage('Push to GitHub Container Registry') {
            steps {
                withCredentials([string(credentialsId: 'ghcr-token', variable: 'GITHUB_TOKEN')]) {
                sh '''
                    source .venv/bin/activate
                    echo $GITHUB_TOKEN | docker login ghcr.io -u Onyesi-john --password-stdin
                    docker push ghcr.io/onyesi-john/waste_detection:latest
                '''
                }
            }
        }

        stage('Deploy Container') {
            steps {
                sh '''
                source .venv/bin/activate
                docker pull ghcr.io/onyesi-john/waste_detection:latest
                docker run -d -p 5000:5000 --name yolo-app ghcr.io/onyesi-john/waste_detection:latest
            '''
            }
        }

    }
}
