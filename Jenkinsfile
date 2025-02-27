pipeline {
    agent any

    environment {
        DOCKER_IMAGE = 'latest'
        DOCKERHUB_USERNAME = 'oyinc'
        DOCKERHUB_REPO = 'waste_detection'
    }

    stages {
        stage('Enable Buildx') {
            steps {
                script {
                    sh '''
                        export DOCKER_CLI_EXPERIMENTAL=enabled
                        docker buildx create --use || true
                        docker buildx inspect --bootstrap || true
                    '''
                }
            }
        }

        stage('Login to Docker Hub') {
            steps {
                withCredentials([string(credentialsId: 'docker-hub-password', variable: 'DOCKER_PASSWORD')]) {
                    sh '''
                        echo $DOCKER_PASSWORD | docker login -u ${DOCKERHUB_USERNAME} --password-stdin
                    '''
                }
            }
        }

        stage('Build & Push Multi-Arch Image') {
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
