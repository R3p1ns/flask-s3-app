pipeline {
    agent any

    environment {
        DOCKER_HUB_REPO = "hieupro7410/flask-s3-app"
        DOCKER_IMAGE = "${DOCKER_HUB_REPO}:${env.BUILD_NUMBER}"
        AWS_REGION = "ap-southeast-1"
        EKS_CLUSTER_NAME = "lan-dau"
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
            # Kiểm tra image
            docker pull ${DOCKER_IMAGE} || true
            
            # Cập nhật image trong deployment (sử dụng delimiter khác thay vì |)
            sed -i 's#<DOCKER_IMAGE>#${DOCKER_IMAGE}#g' deployment.yaml
            
            # Thêm imagePullSecrets (sử dụng delimiter @ để tránh xung đột với /)
            sed -i 's@imagePullSecrets:.*@imagePullSecrets:\\n      - name: docker-hub-creds@' deployment.yaml
            
            # Áp dụng cấu hình
            kubectl apply -f deployment.yaml --validate=false
            kubectl apply -f service.yaml
            kubectl apply -f ingress.yaml
            
            # Kiểm tra trạng thái
            kubectl rollout status deployment/flask-s3-app --timeout=2m || \\
            (kubectl describe pod -l app=flask-s3-app && exit 1)
        """
    }
}
    }
}