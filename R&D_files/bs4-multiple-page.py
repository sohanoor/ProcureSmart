from bs4 import BeautifulSoup
import requests
import lxml

root = 'https://subslikescript.com'
website = f'{root}/movies_letter-A'  #?page=1
result = requests.get(website)
content = result.text
soup = BeautifulSoup(content, 'lxml')
# print(soup.prettify())

# pagination
pagination = soup.find('ul', class_='pagination')
pages = pagination.find_all('li', class_='page-item')

last_page = pages[-2].text

count = 0
error = 0
links = []
for page in range(1, int(last_page) + 1)[:2]:
    print(f'Page Count: {page}')
    print(f'{website}?page={page}')
    # https://subslikescript.com/movies_letter-A?page=1
    result = requests.get(f'{website}?page={page}')
    content = result.text
    soup = BeautifulSoup(content, 'lxml')

    box = soup.find('article', class_='main-article')
    try:
        get_link = box.find_all('a', href=True)
        for link in get_link:
            links.append(link['href'])
    except:
        print('could not find href')

    for link in links:
        try:
            result = requests.get(f'{root}/{link}')
            content = result.text
            soup = BeautifulSoup(content, 'lxml')

            box = soup.find('article', class_='main-article')

            title = box.find('h1').get_text()
            transcript = box.find('div', class_='full-script').get_text(strip=True, separator=' ')

            with open(f'{title}.txt', 'w') as file:
                file.write(transcript)
                count = count + 1
                print(f'{title} :: Success: {count}')
        except:
            error = error + 1
            # print(root + '/' + link)
            print(f'Error: {error} :: {root}/{link}')

print(f'Final Success Count: {count}')
print(f'Final Error Count: {error}')
