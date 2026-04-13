from abc import ABC, abstractmethod
from typing import Any


class DataProcessor(ABC):
    def __init__(self):
        self.values = []
        self.nb_values = -1

    @abstractmethod
    def validate(self, data: Any) -> bool:
        pass

    @abstractmethod
    def ingest(self, data: Any) -> None:
        pass

    def output(self) -> tuple[int, str]:
        if len(self.values) == 0:
            raise Exception("Empty list")
        to_return = self.values[0]
        self.values.pop(0)
        self.nb_values += 1
        return (self.nb_values, to_return)

class NumericProcessor(DataProcessor):
    def __init__(self):
        super().__init__()

    def validate(self, data: Any) -> bool:
        if type(data) == list:
            for value in data:
                if type(value) not in (int, float):
                    return False
        else:
            if type(data) not in (int, float):
                return False
        return True

    def ingest(self, data: Any) -> None:
        if self.validate(data) == False:
            raise TypeError("Improper numeric data")
        if type(data) == list:
            for value in data:
                self.values.append(str(value))
        else:
            self.values.append(str(data))

class TextProcessor(DataProcessor):
    def validate(self, data: Any) -> bool:
        if type(data) == list:
            for value in data:
                if type(value) != str:
                    return False
        else:
            if type(data) != str:
                return False
        return True

    def ingest(self, data: Any) -> None:
        if self.validate(data) == False:
            raise TypeError("Improper text data")
        if type(data) == list:
            for value in data:
                self.values.append(value)
        else:
            self.values.append(data)


class LogProcessor(DataProcessor):
    def validate(self, data: Any) -> bool:
        if type(data) == list:
            for value in data:
                if type(value) != dict:
                    return False
        else:
            if type(data) != dict:
                return False
        return True

    def ingest(self, data: Any) -> None:
        return

if __name__ == "__main__":
    print("=== Code Nexus - Data Processor ===")
    print("Testing Numeric Processor...")
    processor = NumericProcessor()

    print(f"  Trying to validate input '42': {processor.validate(42)}")
    print(f"  Trying to validate input 'Hello': {processor.validate("Hello")}")
    try:
        print(f"  Test invalid ingestion of string 'foo' without prior validation: {processor.ingest("foo")}")
    except Exception as e:
        print(f"  Got exception: {e}")
    print(f"  Processing data: [5, 4, 3, 2, 1]:")
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
    print(f"  Processing data: ['Hello', 'Nexus', 'World']:")
    processor.ingest(['Hello', 'Nexus', 'World'])
    print("  Extracting 1 value...")
    result = processor.output()
    print(f"  Text value {result[0]}: {result[1]}")

    print("\nTesting Text Processor...")

    