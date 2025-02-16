pipeline {
    agent any

    environment {
        DOCKER_IMAGE = 'latest'
        GITHUB_REGISTRY = 'ghcr.io'
        GITHUB_REPO = 'onyesi-john/waste_detection'
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
                    sh '''#!/bin/bash
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
                    sh '''#!/bin/bash
                        . venv/bin/activate
                        python train.py

                        if [ -d "runs/detect" ]; then
                            MODEL_DIR=$(ls -td runs/detect/train* 2>/dev/null | head -1)
                            if [ -n "$MODEL_DIR" ]; then
                                echo "Latest Model Directory: $MODEL_DIR"
                                cp $MODEL_DIR/weights/best.pt ./best.pt || { echo "Error: best.pt not found!"; exit 1; }
                            else
                                echo "Error: No training directory found!"
                                exit 1
                            fi
                        else
                            echo "Error: runs/detect directory does not exist!"
                            exit 1
                        fi

                        ls -lh ./best.pt
                    '''
                }
            }
        }

        stage('Build Docker Image') {
            steps {
                script {
                    sh '''
                        if [ ! -f "./best.pt" ]; then
                            echo "Error: best.pt not found, training might have failed!"
                            exit 1
                        fi
                        docker build -t ${GITHUB_REGISTRY}/${GITHUB_REPO}:${DOCKER_IMAGE} .
                    '''
                }
            }
        }

        stage('Push to GitHub Container Registry') {
            steps {
                withCredentials([string(credentialsId: 'ghcr-token', variable: 'GITHUB_TOKEN')]) {
                    sh '''
                        . venv/bin/activate
                        echo $GITHUB_TOKEN | docker login ghcr.io -u Onyesi-john --password-stdin
                        docker push ghcr.io/onyesi-john/waste_detection:latest
                    '''
                }
            }
        }

        stage('Deploy Container') {
            steps {
                sh '''
                    . venv/bin/activate
                    docker stop yolo-app || true
                    docker rm yolo-app || true
                    docker pull ghcr.io/onyesi-john/waste_detection:latest
                    docker run -d -p 5000:5000 --name yolo-app ghcr.io/onyesi-john/waste_detection:latest
                '''
            }
        }
    }
}
