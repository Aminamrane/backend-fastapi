pipeline {
    agent any
    
    environment {
        DOCKER_REGISTRY = 'docker.io'
        DOCKER_USERNAME = 'leogrv22'
        IMAGE_NAME = 'fastapi-backend'
        VERSION = "${env.BUILD_NUMBER}"
        HELM_PIPELINE_JOB = 'helm-deploy'
        KUBERNETES_NAMESPACE = 'dev'
        AWS_REGION = 'eu-west-3'
    }
    
    stages {
        stage('Checkout') {
            steps {
                script {
                    echo "Checking out code from ${env.GIT_URL}"
                    checkout scm
                }
            }
        }
        
        stage('Tests') {
            steps {
                script {
                    echo "Running unit tests..."
                    sh '''
                        # Install dependencies for each microservice
                        cd Microservices/auth && pip install -r requirements.txt || true
                        cd ../users && pip install -r requirements.txt || true
                        cd ../items && pip install -r requirements.txt || true
                        cd ../gateway && pip install -r requirements.txt || true
                        
                        # Run tests if they exist (placeholder for now)
                        echo "Tests completed (no test files found yet)"
                    '''
                }
            }
        }
        
        stage('Build Docker Images') {
            steps {
                script {
                    echo "Building Docker images for all microservices..."
                    
                    // Build Auth service
                    sh """
                        cd Microservices/auth
                        docker build -t ${DOCKER_USERNAME}/auth:${VERSION} .
                        docker tag ${DOCKER_USERNAME}/auth:${VERSION} ${DOCKER_USERNAME}/auth:latest
                    """
                    
                    // Build Users service
                    sh """
                        cd Microservices/users
                        docker build -t ${DOCKER_USERNAME}/users:${VERSION} .
                        docker tag ${DOCKER_USERNAME}/users:${VERSION} ${DOCKER_USERNAME}/users:latest
                    """
                    
                    // Build Items service
                    sh """
                        cd Microservices/items
                        docker build -t ${DOCKER_USERNAME}/items:${VERSION} .
                        docker tag ${DOCKER_USERNAME}/items:${VERSION} ${DOCKER_USERNAME}/items:latest
                    """
                    
                    // Build Gateway service
                    sh """
                        cd Microservices/gateway
                        docker build -t ${DOCKER_USERNAME}/gateway:${VERSION} .
                        docker tag ${DOCKER_USERNAME}/gateway:${VERSION} ${DOCKER_USERNAME}/gateway:latest
                    """
                }
            }
        }
        
        stage('Push to Docker Hub') {
            steps {
                script {
                    withCredentials([usernamePassword(credentialsId: 'dockerhub-credentials', usernameVariable: 'DOCKER_USER', passwordVariable: 'DOCKER_PASS')]) {
                        sh """
                            echo ${DOCKER_PASS} | docker login -u ${DOCKER_USER} --password-stdin ${DOCKER_REGISTRY}
                            
                            docker push ${DOCKER_USERNAME}/auth:${VERSION}
                            docker push ${DOCKER_USERNAME}/auth:latest
                            
                            docker push ${DOCKER_USERNAME}/users:${VERSION}
                            docker push ${DOCKER_USERNAME}/users:latest
                            
                            docker push ${DOCKER_USERNAME}/items:${VERSION}
                            docker push ${DOCKER_USERNAME}/items:latest
                            
                            docker push ${DOCKER_USERNAME}/gateway:${VERSION}
                            docker push ${DOCKER_USERNAME}/gateway:latest
                        """
                    }
                }
            }
        }
        
        stage('Trigger Helm Deployment') {
            steps {
                script {
                    echo "Triggering Helm pipeline to deploy backend services..."
                    build job: "${HELM_PIPELINE_JOB}", 
                          parameters: [
                              string(name: 'SERVICE', value: 'backend'),
                              string(name: 'IMAGE_VERSION', value: "${VERSION}"),
                              string(name: 'NAMESPACE', value: "${KUBERNETES_NAMESPACE}")
                          ],
                          wait: false
                }
            }
        }
    }
    
    post {
        success {
            echo "✅ Backend pipeline completed successfully!"
            echo "Images pushed: ${DOCKER_USERNAME}/auth:${VERSION}, ${DOCKER_USERNAME}/users:${VERSION}, ${DOCKER_USERNAME}/items:${VERSION}, ${DOCKER_USERNAME}/gateway:${VERSION}"
        }
        failure {
            echo "❌ Backend pipeline failed!"
        }
        always {
            cleanWs()
        }
    }
}

