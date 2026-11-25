
from pages.dashboard_page import DashboardPage


class DashboardSteps:

    def __init__(self, page):
        self.dashboard = DashboardPage(page)

    def open_dashboard(self):
        self.dashboard.open()

    def verify_dashboard(self):
        self.dashboard.verify_dashboard_title()
        self.dashboard.verify_test_cases()

    def execute_authentication_tests(self):
        self.dashboard.run_authentication_suite()

    def verify_execution_result(self):
        self.dashboard.verify_execution_queued()
