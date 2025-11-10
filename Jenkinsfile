pipeline {
  agent any

  environment {
    IMAGE = "aceest-fitness:${env.BUILD_NUMBER}"
  }

  stages {
    stage('Checkout') {
      steps { checkout scm }
    }
    stage('Install & Test') {
      steps {
        sh 'python3 -m pip install --upgrade pip'
        sh 'pip install -r app/requirements.txt'
        sh 'pytest -q'
      }
    }
    stage('Build Docker Image') {
      steps {
        sh 'docker build -t ${IMAGE} .'
      }
    }
    stage('Docker Push (manual config)') {
      steps {
        echo "Configure Docker credentials in Jenkins and enable push here."
      }
    }
  }

  post {
    success {
      echo "Build succeeded"
    }
    failure {
      echo "Build failed"
    }
  }
}