pipeline {
    agent any

    environment {
        DOCKER_REGISTRY      = 'docker.io'
        DOCKER_USERNAME      = 'leogrv22'
        VERSION              = "${env.BUILD_NUMBER}"
        HELM_PIPELINE_JOB    = 'helm-deploy'
        KUBERNETES_NAMESPACE = 'dev'
        AWS_REGION           = 'eu-west-3'
    }

    stages {
        stage('Checkout') {
            steps {
                echo "Checking out code from ${env.GIT_URL}"
                checkout scm
            }
        }

    stage('Unit Tests') {
        steps {
            echo "Running unit tests in Python container (COPY mode, no bind mount)..."
            sh '''
                set -e

                run_tests() {
                    svc="$1"
                    echo "---- Tests for $svc ----"

                    if [ ! -d "Microservices/$svc/tests" ]; then
                    echo "No tests folder for $svc -> skip"
                    return 0
                    fi

                    cid=$(docker create python:3.12-slim bash -lc '
                    set -e
                    cd /app
                    python -m pip install -U pip >/dev/null
                    pip install -r requirements.txt >/dev/null
                    export PYTHONPATH=/app
                    pytest -q
                    ')

                    # Copy service code into container
                    docker cp "Microservices/$svc/." "$cid:/app"

                    # Run tests
                    docker start -a "$cid"

                    # Cleanup
                    docker rm -f "$cid" >/dev/null
                }

                run_tests auth
                # run_tests users
                # run_tests items
                # run_tests gateway
                '''
            }
        }

        stage('Build Docker Images') {
            steps {
                echo "Building Docker images for all microservices..."

                sh """
                    set -e

                    cd Microservices/auth
                    docker build -t ${DOCKER_USERNAME}/auth:${VERSION} .
                    docker tag ${DOCKER_USERNAME}/auth:${VERSION} ${DOCKER_USERNAME}/auth:latest
                    docker tag ${DOCKER_USERNAME}/auth:${VERSION} ${DOCKER_USERNAME}/auth:dev
                """

                sh """
                    set -e

                    cd Microservices/users
                    docker build -t ${DOCKER_USERNAME}/users:${VERSION} .
                    docker tag ${DOCKER_USERNAME}/users:${VERSION} ${DOCKER_USERNAME}/users:latest
                    docker tag ${DOCKER_USERNAME}/users:${VERSION} ${DOCKER_USERNAME}/users:dev
                """

                sh """
                    set -e

                    cd Microservices/items
                    docker build -t ${DOCKER_USERNAME}/items:${VERSION} .
                    docker tag ${DOCKER_USERNAME}/items:${VERSION} ${DOCKER_USERNAME}/items:latest
                    docker tag ${DOCKER_USERNAME}/items:${VERSION} ${DOCKER_USERNAME}/items:dev
                """

                sh """
                    set -e

                    cd Microservices/gateway
                    docker build -t ${DOCKER_USERNAME}/gateway:${VERSION} .
                    docker tag ${DOCKER_USERNAME}/gateway:${VERSION} ${DOCKER_USERNAME}/gateway:latest
                    docker tag ${DOCKER_USERNAME}/gateway:${VERSION} ${DOCKER_USERNAME}/gateway:dev
                """
            }
        }

        stage('Security Scan') {
            steps {
                script {
                    echo "Running Trivy security scan on Docker images..."

                    sh '''
                        docker run --rm \
                            -v /var/run/docker.sock:/var/run/docker.sock \
                            aquasec/trivy:latest image \
                            --severity HIGH,CRITICAL \
                            --no-progress \
                            --exit-code 0 \
                            leogrv22/auth:${VERSION}

                        docker run --rm \
                            -v /var/run/docker.sock:/var/run/docker.sock \
                            aquasec/trivy:latest image \
                            --severity HIGH,CRITICAL \
                            --no-progress \
                            --exit-code 0 \
                            leogrv22/users:${VERSION}

                        docker run --rm \
                            -v /var/run/docker.sock:/var/run/docker.sock \
                            aquasec/trivy:latest image \
                            --severity HIGH,CRITICAL \
                            --no-progress \
                            --exit-code 0 \
                            leogrv22/items:${VERSION}

                        docker run --rm \
                            -v /var/run/docker.sock:/var/run/docker.sock \
                            aquasec/trivy:latest image \
                            --severity HIGH,CRITICAL \
                            --no-progress \
                            --exit-code 0 \
                            leogrv22/gateway:${VERSION}
                        '''
                }
            }
        }

        stage('Push to Docker Hub') {
            steps {
                echo "Pushing images to Docker Hub..."
                withCredentials([usernamePassword(credentialsId: 'dockerhub-credentials', usernameVariable: 'DOCKER_USER', passwordVariable: 'DOCKER_PASS')]) {
                    sh '''
                        set -e
                        echo "$DOCKER_PASS" | docker login -u "$DOCKER_USER" --password-stdin

                        docker push leogrv22/auth:'"$VERSION"'
                        docker push leogrv22/auth:latest
                        docker push leogrv22/auth:dev

                        docker push leogrv22/users:'"$VERSION"'
                        docker push leogrv22/users:latest
                        docker push leogrv22/users:dev

                        docker push leogrv22/items:'"$VERSION"'
                        docker push leogrv22/items:latest
                        docker push leogrv22/items:dev

                        docker push leogrv22/gateway:'"$VERSION"'
                        docker push leogrv22/gateway:latest
                        docker push leogrv22/gateway:dev
                    '''
                }
            }
        }

        stage('Trigger Helm Deployment') {
            steps {
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