import requests, bs4, time
s = requests.Session()
employer = "501713"
s.cookies.update({"employer" : employer,
                  "passwd[{}]".format(employer):"fuck"})
s.proxies = {}
s.proxies['http'] = 'socks5h://localhost:9050'
s.proxies['https'] = 'socks5h://localhost:9050'
for c in range(50):
    time.sleep(2)
    url1 = "https://www.domkadrov.ru/hrsearch.php?positioncode2={0}&city={1}".format(employer, str(936 + c))
    print("city ",c)
    for i in range(50):
        time.sleep(20)
        print("page ", i)
        url = url1 + "&z=" + str(i)
        page = s.get(url)
        page_parser = bs4.BeautifulSoup(page.text, "html.parser")
        row1 = page_parser.findAll("tr", {"class": "row1"})
        rowt2 = page_parser.findAll("tr", {"class": "row2t"})
        rows = row1 + rowt2
        if(len(rows) == 0):
            break
        for row in rows:
            time.sleep(20)
            link = row.findAll("a")[0]
            print("https://www.domkadrov.ru/" + link.attrs['href'])
            resume = s.get("https://www.domkadrov.ru/" + link.attrs['href'])
            resume_parser = bs4.BeautifulSoup(resume.text, "html.parser")
            fio = resume_parser.title.text
            info = resume_parser.findAll("td")
            data = None
            for td in info:
              if(len(td.text) < 20 and len(td.text.split()) == 3 and td.text.split()[2].isdigit()):
                 data = td.text
                 break
            if(data is None):
              continue 
            city = resume_parser.findAll("div", {"class": "test3"})
            if(len(city) == 2):
               city = city[1].text
            else:
               continue
            tds = resume_parser.findAll("td", {"valign": "top"})
            if(len(tds) < 9):
                continue
            phone = tds[9].text
            print(data, city)
            if(len(fio.split()) == 3):
                flink = "https://www.domkadrov.ru/" + link.attrs['href']
                f = open("tels/kzdomk.txt", 'a')
                f.write(fio.encode('utf-8') + '#' + phone.encode('utf-8') + '#' + data.encode('utf-8') + '#' + city.encode('utf-8') + '#' + flink.encode('utf-8')  + '\n\n')
                f.close()






'''
page = s.get("https://www.domkadrov.ru/hrcandcv.php?searchfor=%C0%E7%ED%E0%EA%E0%E5%E2%EE&positioncode2=498537&id=1434579&button=positioncode2%3D498537%26city%3D15%26z%3D2")
parser = bs4.BeautifulSoup(page.text, "html.parser")
print(parser.title)
tds = parser.findAll("td", {"valign":"top"})
print(tds[9])
'''
