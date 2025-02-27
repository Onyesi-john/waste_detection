pipeline {
    agent any

    environment {
        DOCKER_IMAGE = 'latest'
        DOCKERHUB_USERNAME = 'your-dockerhub-username'  // Replace with your DockerHub username
        DOCKERHUB_REPO = 'waste_detection'
    }

    stages {
        stage('Setup Docker Buildx') {
            steps {
                script {
                    sh '''
                        docker buildx create --use || true
                        docker buildx inspect --bootstrap || true
                    '''
                }
            }
        }

        stage('Build and Push Docker Image for Raspberry Pi') {
            steps {
                script {
                    sh '''
                        docker buildx build --platform linux/arm/v7,linux/arm64,linux/amd64 \
                        -t ${DOCKERHUB_USERNAME}/${DOCKERHUB_REPO}:${DOCKER_IMAGE} \
                        --push .
                    '''
                }
            }
        }
    }
}
