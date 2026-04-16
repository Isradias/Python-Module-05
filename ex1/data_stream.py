from abc import ABC, abstractmethod
from typing import Any


class DataProcessor(ABC):
    def __init__(self):
        self.values: list = []
        self.nb_values: int = -1

    @abstractmethod
    def validate(self, data: Any) -> bool:
        pass

    @abstractmethod
    def ingest(self, data: Any) -> None:
        pass

    def output(self) -> tuple[int, str]:
        if len(self.values) == 0:
            raise Exception("Empty list")
        self.nb_values += 1
        return (self.nb_values, self.values.pop(0))


class NumericProcessor(DataProcessor):
    def __init__(self):
        super().__init__()

    def validate(self, data: Any) -> bool:
        if type(data) is list:
            for value in data:
                if type(value) not in (int, float):
                    return False
        else:
            if type(data) not in (int, float):
                return False
        return True

    def ingest(self, data: Any) -> None:
        if self.validate(data) is False:
            raise TypeError("Improper numeric data")
        if type(data) is list:
            for value in data:
                self.values.append(str(value))
        else:
            self.values.append(str(data))


class TextProcessor(DataProcessor):
    def validate(self, data: Any) -> bool:
        if type(data) is list:
            for value in data:
                if type(value) is not str:
                    return False
        else:
            if type(data) is not str:
                return False
        return True

    def ingest(self, data: Any) -> None:
        if self.validate(data) is False:
            raise TypeError("Improper text data")
        if type(data) is list:
            for value in data:
                self.values.append(value)
        else:
            self.values.append(data)


class LogProcessor(DataProcessor):
    def validate(self, data: Any) -> bool:
        if type(data) is list:
            for value in data:
                if type(value) is not dict:
                    return False
        else:
            if type(data) is not dict:
                return False
        return True

    def ingest(self, data: Any) -> None:
        if self.validate(data) is False:
            raise TypeError("Improper log data")
        if type(data) is list:
            for value in data:
                self.values.append(f"{value["log_level"]}: "
                                   f"{value["log_message"]}")
        else:
            self.values.append(f"{data["log_level"]}: {data["log_message"]}")


class DataStream:
    def __init__(self):
        self.processors: dict = {}

    def register_processor(self, proc: DataProcessor) -> None:
        for processor in self.processors:
            if type(proc) is type(processor):
                raise Exception("This type of processor already exists.")
        self.processors.update({proc: 0})

    def process_stream(self, stream: list[Any]) -> None:
        self.remaining: list = stream.copy()
        for value in stream:
            for proc in self.processors:
                try:
                    proc.ingest(value)
                    if type(value) is list:
                        self.processors[proc] += len(value)
                    else:
                        self.processors[proc] += 1
                    print(f"{proc.__class__.__name__} ingests : {value}")
                    self.remaining.remove(value)
                    break
                except Exception:
                    pass
        for value in self.remaining:
            print("DataStream error - "
                  f"Can't process element in stream: {value}")

    def print_processors_stats(self) -> None:
        print("\n== DataStream statistics ==")
        if len(self.processors) == 0:
            print("No processor found, no data")
        else:
            for proc in self.processors:
                print(f"{proc.__class__.__name__}: "
                      f"total {self.processors[proc]}, "
                      f"remaining {len(proc.values)} on processor")


def main() -> None:

    sample: list = [
        'Hello world',
        [3.14, -1, 2.71],
        [{'log_level': 'WARNING',
          'log_message': 'Telnet access! Use ssh instead'},
         {'log_level': 'INFO',
          'log_message': 'User wil is connected'}],
        42,
        ['Hi', 'five']]

    print("=== Code Nexus - Data Stream ===")
    print("Initialize Data Stream...")
    general_processor = DataStream()

    general_processor.print_processors_stats()
    print("\n=== Number processor added ===")
    num_proc = NumericProcessor()
    general_processor.register_processor(num_proc)
    general_processor.process_stream(sample)
    general_processor.print_processors_stats()

    print("\n=== Text processor added ===")
    text_proc = TextProcessor()
    general_processor.register_processor(text_proc)
    general_processor.process_stream(sample)
    general_processor.print_processors_stats()

    print("\n=== Log processor added ===")
    log_proc = LogProcessor()
    general_processor.register_processor(log_proc)
    general_processor.process_stream(sample)
    general_processor.print_processors_stats()

    print("\nConsume some elements: Numeric 3, Text 2, Log 1\n")

    for n in range(3):
        num_proc.output()

    for n in range(2):
        text_proc.output()

    for n in range(1):
        log_proc.output()

    general_processor.print_processors_stats()


if __name__ == "__main__":
    main()
