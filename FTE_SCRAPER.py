from playwright.sync_api import sync_playwright
import re
import csv


URL = "https://www.welcometothejungle.com/en/jobs?refinementList%5Boffices.country_code%5D%5B%5D=US"


def extract_meta_value(card, alt_text):
    """
    Extracts metadata value (Job Type, Location, etc.) based on SVG icon alt text.
    """
    try:
        icon = card.locator(f"svg[alt='{alt_text}']").first
        if icon.count() == 0:
            return ""

        block = icon.locator("xpath=ancestor::div[@variant='default'][1]")
        text = block.inner_text().strip()

        parts = [x.strip() for x in text.split("\n") if x.strip()]
        return parts[0] if parts else ""

    except:
        return ""


def extract_card_data(card):
    """
    Extract structured job data from a single job card.
    """
    lines = [l.strip() for l in card.inner_text().split("\n") if l.strip()]

    # Base fields
    job_title = lines[0] if len(lines) > 0 else ""
    company = lines[1] if len(lines) > 1 else ""
    slogan = lines[2] if len(lines) > 2 else ""

    # Metadata using icon-based locators
    job_type = extract_meta_value(card, "Contract")
    location = extract_meta_value(card, "Location")
    work_location = extract_meta_value(card, "Remote")
    industry = extract_meta_value(card, "Tag")

    # Employees & Posted time (text-based parsing)
    employees = ""
    posted = ""

    for item in lines:
        low = item.lower()

        if not employees and "employees" in low:
            emp = re.findall(r"\d+", item.replace(",", ""))
            employees = emp[0] if emp else ""

        if not posted and (
            "minute" in low or "hour" in low or "day" in low or
            "week" in low or "month" in low or "year" in low or
            low in ["yesterday", "last week", "last month"]
        ):
            posted = item

    # Cleaning rule
    if posted.lower() == "yesterday":
        posted = "1 days ago"

    # Job link extraction
    try:
        href = card.locator("a[href]").nth(1).get_attribute("href")
        link = "https://www.welcometothejungle.com" + href if href else ""
    except:
        try:
            href = card.locator("a[href]").first.get_attribute("href")
            link = "https://www.welcometothejungle.com" + href if href else ""
        except:
            link = ""

    return {
        "Job_Title": job_title,
        "Company_Title": company,
        "Company_Slogan": slogan,
        "Job_Type": job_type,
        "Location": location,
        "Work_Location": work_location,
        "Industry": industry,
        "Employes_Count": employees,
        "Posted_Ago": posted,
        "Job_Link": link
    }


def run():
    all_jobs = []

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        page = browser.new_page()

        # Open target page
        page.goto(URL)
        page.wait_for_timeout(3000)

        # Handle region popup
        try:
            modal = page.locator("div[role='dialog']").first
            modal.wait_for(timeout=5000)
            modal.locator("button").filter(has=page.locator("svg")).first.click(force=True)
        except:
            pass

        # Perform search
        search_bar = page.locator("input[placeholder='Search by job, keyword, or company']")
        search_bar.wait_for(timeout=5000)
        search_bar.click()
        search_bar.fill("Business")
        search_bar.press("Enter")

        page.wait_for_timeout(5000)

        # Pagination loop
        while True:
            page.wait_for_selector("li[data-testid='search-results-list-item-wrapper']")

            cards = page.locator("li[data-testid='search-results-list-item-wrapper']")
            count = cards.count()

            for i in range(count):
                card = cards.nth(i)
                job_data = extract_card_data(card)
                all_jobs.append(job_data)

            # Check next button state
            next_btn = page.locator("a:has(svg[alt='Right'])")

            if next_btn.get_attribute("aria-disabled") == "true":
                break

            next_btn.click()
            page.wait_for_timeout(3000)

        browser.close()

    # Save results to CSV
    with open("results.csv", "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=all_jobs[0].keys())
        writer.writeheader()
        writer.writerows(all_jobs)

    # Analytical results
    total_jobs = len(all_jobs)

    jobs_in_new_york = sum(
        1 for job in all_jobs
        if job["Location"].strip().lower() == "new york"
    )

    more_than_200 = sum(
        1 for job in all_jobs
        if job["Employes_Count"].isdigit() and int(job["Employes_Count"]) > 200
    )

    less_than_200 = sum(
        1 for job in all_jobs
        if job["Employes_Count"].isdigit() and int(job["Employes_Count"]) < 200
    )

    permanent_contract = sum(
        1 for job in all_jobs
        if job["Job_Type"].strip().lower() == "permanent contract"
    )

    internship = sum(
        1 for job in all_jobs
        if job["Job_Type"].strip().lower() == "internship"
    )

    print("\n===== FINAL RESULTS =====")
    print(f"(a) Total jobs: {total_jobs}")
    print(f"(b) Jobs in New York: {jobs_in_new_york}")
    print(f"(c) >200 Employees: {more_than_200}")
    print(f"(d) <200 Employees: {less_than_200}")
    print(f"(e) Permanent Contract: {permanent_contract}")
    print(f"(f) Internship: {internship}")


if __name__ == "__main__":
    run()