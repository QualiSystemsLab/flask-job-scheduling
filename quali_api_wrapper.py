import requests
from requests import Response


class QualiApiException(Exception):
    pass


class QualiApiAuthException(QualiApiException):
    pass


class QualiApiSession:
    def __init__(self, host, username='', password='', domain='Global', token='', port=9000, use_https=False,
                 verify_ssl=False):
        self._base_url = self._build_base_url(host, port, use_https)
        self._verify_ssl = verify_ssl
        self._session = requests.Session()
        self.domain = domain
        self.login_set_auth_header(username, password, domain, token)

    @staticmethod
    def _build_base_url(host, port, use_https):
        protocol = "https" if use_https else "http"
        return f"{protocol}://{host}:{port}/Api"

    @staticmethod
    def _validate_json_response(response: Response):
        if not response.ok:
            raise QualiApiException(f"Failed request. Code: {response.status_code}, Reason: {response.reason}\n"
                                    f"Text: {response.text}")
        return response.json()

    def login_set_auth_header(self, username, password, domain, token):
        if token:
            data = {"token": token, "domain": domain}
        elif username and password:
            data = {"username": username, "password": password, "domain": domain}
        else:
            raise ValueError("Must supply Username / Password OR token_id")
        url = self._base_url + "/Auth/Login"
        response = requests.put(url, json=data, verify=self._verify_ssl)
        if not response.ok:
            raise QualiApiAuthException(f"Failed Login. Status: {response.status_code}, Reason: {response.reason}\n"
                                        f"Text: {response.text}")
        # strip the extraneous quotes
        token = response.text[1:-1]
        self._session.headers.update({"Authorization": f"Basic {token}"})

    # SUITES
    def get_suite_templates(self):
        url = self._base_url + "/Scheduling/SuiteTemplates"
        response = self._session.get(url=url)
        return self._validate_json_response(response)

    def get_suite_template_details(self, suite_template_id):
        url = self._base_url + f"/Scheduling/SuiteTemplates/{suite_template_id}"
        response = self._session.get(url=url)
        return self._validate_json_response(response)

    def enqueue_suite(self, suite_data):
        url = self._base_url + "/Scheduling/Suites"
        response = self._session.post(url=url, headers={"Content-Type": "application/json"}, json=suite_data)
        return self._validate_json_response(response)

    def get_suite_details(self, suite_id):
        url = self._base_url + f"/Scheduling/Suites/{suite_id}"
        response = self._session.get(url=url)
        return self._validate_json_response(response)

    def stop_suite_execution(self, suite_id):
        url = self._base_url + f"/Scheduling/Suites/{suite_id}"
        response = self._session.delete(url=url)
        return self._validate_json_response(response)

    # JOBS
    def enqueue_job(self, job_data: dict):
        url = self._base_url + "/Scheduling/Queue"
        response = self._session.post(url=url, headers={"Content-Type": "application/json"}, json=job_data)
        return self._validate_json_response(response)

    def get_running_jobs(self):
        url = self._base_url + "/Scheduling/Executions"
        response = self._session.get(url)
        return self._validate_json_response(response)


if __name__ == "__main__":
    api = QualiApiSession("localhost", "admin", "admin", "Global")
    suites = api.get_suite_templates()
    pass
