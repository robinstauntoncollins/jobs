from datetime import datetime
from unittest import mock

import pytest
from api.models import Job


class TestJobsModel():


    def test_basic(self):
        with mock.patch('api.models.get_utc_now', return_value=datetime(2020, 8, 3, 19, 30, 0)):
            new_job = Job().import_data({
                'title': 'Wash Dishes',
                'description': 'Wash the dishes',
                'frequency': 'monthly'
            })

        assert new_job.title == 'Wash Dishes'
        assert new_job.description == 'Wash the dishes'
        assert new_job.last_done == datetime.strptime('2020-08-03T19:30:00', "%Y-%m-%dT%H:%M:%S")
        assert new_job.frequency == 'monthly'
        job_data = new_job.export_data()
        assert job_data == {
            'title': 'Wash Dishes',
            'description': 'Wash the dishes',
            'last_done': datetime.strptime('2020-08-03T19:30:00', "%Y-%m-%dT%H:%M:%S"),
            'frequency': 'monthly'
        }

    def test_invalid_data(self):
        with pytest.raises(ValueError):
            Job().import_data({
                'nottitle': 'Something Else'
            })

    def test_repr(self, test_client):
        new_account = Job().import_data({
            'title': 'Sweep kitchen floor',
            'description': 'Sweep the kitchen floor',
            'frequency': 'daily'
        })
        db.session.add(new_account)
        db.session.commit()
        a = Job.query.first()
        assert repr(a) == "<Job ID: 1> Balance: 0.0 Owner ID: 1"

    # def test_db(self, test_client):
    #     new_account = Job().import_data({
    #         'account_number': '1',
    #         'balance': 0,
    #         'customer_id': 1
    #     })
    #     db.session.add(new_account)
    #     db.session.commit()
    #     account = Job.query.first()
    #     assert account == new_account

    # def test_account_owner(self, test_client):
    #     customer = Customer(name="Robin", surname="Staunton-Collins")
    #     db.session.add(customer)
    #     c = Customer.query.first()
    #     new_account = Job(account_number=1234, balance=50, owner=c)
    #     db.session.add(new_account)
    #     db.session.commit()
    #     acc = Job.query.first()
    #     assert acc.owner == c
    