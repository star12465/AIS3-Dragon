from flask import Flask
from secret_vault.apis import GetSecretAPI, CreateSecretAPI, ListSecretAPI
from secret_vault.managers import AuthManager, SecretManager
from secret_vault.models import Secret, User
from secret_vault.utils import DB


class SecretVault(object):
    def __init__(self, port, conn_str):
        self.app = Flask('__main__')
        self.db = DB(conn_str)
        self.port = port
        self._add_all_rules()

        AuthManager.initialize(self.db)
        SecretManager.initialize(self.db)
        # with self.db.session() as db_session:
        #     test_secret = Secret.get_by_name(db_session, 'Test_Secret')

        #     if test_secret in User.get_available_secrets_by_username(db_session, 'admin'):
        #         print('Success!!')
        #     print(User.get_available_secrets_by_username(db_session, 'admin'))
        # #     Secret.create(db_session, 'Test_Secret', 'I\'m a Secret!')

    def _add_all_rules(self):
        self.app.add_url_rule('/get_secret/<string:secret_name>', view_func=GetSecretAPI.as_view('get_secret_api'))
        self.app.add_url_rule('/list_secrets', view_func=ListSecretAPI.as_view('list_secret_api'))
        self.app.add_url_rule('/create_secret', view_func=CreateSecretAPI.as_view('create_secret_api'))

    def run(self):
        self.app.run(port=self.port)

