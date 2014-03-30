import unittest

from pyramid import testing


def init_db():
    from quizr.models import DBSession
    from quizr.models import Base
    from sqlalchemy import create_engine
    engine = create_engine('sqlite://')
    DBSession.configure(bind=engine)
    Base.metadata.bind = engine
    Base.metadata.create_all(engine)
    session = DBSession()
    return session


def register_templates(config):
    config.testing_add_renderer('templates/login.pt')
    config.testing_add_renderer('templates/toolbar.pt')


class ViewTests(unittest.TestCase):
    def setUp(self):
        self.session = init_db()
        self.config = testing.setUp()

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

    def test_main_view(self):
        from quizr.views import main_view
        self.config.testing_securitypolicy(u'username')
        self.config.include(register_templates)
        request = testing.DummyRequest()
        result = main_view(request)
        self.assertEqual(result['username'], u'username')

    def test_registration_nosubmit(self):
        from quizr.views import user_add
        self.config.include(register_templates)
        request = testing.DummyRequest()
        result = user_add(request)
        self.assertTrue('form' in result)

    def test_registration_submit_empty(self):
        from quizr.views import user_add
        self.config.include(register_templates)
        request = testing.DummyRequest()
        result = user_add(request)
        self.assertTrue('form' in result)
        request = testing.DummyRequest(post={'form.submitted': 'Shoot'})
        result = user_add(request)
        self.assertEqual(
            result['form'].form.errors,
            {
                'username': u'Missing value',
                'confirm_password': u'Missing value',
                'password': u'Missing value',
                'email': u'Missing value',
                'name': u'Missing value'
            }
        )

    def test_registration_submit_schema_succeed(self):
        from quizr.views import user_add
        from quizr.models import User
        self.config.include('quizr.addroutes')
        request = testing.DummyRequest(
            post={
                'form.submitted': u'Register',
                'username': u'username',
                'password': u'secret',
                'confirm_password': u'secret',
                'email': u'username@example.com',
                'name': u'John Doe',
            }
        )
        user_add(request)
        users = self.session.query(User).all()
        self.assertEqual(len(users), 1)
        user = users[0]
        self.assertEqual(user.username, u'username')
        self.assertEqual(user.name, u'John Doe')
        self.assertEqual(user.email, u'username@example.com')

    def test_login_view_submit_fail(self):
        from quizr.views import login_view
        self.config.include('quizr.addroutes')
        self._addUser()
        request = testing.DummyRequest(
            post={
                'submit': u'Login',
                'login': u'username',
                'password': u'wrongpassword',
            }
        )
        login_view(request)
        messages = request.session.peek_flash()
        self.assertEqual(messages, [u'Failed to login.'])

    def test_login_view_submit_success(self):
        from quizr.views import login_view
        self.config.include('quizr.addroutes')
        self._addUser()
        request = testing.DummyRequest(
            post={
                'submit': u'Login',
                'login': u'username',
                'password': u'password',
            }
        )
        login_view(request)
        messages = request.session.peek_flash()
        self.assertEqual(messages, [u'Logged in successfully.'])

    def test_logout_view(self):
        from quizr.views import logout_view
        self.config.include('quizr.addroutes')
        request = testing.DummyRequest()
        logout_view(request)
        messages = request.session.peek_flash()
        self.assertEqual(messages, [u'Logged out successfully.'])