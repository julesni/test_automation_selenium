
# from selenium import webdriver
# from selenium.webdriver.chrome.service import Service
# from selenium.webdriver.support.ui import WebDriverWait
# from selenium.common.exceptions import TimeoutException
# from selenium.webdriver.common.by import By
# import time

# # Initialize the Chrome WebDriver
# service = Service("/usr/local/bin/chromedriver")
# driver = webdriver.Chrome(service=service)


# def test_click_item(test_url, target_url, itemname):
#     try:
#         # Open the starting page
#         driver.get(test_url)
#         driver.maximize_window()

#         print(f"\nTesting: {itemname}", flush=True)
#         print(f"Starting URL: {driver.current_url}", flush=True)
#         print(f"Expected URL: {target_url}", flush=True)

#         # Wait until the page has loaded
#         WebDriverWait(driver, 10).until(
#             lambda d: d.execute_script(
#                 "return document.readyState"
#             ) == "complete"
#         )

#         # Find all links matching the requested visible text
#         links = driver.find_elements(
#             By.LINK_TEXT, itemname
#         )

#         print(
#             f"Matching links found: {len(links)}",
#             flush=True
#         )

#         for index, link in enumerate(links):
#             print(
#                 f"Link {index + 1}: "
#                 f"href={link.get_attribute('href')}, "
#                 f"displayed={link.is_displayed()}",
#                 flush=True
#             )

#         # Select the first visible, enabled link
#         link_element = next(
#             (
#                 link for link in links
#                 if link.is_displayed() and link.is_enabled()
#             ),
#             None
#         )

#         if link_element is None:
#             raise Exception(
#                 f"No visible, enabled link found for '{itemname}'"
#             )

#         # Click the navigation link
#         link_element.click()

#         # Wait for JavaScript navigation to update the URL
#         WebDriverWait(driver, 10).until(
#             lambda d: d.current_url == target_url
#         )

#         print(
#             f"PASS: Navigation for '{itemname}' "
#             f"completed successfully!",
#             flush=True
#         )

#         print(
#             f"Current URL: {driver.current_url}",
#             flush=True
#         )

#         # Automatically pause so the page can be inspected
#         print(
#             "Waiting 5 seconds before the next test...",
#             flush=True
#         )
#         time.sleep(5)

#     except TimeoutException:
#         print(
#             f"TIMEOUT: Navigation failed for '{itemname}'.",
#             flush=True
#         )
#         print(f"Expected URL: {target_url}", flush=True)
#         print(f"Actual URL: {driver.current_url}", flush=True)

#         # Print browser-side JavaScript errors, if available
#         try:
#             for entry in driver.get_log("browser"):
#                 print(entry, flush=True)
#         except Exception as err:
#             print(f"Could not retrieve browser logs: {err}")

#     except Exception as err:
#         print(
#             f"Test failed for '{itemname}': {err}",
#             flush=True
#         )


# def close_browser():
#     #Close Chrome after all navigation tests finish.
#     try:
#         driver.quit()
#         print("Browser closed successfully.", flush=True)
#     except Exception as err:
#         print(f"Error closing browser: {err}", flush=True)


# ============================
# Selenium test functions and structured logging for the portfolio.
#===========================================

import logging
import os
import platform
import time
from datetime import datetime
from pathlib import Path

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import (
    TimeoutException,
    WebDriverException,
)

from includes import constants


# ============================================================
# DIRECTORIES
# ============================================================

# Resolve paths relative to the Selenium test runner directory.
BASE_DIR = Path(__file__).resolve().parent.parent

LOGS_DIR = BASE_DIR / constants.LOGS_DIRECTORY
SCREENSHOTS_DIR = BASE_DIR / constants.SCREENSHOTS_DIRECTORY

LOGS_DIR.mkdir(parents=True, exist_ok=True)
SCREENSHOTS_DIR.mkdir(parents=True, exist_ok=True)


# ============================================================
# LOGGING CONFIGURATION
# ============================================================

RUN_TIMESTAMP = datetime.now().strftime("%Y%m%d_%H%M%S_%f")

