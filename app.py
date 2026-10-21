
# from includes import functions
# from includes import constants

# # Map each navigation label to its expected destination URL.
# text_url_array = {
#     constants.HOME_TEXT: constants.HOME_URL,
#     constants.ABOUT_TEXT: constants.ABOUT_URL,
#     constants.HOME_TEXT: constants.HOME_URL,
#     constants.PROJECT_TEXT: constants.PROJECTS_URL,
#     constants.EXPERTISE_TEXT: constants.EXPERTISE_URL,  
#     constants.EDUCATION_TEXT: constants.EDUCATION_URL,
#     constants.BLOG_TEXT: constants.BLOG_URL,
#     constants.CONTACT_TEXT: constants.CONTACT_URL,
# }

# # Test each navigation link.
# for test_name, target_url in text_url_array.items():
#     functions.test_click_item(
#         constants.TEST_URL,
#         target_url,
#         test_name
#     )

# # Close the browser after all tests.
# print("End of tests for all items. Closing the browser now...")
# functions.close_browser()

#==================
# Main entry point for Selenium portfolio tests.
# Runs all tests, records results, and prints a summary.
#=================

import time

from includes import constants
from includes import functions


def main():
    results = []
    suite_start = time.perf_counter()

    try:
        # Start the browser and write the run header to the log.
        functions.initialize_browser()

        # Define the seven navigation tests.
        navigation_tests = [
            ("TC-01", constants.HOME_TEXT, constants.HOME_URL),
            ("TC-02", constants.ABOUT_TEXT, constants.ABOUT_URL),
            ("TC-03", constants.PROJECT_TEXT, constants.PROJECTS_URL),
            ("TC-04", constants.EXPERTISE_TEXT, constants.EXPERTISE_URL),
            ("TC-05", constants.EDUCATION_TEXT, constants.EDUCATION_URL),
            ("TC-06", constants.BLOG_TEXT, constants.BLOG_URL),
            ("TC-07", constants.CONTACT_TEXT, constants.CONTACT_URL),
        ]

        # Execute navigation tests independently so one failure
        # does not prevent the remaining tests from running.
        for test_id, link_text, target_url in navigation_tests:
            result = functions.test_click_item(
                test_id=test_id,
                test_url=constants.TEST_URL,
                target_url=target_url,
                itemname=link_text,
            )
            results.append(result)

        # Execute the negative test.
        negative_result = functions.test_missing_link(
            test_id="TC-08",
            test_url=constants.TEST_URL,
        )
        results.append(negative_result)

    except Exception as error:
        print(f"Test suite setup error: {error}")

    finally:
        functions.close_browser()

        total_duration = time.perf_counter() - suite_start
        passed = sum(1 for result in results if result["status"] == "PASS")
        failed = sum(1 for result in results if result["status"] == "FAIL")
        other = len(results) - passed - failed

        summary = (
            f"TEST SUITE SUMMARY | Total: {len(results)} | "
            f"Passed: {passed} | Failed: {failed} | "
            f"Other: {other} | Duration: {total_duration:.2f}s"
        )

        print("\n" + "=" * 65)
        print(summary)
        print("=" * 65)

        # Write the summary to the same log file.
        for handler in functions.logger.handlers:
            functions.logger.info(summary)
            handler.flush()

        functions.close_logging()


if __name__ == "__main__":
    main()