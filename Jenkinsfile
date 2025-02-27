pipeline {
    agent any

    environment {
        DOCKER_IMAGE = 'latest'
        DOCKERHUB_USERNAME = 'your-dockerhub-username'  // Replace with your DockerHub username
        DOCKERHUB_REPO = 'waste_detection'
    }

    stages {
        stage('Clone Repository') {
            steps {
                git branch: 'stage', url: 'https://github.com/Onyesi-john/waste_detection.git'
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
