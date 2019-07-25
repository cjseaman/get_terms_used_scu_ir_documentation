import requests
from bs4 import BeautifulSoup



file = open('C:\\Users\\cseaman\\Desktop\\Tests\\anchors.html', 'r')
out_file = open('C:\\Users\\cseaman\\Desktop\\list_of_terms.txt', 'w')
disc_file = open('C:\\Users\\cseaman\\Desktop\\discrepancies.txt', 'w')
doc_soup = BeautifulSoup(file, "html.parser")

#print(doc_soup)
terms = ''
row_results = doc_soup.find_all('tr')

#print(row_results)
for row in row_results:
    unfiltered_rows = row
    unfiltered_row_soup = BeautifulSoup(unfiltered_rows.text, "html.parser")
    for r in unfiltered_row_soup:
        list_of_rows = BeautifulSoup(r, "html.parser")

 #       print(list_of_rows)
        list_of_fields = list_of_rows.text.split('\n')
        if len(list_of_fields) > 1:
            terms += (list_of_fields[1] + '\n')

terms_list = terms.split('\n')
terms_list[:] = [x for x in terms_list if x != '\xa0']
terms_list[:] = [x for x in terms_list if x != '']
# print(terms_list)
for t in terms_list:
    out_file.write(t+',')


url = "https://www.scu.edu/institutional-research/documentation/visualizations/"
headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.142 Safari/537.36'}

response = requests.get(url, headers=headers)
soup = BeautifulSoup(response.text, "html.parser")

doc_list_items = soup.find_all('ul', class_="list-group h4 p-3")

doc_links = []
for li in doc_list_items:
 #   print(li)
    li_soup = BeautifulSoup(str(li), "html.parser")
    link_l = li_soup.find_all('a')
    print(link_l)
    for link in link_l:
        link = link.get('href')
        doc_links.append('https://www.scu.edu/' + link)
        # print(link)

print(doc_links)
out = ''
for doc_link in doc_links:
    url = doc_link
 #   headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.142 Safari/537.36'}

    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, "html.parser")

    page_text = soup.find('div', class_="col-md-8").text
  #  print(page_text)

    out += 'Page: '
    out += url
    out += '\n'
    out += 'Terms included on this page: \n\n'
    for term in terms_list:
        if (page_text.find(term) != -1 or page_text.find(term + 's') != -1 or page_text.find(term[:-1]) != -1) and len(term) > 2:
            out += term
            out += '\n'
    out += '\n'

disc_file.write(out)


disc_file.close()
file.close()
out_file.close()


