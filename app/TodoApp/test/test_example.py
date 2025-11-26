import pytest

"""
Test for app
"""

def test_equal_or_not_equal():

    assert 3 == 3
    assert 3!=2

def test_is_instance():
    assert isinstance('this is a string', str)
    assert not isinstance('1', int)

def test_boolean():
    validated = True
    assert validated is True
    assert ('hello' == 'world') is False

def test_type():
    assert type('He' is str)
    assert type('Wo' is not int)

class Student:
    def __init__(self, first_name: str, 
                 last_name: str, 
                 major: str, 
                 years: int) -> None:
        self.first_name = first_name
        self.last_name = last_name
        self.major = major
        self.years = years

@pytest.fixture
def default_employee():
    return Student('Lox', 'Pidor', 'IEF', 3)


def test_person_initialization(default_employee):
    assert default_employee.first_name == 'Lox'
    assert default_employee.last_name == 'Pidor'
    assert default_employee.major == 'IEF'
    assert default_employee.years == 3