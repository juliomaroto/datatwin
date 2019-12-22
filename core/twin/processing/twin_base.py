import abc


class TwinBase(abc.ABC):
    TWIN_PROCESSOR_CALLER_KEY = "twin-transformer"
    BASE_PATH_EXTRA_MODULE = "core.extra"
