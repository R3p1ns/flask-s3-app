pipeline {
    agent any

    environment {
        DOCKER_HUB_REPO = "hieupro7410/flask-s3-app"  // Thay bằng username Docker Hub của bạn
        DOCKER_IMAGE = "${DOCKER_HUB_REPO}:${env.BUILD_NUMBER}"
        AWS_REGION = "ap-southeast-1"
        EKS_CLUSTER_NAME = "lan-dau"
    }

    stages {
        stage('Configure EKS Access') {
        steps {
            sh """
                aws eks update-kubeconfig --name ${EKS_CLUSTER_NAME} --region ${AWS_REGION}
            """
        }
    }
        // Stage 1: Checkout code từ Git
        stage('Checkout') {
            steps {
                git branch: 'main', url: 'https://github.com/R3p1ns/flask-s3-app.git'
            }
        }

        // Stage 2: Build Docker Image
        stage('Build Docker Image') {
            steps {
                script {
                    docker.build(DOCKER_IMAGE)
                }
            }
        }

        // Stage 3: Push Image lên Docker Hub
        stage('Push to Docker Hub') {
            steps {
                script {
                    withCredentials([[
                        $class: 'UsernamePasswordMultiBinding',
                        credentialsId: 'docker-hub-cred',  // Credentials ID lưu trong Jenkins
                        usernameVariable: 'DOCKER_HUB_USER',
                        passwordVariable: 'DOCKER_HUB_PASS'
                    ]]) {
                        sh """
                            echo ${DOCKER_HUB_PASS} | docker login -u ${DOCKER_HUB_USER} --password-stdin
                            docker push ${DOCKER_IMAGE}
                        """
                    }
                }
            }
        }

        // Stage 4: Deploy lên Kubernetes
        stage('Deploy to Kubernetes') {
        steps {
            sh """
                
                kubectl apply -f deployment.yaml
                kubectl apply -f service.yaml
                kubectl apply -f ingress.yaml
                kubectl get pods
            """
            }
        }
    }
}