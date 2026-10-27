# In this file, we shall declare all the contants and variables that do not change. 
TEST_URL = "https://julesni.github.io/julesnizeyimana/"
DYNAMIC_DEFAULT_URL = "https://julesni.github.io/julesnizeyimana/"

"""
Constants and configuration for Selenium portfolio testing.
"""

# ============================================================
# WEBSITE CONFIGURATION
# ============================================================

# The local web server must be running on port 8000.
#DYNAMIC_DEFAULT_URL = "http://localhost:8000/"
#DYNAMIC_DEFAULT_URL= "https://julesni.github.io/julesnizeyimana/"

# Portfolio home page.
#TEST_URL = DYNAMIC_DEFAULT_URL + "index.html"

##https://julesni.github.io/julesnizeyimana/index.html
# ============================================================
# NAVIGATION LABELS
# ============================================================

HOME_TEXT = "Home"
ABOUT_TEXT = "About"
PROJECT_TEXT = "Projects"
EXPERTISE_TEXT = "Area of Expertise"
EDUCATION_TEXT = "Education"
BLOG_TEXT = "Blog"
CONTACT_TEXT = "Contact"


# ============================================================
# EXPECTED PAGE URLS
# ============================================================

HOME_URL = TEST_URL
ABOUT_URL = DYNAMIC_DEFAULT_URL + "about.html"
PROJECTS_URL = DYNAMIC_DEFAULT_URL + "projects.html"
EXPERTISE_URL = DYNAMIC_DEFAULT_URL + "expertise.html"
EDUCATION_URL = DYNAMIC_DEFAULT_URL + "education.html"
BLOG_URL = DYNAMIC_DEFAULT_URL + "blog.html"
CONTACT_URL = DYNAMIC_DEFAULT_URL + "contact.html"


# ============================================================
# TEST CONFIGURATION
# ============================================================

# Maximum time Selenium waits for an expected condition.
WAIT_TIMEOUT = 10

# Browser used for the tests.
BROWSER_NAME = "Chrome"

# Directory names relative to the test runner's location.
LOGS_DIRECTORY = "logs"
SCREENSHOTS_DIRECTORY = "screenshots"