pipeline {
    agent any

    environment {
        DOCKER_IMAGE = 'latest'
        DOCKERHUB_USERNAME = 'oyinc'  // Replace with your DockerHub username
        DOCKERHUB_REPO = 'waste_detection'
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
                        python train.py || echo "Skipping training if already trained."

                        if [ -d "yolov5/runs/train" ]; then
                            MODEL_DIR=$(ls -td yolov5/runs/train/exp* 2>/dev/null | head -1)
                            if [ -n "$MODEL_DIR" ]; then
                                echo "Latest Model Directory: $MODEL_DIR"
                                cp $MODEL_DIR/weights/best.pt ./best.pt || { echo "Error: best.pt not found!"; exit 1; }
                            else
                                echo "Error: No training directory found!"
                                exit 1
                            fi
                        else
                            echo "Error: yolov5/runs/train directory does not exist!"
                            exit 1
                        fi

                        ls -lh ./best.pt
                    '''
                }
            }
        }

        stage('Setup Docker Buildx') {
            steps {
                script {
                    sh '''
                        docker run --rm --privileged multiarch/qemu-user-static --reset -p yes
                        docker buildx create --name mybuilder --use
                        docker buildx inspect --bootstrap
                    '''
                }
            }
        }

        stage('Build Docker Image with Buildx') {
            steps {
                script {
                    sh '''
                        if [ ! -f "./best.pt" ]; then
                            echo "Error: best.pt not found, training might have failed!"
                            exit 1
                        fi

                        docker buildx build --platform linux/arm/v7,linux/amd64 \
                        -t ${DOCKERHUB_USERNAME}/${DOCKERHUB_REPO}:${DOCKER_IMAGE} \
                        --push .
                    '''
                }
            }
        }

        stage('Push to Docker Hub') {
            steps {
                withCredentials([string(credentialsId: 'dockerhub-token', variable: 'DOCKERHUB_TOKEN')]) {
                    sh '''
                        echo $DOCKERHUB_TOKEN | docker login -u $DOCKERHUB_USERNAME --password-stdin
                        docker push ${DOCKERHUB_USERNAME}/${DOCKERHUB_REPO}:${DOCKER_IMAGE}
                    '''
                }
            }
        }

        stage('Deploy Container') {
            steps {
                sh '''
                    docker stop yolo-app || true
                    docker rm yolo-app || true
                    docker pull ${DOCKERHUB_USERNAME}/${DOCKERHUB_REPO}:${DOCKER_IMAGE}
                    docker run -d -p 5000:5000 --name yolo-app ${DOCKERHUB_USERNAME}/${DOCKERHUB_REPO}:${DOCKER_IMAGE}
                '''
            }
        }
    }
}
