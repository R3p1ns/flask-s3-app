pipeline {
    agent any

    environment {
        DOCKER_HUB_REPO = "hieupro7410/flask-s3-app"
        DOCKER_IMAGE = "${DOCKER_HUB_REPO}:${env.BUILD_NUMBER}"
        AWS_REGION = "ap-southeast-1"
        EKS_CLUSTER_NAME = "lan-dau"
    }

    stages {
        // Stage 1: Checkout code từ Git
        stage('Checkout') {
            steps {
                git branch: 'main', url: 'https://github.com/R3p1ns/flask-s3-app.git'
            }
        }


        // Stage 3: Build Docker Image
        stage('Build Docker Image') {
            steps {
                script {
                    docker.build(DOCKER_IMAGE)
                }
            }
        }

        // Stage 4: Push Image lên Docker Hub
        stage('Push to Docker Hub') {
            steps {
                script {
                    withCredentials([[
                        $class: 'UsernamePasswordMultiBinding',
                        credentialsId: 'docker-hub-cred',
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

        // Stage 5: Deploy lên Kubernetes
        stage('Deploy to EKS') {
    steps {
        script {
            withCredentials([
                string(credentialsId: 'AWS_ACCESS_KEY_ID', variable: 'AWS_ACCESS_KEY_ID'),
                string(credentialsId: 'AWS_SECRET_ACCESS_KEY', variable: 'AWS_SECRET_ACCESS_KEY')
            ]) {
                sh """
                # Cấu hình AWS CLI
                aws configure set aws_access_key_id ${AWS_ACCESS_KEY_ID}
                aws configure set aws_secret_access_key ${AWS_SECRET_ACCESS_KEY}
                aws configure set region ${AWS_REGION}

                # Cập nhật kubeconfig với đầy đủ quyền
                aws eks --region ${AWS_REGION} update-kubeconfig --name ${EKS_CLUSTER_NAME}

                # Kiểm tra kết nối
                kubectl get nodes

                # Triển khai ứng dụng
                sed -i 's|<DOCKER_IMAGE>|${DOCKER_IMAGE}:${DOCKER_TAG}|g' k8s/deployment.yaml
                kubectl apply -f depoyment.yaml
                kubectl rollout status deployment/flask-s3-app --timeout=2m
                """
            }
        }
    }
}
    }
}