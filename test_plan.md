# Selenium Portfolio Link Testing Plan

**Project:** Jules Nizeyimana Professional Portfolio  
**Testing tool:** Python and Selenium WebDriver  
**Browser:** Google Chrome  
**Test environment:** Local HTTP server  
**Base URL:** `https://julesni.github.io/julesnizeyimana/`
**Base URL:** 
https://julesni.github.io/julesnizeyimana/

## 1. Objective

The objective of this test plan is to verify that the portfolio's main navigation links work as expected and that the Selenium automation records both successful and failed tests.

Each test will have a unique ID, an expected result, an actual result, a status, and an execution duration.

## 2. Test Cases

| Test ID | What is tested | Steps | Expected result |
|---|---|---|---|
| TC-01 | Home page | Open the portfolio home page. | The home page loads successfully, and the browser reaches the expected URL. |
| TC-02 | About navigation | Open the home page and click the About link. | The About page opens, and the URL matches the expected destination. |
| TC-03 | Projects navigation | Open the home page and click the Projects link. | The Projects page opens, and the URL matches the expected destination. |
| TC-04 | Area of Expertise navigation | Open the home page and click the Area of Expertise link. | The Expertise page opens, and the URL matches the expected destination. |
| TC-05 | Education navigation | Open the home page and click the Education link. | The Education page opens, and the URL matches the expected destination. |
| TC-06 | Blog navigation | Open the home page and click the Blog link. | The Blog page opens, and the URL matches the expected destination. |
| TC-07 | Contact navigation | Open the home page and click the Contact link. | The Contact page opens, and the URL matches the expected destination. |
| TC-08 | Negative test: nonexistent link | Open the home page and attempt to locate a deliberately nonexistent link(CERTIFICATES). | The element is not found; the test is recorded as FAIL, a screenshot is saved, and the remaining tests continue. |

## 3. Test Execution Rules

1. Each test must have a unique test ID.
2. Tests must verify their expected outcomes rather than only click links.
3. Each test must record its expected and actual results.
4. Each test must record PASS or FAIL and its duration.
5. Failures must include the error message and the browser URL at the time of failure.
6. Failed tests must produce screenshots where possible.
7. A failed test must not prevent subsequent tests from running.
8. Each execution must produce a timestamped log file.
9. Each execution must include a run header and a final summary.

## 4. Acceptance Criteria

The test automation is considered operational when:

- All eight test cases execute.
- Each test produces a structured log entry.
- The negative test demonstrates failure logging.
- The log includes timestamps and severity levels.
- Failures include diagnostic information and screenshots where possible.
- The run summary reports the total, passed, and failed tests.
