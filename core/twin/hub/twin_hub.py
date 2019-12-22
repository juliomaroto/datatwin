from core.web_server.flask_wrapper import FlaskAppWrapper
from docker import APIClient
import os


class TwinHub:
    DOCKER_CLIENT_URI = 'unix://var/run/docker.sock'
    TWIN_DOCKER_SOURCES_DIR = os.path.join("asset", "twin-docker-sources")
    DOCKERFILE_PATH = "Dockerfile"
    DEFAULT_DOCKERFILE_ENCODING = "utf-8"

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

        response = docker_client.build(
            dockerfile=TwinHub.DOCKERFILE_PATH,
            path=TwinHub.TWIN_DOCKER_SOURCES_DIR,
            encoding=TwinHub.DEFAULT_DOCKERFILE_ENCODING,
            rm=True,
            tag='twin/volume'
        )

        for it in response:
            print(it)
