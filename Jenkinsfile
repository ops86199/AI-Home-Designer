pipeline {
    agent any
    stages {
        stage ('checkout code') {
            steps{
                git url: 'https://github.com/ops86199/AI-Home-Designer.git', branch: 'main'
            }
        }

        stage('docker image build') {
            steps {
                sh 'docker rmi ai-home-designer:latest || true'
                sh 'docker build -t ai-home-designer:latest .'
            }
        }
        stage('docker image push') {
            steps {
                withCredentials([usernamePassword(credentialsId: 'dockerhubc', usernameVariable: 'DOCKERHUB_USERNAME', passwordVariable: 'DOCKERHUB_PASSWORD')]) {
                    sh 'echo $DOCKERHUB_PASSWORD | docker login -u $DOCKERHUB_USERNAME --password-stdin'
                    sh 'docker tag ai-home-designer:latest $DOCKERHUB_USERNAME/ai-home-designer:latest'
                    sh 'docker push $DOCKERHUB_USERNAME/ai-home-designer:latest'
                }
            }
        }
        stage('run container') {
            steps {
                 sh '''
                 docker rm -f con3 || true 
                 docker run --name con2 -d -p 5000:5000 ops86199/ai-home-designe:latest
                 '''
            }
        }
        // stage('deploy to k8s cluster') {
        //     steps {
        //         withKubeConfig([credentialsId: 'kubeconfig-credentials-id']) {
        //             sh 'kubectl apply -f k8s/deployment.yaml'
        //             sh 'kubectl apply -f k8s/service.yaml'
        //         }
        //     }
        // }
    }  
}
