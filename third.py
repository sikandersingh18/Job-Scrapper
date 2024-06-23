import requests
from bs4 import BeautifulSoup

def scrape_indeed(job_title, location):
    """
    Scrapes job listings from Indeed.com.

    Args:
        job_title (str): The job title to search for.
        location (str): The location to search in.

    Returns:
        list: A list of dictionaries, where each dictionary represents a job listing.
    """

    base_url = "https://www.indeed.com/jobs"
    params = {
        "q": job_title,
        "l": location
    }

    jobs = []
    while True:
        response = requests.get(base_url, params=params)
        soup = BeautifulSoup(response.content, "html.parser")

        job_cards = soup.find_all("div", class_="job_seen_beacon")
        for card in job_cards:
            title = card.find("h2", class_="jobTitle").text.strip()
            company = card.find("span", class_="companyName").text.strip()
            location = card.find("div", class_="companyLocation").text.strip()

            jobs.append({
                "title": title,
                "company": company,
                "location": location
            })

        # Check for next page
        next_page_link = soup.find("a", {"aria-label": "Next"})
        if next_page_link:
            next_page_url = "https://www.indeed.com" + next_page_link["href"]
            base_url = next_page_url
            params = {}  # Clear params for subsequent pages
        else:
            break  # No more pages

    return jobs

# Get user input for job title and location
job_title = input("Enter the job title you want to search for: ")
location = input("Enter the location you want to search in: ")

jobs = scrape_indeed(job_title, location)

# Print the scraped job listings
if jobs:
    print("\nFound job listings:")
    for job in jobs:
        print(f"- {job['title']} at {job['company']} ({job['location']})")
else:
    print("No job listings found.")