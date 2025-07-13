pipeline {
    agent any

    environment {
        DOCKER_HUB_REPO = "hieupro7410/flask-s3-app"
        DOCKER_IMAGE = "${DOCKER_HUB_REPO}:${env.BUILD_NUMBER}"
        AWS_REGION = "ap-southeast-1"
        EKS_CLUSTER_NAME = "lan-dau"
        K8S_DIR = "k8s"
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
                    [$class: 'AmazonWebServicesCredentialsBinding',
                     credentialsId: 'aws-creds',
                     accessKeyVariable: 'AWS_ACCESS_KEY_ID',
                     secretKeyVariable: 'AWS_SECRET_ACCESS_KEY']
                ]) {
                    sh '''
                        aws configure set aws_access_key_id $AWS_ACCESS_KEY_ID
                        aws configure set aws_secret_access_key $AWS_SECRET_ACCESS_KEY
                        aws configure set region ${AWS_REGION}
                        aws eks update-kubeconfig --name ${EKS_CLUSTER_NAME} --region ${AWS_REGION}
                        kubectl get nodes
                    '''
                }
            }
        }

        // Các stage khác giữ nguyên...
    }
}