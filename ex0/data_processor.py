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

if __name__ == "__main__":
    print("=== Code Nexus - Data Processor ===")
    print("Testing Numeric Processor...")
    processor = NumericProcessor()

    print(f"  Trying to validate input '42': {processor.validate(42)}")
    print(f"  Trying to validate input 'Hello': {processor.validate("Hello")}")
    try:
        print("  Test invalid ingestion of string 'foo' "
              f"without prior validation: {processor.ingest("foo")}")
    except Exception as e:
        print(f"  Got exception: {e}")
    print("  Processing data: [5, 4, 3, 2, 1]:")
    processor.ingest([5, 4, 3, 2, 1])
    print("  Extracting 42 values")
    try:
        for n in range(42):
            result = processor.output()
            rank = result[0]
            value = result[1]
            print(f"  Numeric value {rank}: {value}")
    except Exception as e:
        print(f"  Got exception: {e}")

    print("\nTesting Text Processor...")
    processor = TextProcessor()
    print(f"  Trying to validate input '42': {processor.validate(42)}")
    print("  Processing data: ['Hello', 'Nexus', 'World']:")
    processor.ingest(['Hello', 'Nexus', 'World'])
    print("  Extracting 1 value...")
    result = processor.output()
    print(f"  Text value {result[0]}: {result[1]}")

    print("\nTesting Text Processor...")
    processor = LogProcessor()
    print(f"  Trying to validate input 'Hello': {processor.validate('Hello')}")
    data = [{'log_level': 'NOTICE', 'log_message': 'Connection to server'},
            {'log_level': 'ERROR', 'log_message': 'Unauthorized access!!'}]
    print(f"  Processing data: {data}")
    processor.ingest(data)
    print("  Extracting 2 values...")
    try:
        for n in range(3):
            result = processor.output()
            rank = result[0]
            value = result[1]
            print(f"  Log value {rank}: {value}")
    except Exception as e:
        print(e)
