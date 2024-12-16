import argparse
import re
import sys
import xml.etree.ElementTree as ET
from xml.dom.minidom import parseString

class ConfigParser:
    def __init__(self):
        self.constants = {}

    def parse(self, text):
        text = self.remove_comments(text)
        lines = text.splitlines()
        root = ET.Element("configuration")

        while lines:
            line = lines.pop(0).strip()
            if not line:
                continue

            # Разбор констант
            if match := re.match(r"var ([a-zA-Z_][a-zA-Z0-9_]*) := (.+);", line):
                name, value = match.groups()
                self.constants[name] = self.parse_value(value)
                ET.SubElement(root, name).text = str(self.constants[name])

            # Разбор словаря
            elif line == "begin":
                dictionary_element = ET.SubElement(root, "dictionary")
                self.parse_dictionary(lines, dictionary_element)

            else:
                raise SyntaxError(f"Syntax error in line: {line}")

        return root

    def parse_dictionary(self, lines, parent_element):
        while lines:
            line = lines.pop(0).strip()

            if line == "end":
                return

            # Вложенный словарь
            if match := re.match(r"([a-zA-Z_][a-zA-Z0-9_]*) := begin", line):
                name = match.group(1)
                sub_element = ET.SubElement(parent_element, name)
                self.parse_dictionary(lines, sub_element)

            # Пара ключ-значение
            elif match := re.match(r"([a-zA-Z_][a-zA-Z0-9_]*) := (.+);", line):
                name, value = match.groups()
                value_element = ET.SubElement(parent_element, name)
                parsed_value = self.parse_value(value)
                self.build_xml(value_element, parsed_value)

            else:
                raise SyntaxError(f"Syntax error in dictionary line: {line}")

    def parse_value(self, value):
        value = value.strip()

        # Число (int или float)
        if re.match(r"^\d+(\.\d+)?$", value):
            return float(value) if '.' in value else int(value)

        # String
        elif value.startswith("\"") and value.endswith("\""):
            return value[1:-1]

        # List в формате (list ...)
        elif value.startswith("(list") and value.endswith(")"):
            items = value[5:-1].split()
            return [self.parse_value(item) for item in items]

        # List в формате [value, value, ...]
        elif value.startswith("[") and value.endswith("]"):
            items = value[1:-1].split(",")
            return [self.parse_value(item.strip()) for item in items]

        # Константы
        elif value.startswith("$[") and value.endswith("]"):
            const_name = value[2:-1]
            if const_name in self.constants:
                return self.constants[const_name]
            else:
                raise ValueError(f"Undefined constant: {const_name}")

        else:
            raise ValueError(f"Invalid value: {value}")

    def remove_comments(self, text):
        text = re.sub(r"--.*", "", text)
        return "\n".join(line.strip() for line in text.splitlines() if line.strip())

    def build_xml(self, parent_element, value):
        if isinstance(value, list):
            for item in value:
                item_element = ET.SubElement(parent_element, "item")
                item_element.text = str(item)
        else:
            parent_element.text = str(value)

    def to_xml_string(self, root):
        rough_string = ET.tostring(root, encoding="unicode")
        reparsed = parseString(rough_string)
        return reparsed.toprettyxml(indent="    ")

def run_parser(input_text):
    """Function to run the parser and get XML string."""
    config_parser = ConfigParser()
    root = config_parser.parse(input_text)
    return config_parser.to_xml_string(root)

def main():
    parser = argparse.ArgumentParser(description="Config to XML parser")
    args = parser.parse_args()

    input_text = sys.stdin.read()
    config_parser = ConfigParser()

    try:
        root = config_parser.parse(input_text)
        xml_output = config_parser.to_xml_string(root)
        # Вывод только выходных данных в формате XML
        print(xml_output)
    except (SyntaxError, ValueError) as e:
        print(f"Error: {e}", file=sys.stderr)

if __name__ == "__main__":
    main()
