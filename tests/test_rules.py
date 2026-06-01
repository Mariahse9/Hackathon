import pytest
from hackaton.version import Rules

@pytest.mark.parametrize(
    "text, expected",
    [
        ("Сервер упал", "incidents"),
        ("Вы выиграли приз", "spam"),
        ("Ваш аккаунт заблокирован", "security_alerts"),
        ("Счет на оплату", "finance_and_docs"),
        ("Назначена встреча", "meetings"),
    ],
)
def test_categories(create_email, text, expected):
    email = create_email(text)
    rules = Rules()
    assert rules.classify(email) == expected

def test_unsorted(create_email):
    email = create_email("Просто текст")
    rules = Rules()
    assert rules.classify(email) == "unsorted"

def test_error(create_email):
    email = create_email("Код ошибки ERR_500")
    rules = Rules()
    assert rules.classify(email).startswith("errors")
