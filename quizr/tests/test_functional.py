import unittest


class ViewTests(unittest.TestCase):
    def setUp(self):
        import os
        import pkg_resources
        from pyramid.paster import bootstrap
        pkgroot = pkg_resources.get_distribution('quizr').location
        testing_ini = os.path.join(pkgroot, 'testing.ini')
        env = bootstrap(testing_ini)
        self.closer = env['closer']
        from webtest import TestApp
        self.testapp = TestApp(env['app'])

    def tearDown(self):
        import transaction
        transaction.abort()
        self.closer()

    def login(self):
        self.testapp.post(
            '/register',
            {
                'form.submitted': u'Register',
                'username': u'username',
                'password': u'secret',
                'confirm_password': u'secret',
                'email': u'username@example.com',
                'name': u'John Doe',
            },
            status=302,
        )
        self.testapp.post(
            '/login',
            {'login': 'username', 'password': 'secret'},
            status=302,
        )