LOG_FILE = LOGS_DIR / f"Test_{RUN_TIMESTAMP}.log"

logger = logging.getLogger("portfolio_selenium")
logger.setLevel(logging.INFO)
logger.propagate = False

# Prevent duplicate handlers if the module is imported more than once.
if not logger.handlers:
    file_handler = logging.FileHandler(
        LOG_FILE,
        encoding="utf-8"
    )

    formatter = logging.Formatter(
        "%(asctime)s | %(levelname)s | %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S"
    )

    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)

    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)


# ============================================================
# BROWSER CONFIGURATION
# ============================================================

driver = None


def initialize_browser():
    """Start Chrome and record browser and operating-system details."""
    global driver

    service = Service("/usr/local/bin/chromedriver")

    options = webdriver.ChromeOptions()
    options.add_argument("--headless=new")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--window-size=1920,1080")

    driver = webdriver.Chrome(
        service=service,
        options=options
    )
    driver.maximize_window()

    browser_name = driver.capabilities.get(
        "browserName", constants.BROWSER_NAME
    )

    browser_version = driver.capabilities.get(
        "browserVersion", "Unknown"
    )

    logger.info(
        "RUN START | "
        "Website=%s | "
        "Browser=%s %s | "
        "OS=%s | "
        "Python=%s",
        constants.TEST_URL,
        browser_name,
        browser_version,
        platform.platform(),
        platform.python_version()
    )

    return driver


# ============================================================
# TEST RESULT LOGGING
# ============================================================

def record_test_result(
    test_id,
    description,
    expected,
    actual,
    status,
    duration,
    url,
    error=None,
    screenshot=None
):
    #Write a structured test result to the log."""

    message = (
        f"{test_id} | "
        f"Test={description} | "
        f"Expected={expected} | "
        f"Actual={actual} | "
        f"Status={status} | "
        f"Duration={duration:.2f}s | "
        f"URL={url}"
    )

    if error:
        message += f" | Error={error}"

    if screenshot:
        message += f" | Screenshot={screenshot}"

    if status == "FAIL":
        logger.error(message)
    else:
        logger.info(message)


# ============================================================
# SCREENSHOT CAPTURE
# ============================================================

def capture_failure_screenshot(test_id):
    """Save a screenshot when a test fails."""

    if driver is None:
        return None

    screenshot_path = (
        SCREENSHOTS_DIR / f"{test_id}_fail_{RUN_TIMESTAMP}.png"
    )

    try:
        saved = driver.save_screenshot(str(screenshot_path))

        if saved:
            return str(screenshot_path.relative_to(BASE_DIR))

    except WebDriverException as error:
        logger.error(
            "%s | Screenshot capture failed | Error=%s",
            test_id,
            error
        )

    return None


# ============================================================
# NAVIGATION TEST
# ============================================================

def test_click_item(
    test_id,
    test_url,
    target_url,
    itemname
):
#======================================
#   Test a navigation link and record PASS or FAIL.

#   Returns a dictionary containing the test outcome.
#=================================================== 

    start_time = time.perf_counter()

    expected = (
        f"Click '{itemname}' and reach {target_url}"
    )

    actual = "Test did not complete"
    error_message = None
    screenshot = None
    status = "FAIL"

    try:
        if driver is None:
            raise RuntimeError("Browser has not been initialized.")

        # Open the starting page.
        driver.get(test_url)

        WebDriverWait(
            driver,
            constants.WAIT_TIMEOUT
        ).until(
            lambda browser: browser.execute_script(
                "return document.readyState"
            ) == "complete"
        )

        # Locate matching links.
        links = driver.find_elements(
            By.LINK_TEXT,
            itemname
        )

        link_element = next(
            (
                link for link in links
                if link.is_displayed() and link.is_enabled()
            ),
            None
        )

        if link_element is None:
            raise AssertionError(
                f"No visible, enabled link found for '{itemname}'."
            )

        # Click the link.
        link_element.click()

        # Wait for the expected destination.
        WebDriverWait(
            driver,
            constants.WAIT_TIMEOUT
        ).until(
            lambda browser: browser.current_url == target_url
        )

        actual = f"Navigation successful: {driver.current_url}"
        status = "PASS"

    except Exception as error:
        error_message = f"{type(error).__name__}: {error}"

        if driver is not None:
            try:
                actual = (
                    f"Navigation unsuccessful; "
                    f"current URL={driver.current_url}"
                )
            except WebDriverException:
                actual = "Unable to retrieve current browser URL"

        screenshot = capture_failure_screenshot(test_id)

    finally:
        duration = time.perf_counter() - start_time

        current_url = "Unavailable"

        if driver is not None:
            try:
                current_url = driver.current_url
            except WebDriverException:
                pass

        record_test_result(
            test_id=test_id,
            description=f"Navigation: {itemname}",
            expected=expected,
            actual=actual,
            status=status,
            duration=duration,
            url=current_url,
            error=error_message,
            screenshot=screenshot
        )
