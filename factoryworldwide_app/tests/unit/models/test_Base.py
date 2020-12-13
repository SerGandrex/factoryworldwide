import unittest
from unittest.mock import Mock, patch

from factoryworldwide_app.models.BaseModel import Base


class BaseModelTestCase(unittest.TestCase):
    def setUp(self) -> None:
        self.model = Base()
        Base.query = Mock()

    @patch('factoryworldwide_app.models.BaseModel.db.session.add', Mock())
    @patch('factoryworldwide_app.models.BaseModel.db.session.commit', Mock())
    def test_save(self):
        self.assertEqual(self.model.save(), self.model)

    @patch('factoryworldwide_app.models.BaseModel.db.session.commit', Mock())
    def test_update(self):
        self.assertEqual(self.model.update(), self.model)

    @patch('factoryworldwide_app.models.BaseModel.db.session.delete', Mock())
    @patch('factoryworldwide_app.models.BaseModel.db.session.commit', Mock())
    def test_delete(self):
        self.assertEqual(self.model.update(), self.model)

    def test_get(self):
        Base.query.get = Mock(return_value=1)
        self.assertEqual(Base.get('1'), 1)

    @patch('factoryworldwide_app.models.BaseModel.Base.query.filter_by')
    def test_filter(self, filter_by_mock):
        filter_by_mock.return_value = Mock()
        filter_by_mock.return_value.first.return_value = 1
        self.assertEqual(Base.filter(filter='filter'), 1)

    def test_list(self):
        Base.query.all = Mock(return_value=1)
        self.assertEqual(Base.list(), 1)
