pipeline {
    agent any

    environment {
    DOCKER_IMAGE = 'latest'
    GITHUB_REGISTRY = 'ghcr.io'  // GitHub Container Registry
    GITHUB_REPO = 'onyesi-john/waste_detect'  // Replace with your actual GitHub repository name
   }


    stages {
        stage('Clone Repository') {
            steps {
               git branch: 'stage', url: 'https://github.com/Onyesi-john/mlops.git'
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
                    sh '''#!/bin/bash
                    source venv/bin/activate
                    python train.py
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
