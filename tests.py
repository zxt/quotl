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

if __name__ == '__main__':
    unittest.main()
