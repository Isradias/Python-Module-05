from abc import ABC, abstractmethod, Any
import typing


class DataProcessor(ABC):
    @abstractmethod
    def validade(self, data: Any) -> bool:
        pass

    @abstractmethod
    def ingest(self, data: Any) -> None:
        pass

    def output(self) -> tuple[int, str]:
        pass

class NumericProcessor(DataProcessor):
    def validade(self, data: Any) -> bool:
        return

     def ingest(self, data: Any) -> None:
        return

class TextProcessor(DataProcessor):
    def validade(self, data: Any) -> bool:
        return

     def ingest(self, data: Any) -> None:
        return


class LogProcessor(DataProcessor):
    def validade(self, data: Any) -> bool:
        return

     def ingest(self, data: Any) -> None:
        return