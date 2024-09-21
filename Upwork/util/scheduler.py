from Upwork.util.link import extract_links
from Upwork.scraper import fetch_page_content, extract_job_info


def job_data_extract(url):

    url_list: list = extract_links(url)
    for url in url_list:
        print(f"Job Info for URL: {url}")
        page_content = fetch_page_content(url)
        job_info = extract_job_info(page_content, url)
        print(job_info)
        print("\n" + "=" * 80 + "\n")
