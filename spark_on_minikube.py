import os


def install_and_delete_minikube():
    try:
        os.system("minikube delete")
    except:
        print("Minikube not deleted, but might okay, as it is the frist time running this...")
    os.system("minikube start --memory 4098 --cpus 3")


def prepare_docker_container_with_spark():
    print("TBD")


def deploy_on_kubernetes():
    print("TBD")


install_and_delete_minikube()
