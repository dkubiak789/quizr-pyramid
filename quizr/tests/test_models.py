# -*- coding: utf-8 -*-
import unittest

from pyramid import testing


def init_db():
    from quizr.models import (
        DBSession,
        Base,
        )
    from sqlalchemy import create_engine
    engine = create_engine('sqlite://')
    DBSession.configure(bind=engine)
    Base.metadata.bind = engine
    Base.metadata.create_all(engine)
    session = DBSession()
    return session


class ModelsTestCase(unittest.TestCase):
    def setUp(self):
        self.session = init_db()

    def tearDown(self):
        import transaction
        from quizr.models import DBSession
        transaction.abort()
        DBSession.remove()
        testing.tearDown()

    def _addUser(self, username=u'username'):
        from quizr.models import User
        user = User(username=username, password=u'password', name=u'name',
                    email=u'email')
        self.session.add(user)
        self.session.flush()
        return user


class TestUser(ModelsTestCase):
    def test_add_user(self):
        from quizr.models import User
        user = User(u'username', u'password', u'name', u'email')
        self.session.add(user)
        self.session.flush()
        user = self.session.query(User).filter(User.username == u'username')
        user = user.first()
        self.assertEqual(user.username, u'username')
        self.assertEqual(user.name, u'name')
        self.assertEqual(user.email, u'email')

    def test_doesnt_exitst(self):
        from quizr.models import User
        from sqlalchemy.orm.exc import NoResultFound
        query = self.session.query(User).filter(User.username == u'nobody')
        self.assertRaises(NoResultFound, query.one)

    def test_arleady_exist(self):
        from sqlalchemy.exc import IntegrityError
        self._addUser()
        self.assertRaises(IntegrityError, self._addUser)

    def test_password_hashing(self):
        import cryptacular.bcrypt
        crypt = cryptacular.bcrypt.BCRYPTPasswordManager()
        user = self._addUser()
        self.assertTrue(crypt.check(user.password, u'password'))

    def test_password_checking(self):
        from quizr.models import User
        self._addUser()
        self.assertTrue(User.check_password(u'username', u'password'))
        self.assertFalse(User.check_password(u'username', u'wrong'))
        self.assertFalse(User.check_password(u'nobody', u'password'))

    def test_getting_by_username(self):
        from quizr.models import User
        user = self._addUser()
        self.assertEqual(user, User.get_by_username(u'username'))
