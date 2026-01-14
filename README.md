# Gym-Class-Auto-Booker-Selenium-Automation-
This project automates the repetitive task of booking gym classes. It logs in securely, scans available class cards, filters classes by day, performs bookings or waitlist actions when available, and finally verifies the bookings. 


🚀 Features

🔐 Automated login using Selenium

🕒 Filters classes by day and time

🖱️ Automatically books or waitlists classes

🔁 Retry mechanism for unstable UI interactions

📋 Booking verification after submission

📊 Final booking summary with validation

🧠 Handles dynamic content & stale elements safely

🛠️ Tech Stack

Python 3

Selenium WebDriver

ChromeDriver

Explicit waits (WebDriverWait)

Retry & exception handling

📂 Project Structure
gym-class-auto-booker/
│
├── main.py        # Core automation logic
├── README.md      # Project documentation

▶️ How It Works (Flow)

Launch Chrome with a persistent user profile

Log in to the gym portal

Scan all class cards on the schedule

Filter classes:

Tuesday or Thursday

6:00 PM slot

Book / join waitlist if available

Navigate to “My Bookings”

Verify bookings

Print final success or mismatch summary

⚠️ Important Notes

Uses explicit waits to avoid flaky behavior

Handles dynamic DOM re-rendering

Retry logic prevents failures due to slow UI updates

For educational and personal automation use only

🔮 Future Enhancements

Date range selection

Notification (Email / WhatsApp)

Headless execution

Configurable class preferences

Logging & screenshots on failure

👨‍💻 Author

Sudharson S
Python Developer | Automation Enthusiast
