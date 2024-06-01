import pytest
from app import db
from app.models import Employee

@pytest.fixture(scope='module')
def new_employee():
    employee = Employee(name='testuser', password_hash='testpassword', is_admin=True)
    return employee

def test_new_employee(new_employee):
    assert new_employee.name == 'testuser'
    assert new_employee.password_hash == 'testpassword'
    assert new_employee.is_admin

def test_employee_model(test_client):
    new_emp = Employee(name='testuser', password_hash='testpassword', is_admin=True)
    db.session.add(new_emp)
    db.session.commit()
    emp = Employee.query.filter_by(name='testuser').first()
    assert emp is not None
    assert emp.name == 'testuser'