# FTE_SCRAPER
# 🔍 Job Scraper – Welcome to the Jungle (Playwright)

This project is an automated web scraper built using **Python + Playwright** to extract job listings data from the Welcome to the Jungle platform.

It performs **end-to-end scraping**, including:
- Handling popups
- Search automation
- Data extraction using DOM inspection
- Pagination traversal
- Data cleaning
- CSV export
- Analytical insights

---

## 🚀 Features

✅ Automated browser interaction using Playwright  
✅ Handles cookie & region popups  
✅ Searches for specific roles (e.g., "Business")  
✅ Extracts structured job data from dynamic React UI  
✅ Uses **DOM-based locators (no random guessing)**  
✅ Handles multi-page pagination  
✅ Cleans inconsistent data formats  
✅ Exports final dataset to CSV  
✅ Computes analytical metrics  

---

## 📊 Extracted Fields

The scraper collects the following fields:

- Job_Title  
- Company_Title  
- Company_Slogan  
- Job_Type  
- Location  
- Work_Location  
- Industry  
- Employes_Count  
- Posted_Ago  
- Job_Link  

---

## 🧠 Data Cleaning Logic

- Converts **"Yesterday" → "1 days ago"**
- Extracts numeric values from:
  - `"4,400 employees" → 4400`
- Handles:
  - Salary noise (e.g., `$75K`, `€3.7K`)
  - Missing fields
  - Variable data positions

---

## 🧪 Analytical Insights

The script automatically computes:

- Total number of jobs
- Jobs in New York
- Companies with:
  - More than 200 employees
  - Less than 200 employees
- Count of:
  - Permanent contracts
  - Internships

---

## 🛠 Tech Stack

- Python 🐍  
- Playwright 🎭  
- Regex (data cleaning)  
- CSV module  

---

## ⚙️ How to Run

### 1. Install dependencies

```bash
pip install playwright
playwright install
