from core.web_server.flask_wrapper import FlaskAppWrapper
from docker import APIClient, DockerClient
import os


class TwinHub:
    DOCKER_CLIENT_URI = 'unix://var/run/docker.sock'
    TWIN_DOCKER_SOURCES_DIR = os.path.join("asset", "twin-docker-sources")
    DOCKERFILE_PATH = "Dockerfile"
    DEFAULT_DOCKERFILE_ENCODING = "utf-8"
    NODE_IMAGE_TAG = "twin/dev"
    NETWORK_NAME = "twin_network"
    NODE_COUNTER = 0

    def __init__(self):
        self.__flask_app = FlaskAppWrapper(__name__)

    def start(self):
        self.__flask_app.add_endpoint(
            endpoint='/node/add',
            endpoint_name='add_node',
            handler=self.__add_node
        )

        self.__flask_app.run()

    @staticmethod
    def __add_node():
        docker_client = APIClient(base_url=TwinHub.DOCKER_CLIENT_URI)

        responses = docker_client.build(
            dockerfile=TwinHub.DOCKERFILE_PATH,
            path=TwinHub.TWIN_DOCKER_SOURCES_DIR,
            encoding=TwinHub.DEFAULT_DOCKERFILE_ENCODING,
            rm=True,
            tag=TwinHub.NODE_IMAGE_TAG
        )

        for msg in responses:
            print(msg)

        # Creating network if not exists.
        network = docker_client.networks(names=[TwinHub.NETWORK_NAME])
        if not network:
            docker_client.create_network(TwinHub.NETWORK_NAME, driver="bridge")

        # Creating new container
        TwinHub.NODE_COUNTER += 1
        node_name = 'twin_node_{}'.format(TwinHub.NODE_COUNTER)

        container = docker_client.create_container(
            TwinHub.NODE_IMAGE_TAG,
            name=node_name,
            ports=[5000],
            tty=True,
            stdin_open=True,
            detach=True,
            hostname=node_name
        )

        docker_client.start(container['Id'])

        docker_client.connect_container_to_network(
            container=node_name,
            net_id=TwinHub.NETWORK_NAME
        )

        return "<html><h1>Hello world</h1></html>"
