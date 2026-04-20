from abc import ABC, abstractmethod
from typing import Any, Protocol


class DataProcessor(ABC):
    def __init__(self) -> None:
        self.values: list[str] = []
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
    def __init__(self) -> None:
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


class ExportPlugin(Protocol):
    def process_output(self, data: list[tuple[int, str]]) -> None:
        ...


class ExportCSV:
    def process_output(self, data: list[tuple[int, str]]) -> None:
        print("CSV Output:")
        if len(data) == 0:
            print("--No itens to output")
            return
        print(",".join(value[1] for value in data))


class ExportJSON:
    def process_output(self, data: list[tuple[int, str]]) -> None:
        print("JSON Output:")
        if len(data) == 0:
            print("--No itens to output")
            return
        output = {"item " + str(value[0]): value[1] for value in data}
        print(output)


class DataStream:
    def __init__(self) -> None:
        self.processors: dict[DataProcessor, int] = {}

    def register_processor(self, proc: DataProcessor) -> None:
        for processor in self.processors:
            if type(processor) is type(proc):
                raise Exception("This type of processor already exists.")
        self.processors.update({proc: 0})

    def process_stream(self, stream: list[Any]) -> None:
        self.remaining: list[Any] = stream.copy()
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
        print("")

    def output_pipeline(self, nb: int, plugin: ExportPlugin) -> None:
        for proc in self.processors:
            to_export: list[tuple[int, str]] = []
            for x in range(nb):
                try:
                    to_export.append(proc.output())
                except Exception:
                    break
            plugin.process_output(to_export)


def main() -> None:
    sample: list[Any] = [
        'Hello world',
        [3.14, -1, 2.71],
        [{'log_level': 'WARNING',
          'log_message': 'Telnet access! Use ssh instead'},
         {'log_level': 'INFO',
          'log_message': 'User wil is connected'}],
        42,
        ['Hi', 'five']]

    general_processor: DataStream = DataStream()
    num_proc: NumericProcessor = NumericProcessor()
    text_proc: TextProcessor = TextProcessor()
    log_proc: LogProcessor = LogProcessor()
    csv_export: ExportPlugin = ExportCSV()
    json_export: ExportPlugin = ExportJSON()
    general_processor.register_processor(num_proc)
    general_processor.register_processor(text_proc)
    general_processor.register_processor(log_proc)
    general_processor.process_stream(sample)
    general_processor.print_processors_stats()
    print("Send 3 processed data from each processor to a CSV plugin:")
    general_processor.output_pipeline(3, csv_export)
    general_processor.print_processors_stats()
    print("Send 2 processed data from each processor to a JSON plugin:")
    general_processor.output_pipeline(2, json_export)
    general_processor.print_processors_stats()


if __name__ == "__main__":
    main()
