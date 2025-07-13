pipeline {
    agent any

    environment {
        DOCKER_HUB_REPO = "hieupro7410/flask-s3-app"
        DOCKER_IMAGE = "${DOCKER_HUB_REPO}:${env.BUILD_NUMBER}"  // Sử dụng BUILD_NUMBER làm tag
        AWS_REGION = "ap-southeast-1"
        EKS_CLUSTER_NAME = "lan-dau"
        K8S_DIR = "k8s"  // Thư mục chứa file k8s
    }

    stages {
        stage('Checkout') {
            steps {
                git branch: 'main', url: 'https://github.com/R3p1ns/flask-s3-app.git'
            }
        }

        stage('Configure AWS EKS') {
            steps {
                withCredentials([
                    string(credentialsId: 'AWS_ACCESS_KEY_ID', variable: 'AWS_ACCESS_KEY_ID'),
                    string(credentialsId: 'AWS_SECRET_ACCESS_KEY', variable: 'AWS_SECRET_ACCESS_KEY')
                ]) {
                    sh """
                        aws configure set aws_access_key_id ${AWS_ACCESS_KEY_ID}
                        aws configure set aws_secret_access_key ${AWS_SECRET_ACCESS_KEY}
                        aws configure set region ${AWS_REGION}
                        aws eks update-kubeconfig --name ${EKS_CLUSTER_NAME} --region ${AWS_REGION}
                        kubectl get nodes
                    """
                }
            }
        }

        stage('Build Docker Image') {
            steps {
                script {
                    docker.build(DOCKER_IMAGE)
                }
            }
        }

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

        stage('Deploy to EKS') {
            steps {
                sh """
                    # Cập nhật image trong deployment
                    sed -i 's|<DOCKER_IMAGE>|${DOCKER_IMAGE}|g' ${K8S_DIR}/deployment.yaml
                    
                    # Áp dụng cấu hình Kubernetes
                    kubectl apply -f ${K8S_DIR}/deployment.yaml
                    kubectl apply -f ${K8S_DIR}/service.yaml
                    kubectl rollout status deployment/flask-s3-app --timeout=2m
                    kubectl get pods
                """
            }
        }
    }
}