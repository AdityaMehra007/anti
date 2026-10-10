import urllib.request
from bs4 import BeautifulSoup
import re

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36',
    'Referer': 'https://jobspresso.co/remote-work/'
}

urls = [
    'https://jobspresso.co/job/technical-customer-support-l1/',
    'https://jobspresso.co/job/senior-product-manager-data/',
    'https://jobspresso.co/job/executive-assistant-11/',
    'https://jobspresso.co/job/technical-support-specialist-apac/'
]

for url in urls:
    req = urllib.request.Request(url, headers=headers)
    try:
        with urllib.request.urlopen(req, timeout=15) as resp:
            soup = BeautifulSoup(resp.read().decode('utf-8'), 'html.parser')
            title = soup.find('h1', class_='page-title').get_text(strip=True) if soup.find('h1', class_='page-title') else 'N/A'
            company = soup.find('div', class_='job-company') or soup.find('h2', class_='company-name')
            comp_name = company.get_text(strip=True) if company else 'N/A'
            
            # Application link / button
            app_btn = soup.find('a', class_='application_button_link') or soup.find('input', class_='application_button') or soup.find('a', class_='job_application_email')
            app_url = app_btn['href'] if app_btn and 'href' in app_btn.attrs else 'N/A'
            
            # Application details / modal
            app_details = soup.find('div', class_='application_details')
            if app_details:
                link_inside = app_details.find('a')
                if link_inside and 'href' in link_inside.attrs:
                    app_url = link_inside['href']
                text_inside = app_details.get_text(strip=True)
            else:
                text_inside = 'N/A'
                
            print(f"\nURL: {url}")
            print(f"Title: {title}")
            print(f"Company: {comp_name}")
            print(f"Direct Apply URL: {app_url}")
            print(f"Apply text snippet: {text_inside[:150]}")
    except Exception as e:
        print(f"Error for {url}: {e}")