# Keep a short pause between browser tests.
    time.sleep(0.5)
    return {
        "test_id": test_id,
        "description": f"Navigation: {itemname}",
        "status": status,
        "duration": duration,
        "error": error_message,
    }


# ============================================================
# NEGATIVE TEST
# ============================================================

def test_missing_link(test_id, test_url):
#====================
#Deliberately fail by searching for a nonexistent link.
#This is a negative test used to demonstrate failure logging.
#==========================

    start_time = time.perf_counter()

    description = "Negative test: nonexistent link: CERTIFICATES"
    expected = (
        "The nonexistent link should not be found; "
        "the negative test should record FAIL."
    )

    actual = "Test did not complete"
    error_message = None
    screenshot = None
    status = "FAIL"

    try:
        if driver is None:
            raise RuntimeError("Browser has not been initialized.")

        driver.get(test_url)

        WebDriverWait(
            driver,
            constants.WAIT_TIMEOUT
        ).until(
            lambda browser: browser.execute_script(
                "return document.readyState"
            ) == "complete"
        )

        nonexistent_link = driver.find_elements(
            By.LINK_TEXT,
            "This Link Does Not Exist"
        )

        if nonexistent_link:
            actual = (
                "Unexpectedly found the nonexistent test link."
            )

            raise AssertionError(actual)

        # The expected condition has occurred: the link is absent.
        actual = (
            "The nonexistent link was not found; "
            "the test correctly detected its absence."
        )

        # Deliberately mark the negative test as FAIL so the
        # assignment has an explicit recorded failure.
        error_message = (
            "Expected negative-test failure: "
            "the deliberately nonexistent link was absent."
        )

    except Exception as error:
        error_message = f"{type(error).__name__}: {error}"

        if driver is not None:
            try:
                actual = (
                    f"Negative test encountered an exception; "
                    f"URL={driver.current_url}"
                )
            except WebDriverException:
                actual = "Unable to retrieve current browser URL"

    finally:
        duration = time.perf_counter() - start_time

        current_url = "Unavailable"

        if driver is not None:
            try:
                current_url = driver.current_url
            except WebDriverException:
                pass

        screenshot = capture_failure_screenshot(test_id)

        record_test_result(
            test_id=test_id,
            description=description,
            expected=expected,
            actual=actual,
            status=status,
            duration=duration,
            url=current_url,
            error=error_message,
            screenshot=screenshot
        )

    return {
        "test_id": test_id,
        "description": description,
        "status": status,
        "duration": duration,
        "error": error_message,
    }


# ============================================================
# BROWSER CLEANUP
# ============================================================

def close_browser():
    """Close Chrome safely after all tests have finished."""

    global driver

    if driver is not None:
        try:
            driver.quit()
            logger.info("BROWSER CLOSED | Chrome session terminated.")
        except WebDriverException as error:
            logger.error(
                "BROWSER CLOSE ERROR | %s",
                error
            )
        finally:
            driver = None


def close_logging():
    #Flush and close all log handlers.

    for handler in logger.handlers[:]:
        handler.flush()
        handler.close()
        logger.removeHandler(handler)
       