import os


def install_and_delete_minikube():
    try:
        os.system("minikube delete")
    except:
        print("Minikube not deleted, but might okay, as it is the frist time running this...")
    os.system("minikube start --memory 4098 --cpus 3")

def execute_command_inside_minikube(command):
    os.system("minikube ssh \"" + command + "\"")

def prepare_docker_container_with_spark(spark_url):
    execute_command_inside_minikube("wget "+ spark_url)
    execute_command_inside_minikube("sudo mkdir -p /usr/local/")
    execute_command_inside_minikube("sudo zcat spark-2.3.1-bin-hadoop2.7.tgz | tar -xvf - ")
    execute_command_inside_minikube("sudo mv spark-2.3.1-bin-hadoop2.7 /usr/local/spark")
    execute_command_inside_minikube("cd /usr/local/spark && sudo ./bin/docker-image-tool.sh build")

def deploy_on_kubernetes():
    print("TBD")


install_and_delete_minikube()
prepare_docker_container_with_spark("http://ftp-stud.hs-esslingen.de/pub/Mirrors/ftp.apache.org/dist/spark/spark-2.3.1/spark-2.3.1-bin-hadoop2.7.tgz")