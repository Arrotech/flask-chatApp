import os
import unittest  # noqa
import urllib.request
from flask_testing import LiveServerTestCase
from selenium import webdriver
from app import create_app
from app.extensions import db
from app.api.v1.models.models import User
from flask import url_for
import time

test_user_username = "Harun254"
test_user_email = "gitundugachanja94@gmail.com"
test_user_password = "Harun20930988!"


class Authentication(object):

    def setUp(self):
        self.driver = webdriver.Chrome()
        self.driver.get(self.get_server_url())

        db.session.commit()
        db.drop_all()
        db.create_all()

        self.user = User(username=test_user_username,
                         email=test_user_email, password=test_user_password)

        db.session.add(self.user)
        db.session.commit()

    def tearDown(self):
        self.driver.quit()

    def test_login_user(self):
        self.driver = webdriver.Chrome()
        self.driver.get(self.get_server_url())
        login_link = self.get_server_url() + url_for('chat_v1.login')
        self.driver.get(login_link)
        self.driver.find_element_by_id(
            "username").send_keys(test_user_username)
        self.driver.find_element_by_id(
            "password").send_keys(test_user_password)
        self.driver.find_element_by_tag_name("submit").click()
        time.sleep(2)

        assert url_for("chat_v1.home") in self.driver.current_url


# class TestFrontEnd(LiveServerTestCase):

#     def create_app(self):
#         config_name = "testing"
#         self.app = create_app(config_name)
#         self.app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY')
#         self.app.config.update(
#             # Specify the test database
#             SQLALCHEMY_DATABASE_URI=os.environ.get("TEST_DB_URL"),
#             # Change the port that the liveserver listens on
#             LIVESERVER_PORT=8943
#         )

#         return self.app

#     def setUp(self):
        # self.driver = webdriver.Chrome()
        # self.driver.get(self.get_server_url())

#         db.session.commit()
#         db.drop_all()
#         db.create_all()

#         self.user = User(username=test_user_username,
#                          email=test_user_email, password=test_user_password)

#         db.session.add(self.user)
#         db.session.commit()

#     def tearDown(self):
        # self.driver.quit()

#     def test_server_is_running(self):
#         response = urllib.request.urlopen(self.get_server_url())
#         self.assertEqual(response.code, 200)


if __name__ == '__main__':
    unittest.main()
