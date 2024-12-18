pipeline {
    agent any
    stages {
        stage('Clone Repository') {
            steps {
                git branch: 'main', url: '605134428434.dkr.ecr.us-east-1.amazonaws.com/ecr-jenkins-repo'
            }
        }
        stage('Build Docker Image') {
            steps {
                sh 'docker build -t iris-predictor .'
            }
        }
        stage('Test Docker Container') {
            steps {
                sh 'docker run -d -p 5000:5000 iris-predictor'
                sh 'curl -X POST -H "Content-Type: application/json" -d \'{"sepal_length": 5.1, "sepal_width": 3.5, "petal_length": 1.4, "petal_width": 0.2}\' http://localhost:5000/predict'
            }
        }
        stage('Push to ECR') {
            steps {
                sh '''
                aws ecr get-login-password --region us-east-1 | docker login --username AWS --password-stdin 605134428434.dkr.ecr.us-east-1.amazonaws.com
                docker tag iris-predictor:latest 605134428434.dkr.ecr.us-east-1.amazonaws.com/iris-predictor
                docker push 605134428434.dkr.ecr.us-east-1.amazonaws.com/iris-predictor
                '''
            }
        }
    }
}
