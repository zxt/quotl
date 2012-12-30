import os
import unittest
import tempfile
import quotr

class QuotrTestCase(unittest.TestCase):

    def setUp(self):
        self.db_fd, quotr.app.config['DATABASE'] = tempfile.mkstemp()
        quotr.app.config['TESTING'] = True
        self.app = quotr.app.test_client()
        quotr.init_db()

    def tearDown(self):
        os.close(self.db_fd)
        os.unlink(quotr.app.config['DATABASE'])

    def login(self, username, password):
        return self.app.post('/login', data=dict(
            username=username,
            password=password
        ), follow_redirects=True)

    def logout(self):
        return self.app.get('/logout', follow_redirects=True)

    def test_empty_db(self):
        rv = self.app.get('/')
        assert 'No quotes found. How about adding some?' in rv.data

    def test_login_logout(self):
        rv = self.login(quotr.app.config['USERNAME'], quotr.app.config['PASSWORD'])
        assert 'Login successful' in rv.data
        rv = self.logout()
        assert 'Logout successful' in rv.data
        rv = self.login('invalidusername', quotr.app.config['PASSWORD'])
        assert 'Invalid username' in rv.data
        rv = self.login(quotr.app.config['USERNAME'], 'invalidpassword')
        assert 'Invalid password' in rv.data

    def test_add_quote(self):
        self.login('admin', 'default')
        rv = self.app.post('/add', data=dict(
            quote='This is a very <strong>awesome</strong> quote.',
            author='<Anonymous>'
        ), follow_redirects=True)
        assert 'No quotes found. How about adding some?' not in rv.data
        assert 'This is a very <strong>awesome</strong> quote.' in rv.data
        assert '&lt;Anonymous&gt;' in rv.data

if __name__ == '__main__':
    unittest.main()
