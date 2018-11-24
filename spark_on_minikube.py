import os


def install_and_delete_minikube():
    try:
        os.system("minikube delete")
    except:
        print("Minikube not deleted, but might okay, as it is the frist time running this...")
    os.system("minikube start --memory 4098 --cpus 3")

def execute_command_inside_minikube(command):
    os.system("minikube ssh \"" + command + "\"")

def install_java_on_minikube():
    execute_command_inside_minikube("curl https://download.java.net/java/GA/jdk11/13/GPL/openjdk-11.0.1_linux-x64_bin.tar.gz --output java-11.tgz")
    execute_command_inside_minikube("sudo zcat java-11.tgz | tar -xvf - ")
    execute_command_inside_minikube("sudo mkdir -p /usr/local/")
    execute_command_inside_minikube("sudo mv jdk-11.0.1 /usr/local/java")
    execute_command_inside_minikube("echo \"export JAVA_HOME=/usr/local/java\" | sudo tee -a /etc/profile.d/java.sh")

def prepare_docker_container_with_spark(spark_url):
    execute_command_inside_minikube("wget "+ spark_url)
    execute_command_inside_minikube("sudo mkdir -p /usr/local/")
    execute_command_inside_minikube("sudo zcat spark-2.3.1-bin-hadoop2.7.tgz | tar -xvf - ")
    execute_command_inside_minikube("sudo mv spark-2.3.1-bin-hadoop2.7 /usr/local/spark")
    execute_command_inside_minikube("echo 'export PATH=$PATH:/usr/local/spark/bin' | sudo tee -a /etc/profile.d/spark.sh")
    execute_command_inside_minikube("cd /usr/local/spark && sudo ./bin/docker-image-tool.sh -t spark-docker build")
    execute_command_inside_minikube("docker run -d -p 5000:5000 --restart=always --name registry registry:2")
    execute_command_inside_minikube("docker tag spark:spark-docker localhost:5000/spark")
    execute_command_inside_minikube("docker push localhost:5000/spark")
    os.system("kubectl create serviceaccount spark")
    os.system("kubectl create clusterrolebinding spark-role --clusterrole=edit --serviceaccount=default:spark --namespace=default")

def run_spark_pi():
    os.system("$SPARK_HOME/bin/spark-submit --master k8s://https://$(minikube ip):8443 --deploy-mode cluster --name spark-pi --class org.apache.spark.examples.SparkPi --conf spark.executor.instances=3 --conf spark.kubernetes.container.image=localhost:5000/spark --conf spark.kubernetes.authenticate.driver.serviceAccountName=spark local:///opt/spark/examples/jars/spark-examples_2.11-2.3.1.jar")


install_and_delete_minikube()
prepare_docker_container_with_spark("http://ftp-stud.hs-esslingen.de/pub/Mirrors/ftp.apache.org/dist/spark/spark-2.3.1/spark-2.3.1-bin-hadoop2.7.tgz")
run_spark_pi()