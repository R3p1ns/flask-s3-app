pipeline {
    agent any

    environment {
        DOCKER_HUB_REPO = "/flask-s3-app"  // Thay bằng username Docker Hub của bạn
        DOCKER_IMAGE = "${DOCKER_HUB_REPO}:${env.BUILD_NUMBER}"
    }

    stages {
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
                        credentialsId: 'dockerhub-creds',  // Credentials ID lưu trong Jenkins
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
                    # Thay thế image trong file deployment.yaml
                    sed -i 's|image:.*|image: ${DOCKER_IMAGE}|g' deployment.yaml
                    
                    # Áp dụng cấu hình Kubernetes
                    kubectl ${KUBE_CONFIG} apply -f deployment.yaml
                    kubectl ${KUBE_CONFIG} apply -f service.yaml
                    kubectl ${KUBE_CONFIG} apply -f ingress.yaml
                    
                    # Kiểm tra trạng thái
                    kubectl ${KUBE_CONFIG} get pods
                """
            }
        }
    }
}