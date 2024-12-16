import unittest
from config_parser import run_parser

class TestConfigParser(unittest.TestCase):

    def test_web_server_configuration(self):
        config = """-- Конфигурация веб-сервера
var port := 8080;
var host := "localhost";
begin
    document_root := "/var/www/html";
    max_clients := 100;
end"""

        expected_output = """<?xml version=\"1.0\" ?>
<configuration>
    <port>8080</port>
    <host>localhost</host>
    <dictionary>
        <document_root>/var/www/html</document_root>
        <max_clients>100</max_clients>
    </dictionary>
</configuration>"""

        output = run_parser(config)
        self.assertEqual(output.strip(), expected_output.strip())

    def test_bd_configuration(self):
        config = """-- Настройки базы данных
var db_name := "test_db";
var max_connections := 20;
begin
    user := "admin";
    password := "secret";
end"""

        expected_output = """<?xml version=\"1.0\" ?>
<configuration>
    <db_name>test_db</db_name>
    <max_connections>20</max_connections>
    <dictionary>
        <user>admin</user>
        <password>secret</password>
    </dictionary>
</configuration>"""

        output = run_parser(config)
        self.assertEqual(output.strip(), expected_output.strip())

    def test_syntax_error(self):
        config = """var port = 8080;"""  # Ошибка: отсутствует :=

        with self.assertRaises(SyntaxError):
            run_parser(config)

    def test_nested_structure(self):
        config = """-- Вложенная структура
var root := "main";
begin
    var sub_key := "value";
    end;
end;"""  # Ошибка: Лишний end

        with self.assertRaises(SyntaxError):
            run_parser(config)

    def test_undefined_constant(self):
        config = """var db_name := unknown_constant;"""  # Ошибка: неопределённая константа

        with self.assertRaises(ValueError):
            run_parser(config)