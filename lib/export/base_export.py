

class BaseExportError(RuntimeError):
    pass


class BaseExport():

    def __init__(self) -> None:
        self.external_state: list = []
        pass

    def export(self):
        """
        Start and complete the export process.
        """
        raise NotImplementedError()
    
    def get_external_state():
        pass