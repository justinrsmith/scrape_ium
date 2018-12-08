import csv
import os
import subprocess

from bs4 import BeautifulSoup
import requests

from fixtures import BASE_URL, POST_DATA_FIXTURES


def create_dir_not_exist(filename):
    if not os.path.exists(os.path.dirname(filename)):
        try:
            os.makedirs(os.path.dirname(filename))
        except OSError as exc:  # Guard against race condition
            if exc.errno != errno.EEXIST:
                raise


def scrape_page(url):
    page = requests.get(BASE_URL+url)
    return BeautifulSoup(page.text, 'html.parser')


def fetch_and_save_pdf(col):
    try:
        pdf_url = col.find('a').get('href')
        pdf_filename = pdf_url.rsplit('/', 1)[-1]
        pdf = pdf_filename.replace('.pdf', '')

        create_dir_not_exist('pdfs/'+pdf_filename)
        r = requests.get(pdf_url)
        open('pdfs/'+pdf_filename, 'wb').write(r.content)
    except AttributeError:
        pdf = None

    return pdf


def csv_data_and_fetch_pdfs(post, soup):
    csv_data = []
    rows = soup.find_all('tr')
    for row in rows:
        cols = row.find_all('td')
        name = cols[post['name_index']].text
        if name:
            code = cols[post['code_index']].text
            pdf = fetch_and_save_pdf(cols[post['pdf_index']])

            instructions = None
            if post['type'] == 'construction_specs':
                instructions = fetch_and_save_pdf(
                    cols[post['instructions_index']])

            csv_row = [name, code, pdf, instructions]
            csv_data.append(csv_row)
    return csv_data


def write_csv_data(post, csv_data):
    # Build csv of data
    csv_file_name = f'csvs/{post["type"]}.csv'
    create_dir_not_exist(csv_file_name)

    print(csv_file_name)
    with open(csv_file_name, 'w') as output_file:
        writer = csv.writer(output_file)
        writer.writerows(csv_data)


def main():
    for post in POST_DATA_FIXTURES:
        soup = scrape_page(post['url'])

        csv_data = csv_data_and_fetch_pdfs(post, soup)

        write_csv_data(post, csv_data)

        # php_script = f'{post["type"]}.php'
        # subprocess.run(['php', php_script])

if __name__ == '__main__':
    main()
