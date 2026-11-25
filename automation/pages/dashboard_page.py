
from playwright.sync_api import Page, expect
from locators.dashboard_locators import DashboardLocators


class DashboardPage:

    def __init__(self, page: Page):
        self.page = page

    def open(self):
        self.page.goto(
            "http://localhost:5173",
            wait_until="networkidle"
        )

    def verify_dashboard_title(self):
        expect(
            self.page.locator(
                DashboardLocators.DASHBOARD_TITLE
            )
        ).to_have_text("Turbo Test Automation")

    def verify_test_cases(self):
        rows = self.page.locator(
            ".panel"
        ).first.locator("table tbody tr")

        expect(rows).to_have_count(2)

    def run_authentication_suite(self):
        self.page.locator(
            DashboardLocators.RUN_AUTH_BUTTON
        ).click()

    def verify_execution_queued(self):
        expect(
            self.page.locator(
                DashboardLocators.QUEUED_STATUS
            ).first
        ).to_be_visible(timeout=10000)
