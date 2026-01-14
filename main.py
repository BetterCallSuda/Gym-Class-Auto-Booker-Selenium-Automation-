import os
from time import sleep
from selenium import webdriver
from selenium.common import NoSuchElementException, TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# -------------------- CONFIG --------------------
ACCOUNT_EMAIL = "suda@test.com"
ACCOUNT_PASSWORD = "Avengerironman46"
GYM_URL = "https://appbrewery.github.io/gym"
WAIT_TIME = 5

# -------------------- DRIVER SETUP --------------------
chrome_options = webdriver.ChromeOptions()
chrome_options.add_experimental_option("detach", True)

user_data_dir = os.path.join(os.getcwd(), "Suda")
chrome_options.add_argument(f"--user-data-dir={user_data_dir}")

driver = webdriver.Chrome(options=chrome_options)
driver.get(GYM_URL)
wait = WebDriverWait(driver, WAIT_TIME)

# -------------------- UTILITIES --------------------
def retry(action, retries=5, label="Action"):
    for attempt in range(retries):
        try:
            print(f"Trying {label} (Attempt {attempt + 1})")
            return action()
        except TimeoutException:
            if attempt == retries - 1:
                raise
            sleep(1)

# -------------------- LOGIN --------------------
def login():
    wait.until(EC.element_to_be_clickable(
        (By.CSS_SELECTOR, "a button"))
    ).click()

    wait.until(EC.presence_of_element_located(
        (By.ID, "email-input"))
    ).send_keys(ACCOUNT_EMAIL)

    wait.until(EC.presence_of_element_located(
        (By.ID, "password-input"))
    ).send_keys(ACCOUNT_PASSWORD)

    driver.find_element(By.ID, "submit-button").click()
    wait.until(EC.presence_of_element_located((By.ID, "schedule-page")))

retry(login, label="Login")

# -------------------- BOOKING LOGIC --------------------
def book(button):
    button.click()
    wait.until(lambda d: button.text == "Booked")

booked_count = 0
class_cards = driver.find_elements(By.CSS_SELECTOR, "div[id^='class-card-']")

for card in class_cards:
    try:
        day_group = card.find_element(
            By.XPATH, "./ancestor::div[contains(@id,'day-group-')]")
        day_title = day_group.find_element(By.TAG_NAME, "h2").text
        time_text = card.find_element(By.CSS_SELECTOR, "p[id^='class-time-']").text
    except NoSuchElementException:
        continue

    if ("Tue" in day_title or "Thu" in day_title) and "6:00 PM" in time_text:
        class_name = card.find_element(By.CSS_SELECTOR, "h3").text
        button = card.find_element(By.CSS_SELECTOR, "button")

        if button.text in ["Book Class", "Join Waitlist"]:
            retry(lambda: book(button), label="Booking")
            print(f"✓ Booked: {class_name} on {day_title}")
            booked_count += 1
            sleep(0.5)
        else:
            print(f"Already booked/waitlisted: {class_name}")

# -------------------- VERIFY BOOKINGS --------------------
def verify_bookings():
    driver.find_element(By.ID, "my-bookings-link").click()
    wait.until(EC.presence_of_element_located((By.ID, "my-bookings-page")))
    return driver.find_elements(By.CSS_SELECTOR, "div[id*='card-']")

bookings = retry(verify_bookings, label="Verify Bookings")

verified = sum(
    1 for slot in bookings
    if "6:00 PM" in slot.text and ("Tue" in slot.text or "Thu" in slot.text)
)

print("\n--- VERIFICATION ---")
print(f"Expected: {booked_count}")
print(f"Found: {verified}")
print("✅ SUCCESS" if booked_count == verified else "❌ MISMATCH")
