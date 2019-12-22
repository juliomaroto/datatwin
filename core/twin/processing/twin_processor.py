from core.calls import TwinProcessorCaller
from core.twin.processing.twin_base import TwinBase
from importlib import import_module


class TwinProcessor(TwinBase):
    def __init__(self, config: {}):
        self.__config = config

    def start(self):
        twin_job: {} = self.__config.get('twin-job')
        module = twin_job.get("module")

        module_path = "{}.{}".format(self.BASE_PATH_EXTRA_MODULE, module)
        _module = import_module(module_path)

        class_name = "".join([tkn.capitalize() for tkn in module.split("_")])
        _class = getattr(_module, class_name)

        instance = _class()

        yielded_results = instance.run()

        """
            Asynchronous calls to next defined processors defined for
            the pipeline
        """
        for res in yielded_results:
            twin_processor_caller: TwinProcessorCaller = self.__config.get(
                self.TWIN_PROCESSOR_CALLER_KEY
            )

            twin_processor_caller.call(res)
