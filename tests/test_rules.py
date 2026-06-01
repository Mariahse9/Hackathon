import pytest
from verison import Rules, EmailReceiver

@pytest.mark.parametrize(
    "text, expected",
    [
        ("Сервер упал", "incidents"),
        ("Вы выиграли приз", "spam"),
        ("Ваш аккаунт заблокирован", "security_alerts"),
        ("Счет на оплату", "finance_and_docs"),
        ("Назначена встреча", "meetings"),
        ("Нет доступа", "access_and_hr"),
    ],
)
def test_categories(create_email, text, expected):
    email = create_email(text)
    rules = Rules()
    result = rules.classify(email)
    assert result == expected
    assert isinstance(result, str)
    assert result != ""
    assert " " not in result

def test_unsorted(create_email):
    email = create_email("Просто текст")
    rules = Rules()
    result = rules.classify(email)
    assert result == "unsorted"
    assert "/" not in result

def test_error(create_email):
    email = create_email("Код ошибки ERR_500")
    rules = Rules()
    result = rules.classify(email)
    assert result.startswith("errors/")
    assert "incidents" in result or "unsorted" in result

def test_alerts(create_email):
    email = create_email("Alert сервер недоступен")
    rules = Rules()
    assert rules.classify(email) == "alerts"

def test_unclassified_binary_file(tmp_path):
    file = tmp_path / "virus.exe"
    file.write_text("bad")
    email = EmailReceiver(file)
    rules = Rules()
    assert rules.classify(email) == "unclassified"

def test_logs_info(create_email):
    email = create_email("healthcheck system error_log.txt report")
    rules = Rules()
    assert rules.classify(email) == "logs_info"
