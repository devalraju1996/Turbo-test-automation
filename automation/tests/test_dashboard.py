
from steps.dashboard_steps import DashboardSteps


def test_dashboard_loads(browser_page):

    steps = DashboardSteps(browser_page)

    steps.open_dashboard()

    steps.verify_dashboard()


def test_authentication_execution(browser_page):

    steps = DashboardSteps(browser_page)

    steps.open_dashboard()

    steps.execute_authentication_tests()

    steps.verify_execution_result()
