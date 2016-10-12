import urllib.request as ur, os, re, html

def go():
    for n in range(1227, 1628):
        url = 'http://rg-vestnik.ru/statia/' + str(n)
        get_html(url, n)

def get_html(url, n):
    page = ur.urlopen(url)
    text = page.read().decode('windows-1251')
    reading(url, n, text)

def reading(url, n, text):
    text = text.replace('&nbsp;','')
    res = re.search('class="zagolovok"><h1>(.*?)</h1>', text, flags=re.DOTALL)
    if res:
        header = res.group(1)
    res = re.search('Вернуться в раздел: <b>(.*?)</b>', text, flags=re.DOTALL)
    if res:
        category = res.group(1)
    res = re.search('Автор: (.*?)\| (.*?)<', text, flags=re.DOTALL)
    if res:
        author = res.group(1)
        date = clean_date(res.group(2))
    res = re.search('class="text">(.*?)</div>', text, flags=re.DOTALL)
    if res:
        article = clean_article(res.group(1))
    put_data(url, n, author, header, date, category, article)
#столько if res, потому что иначе, к сожалению, почему-то не работает (

def clean_article(article):
    regTag = re.compile('<.*?>', flags=re.U | re.DOTALL)
    regN = re.compile('\\n\\r(\\n\\r)*', flags=re.U | re.DOTALL)
    article = regTag.sub("", article)
    article = regN.sub("", article)
    return article

def clean_date(date):
    arr = list(date)
    date = arr[0] + arr[1] + '.' + arr[3] + arr[4] + '.' + arr[6] + arr[7] + arr[8] + arr[9]
    return date
    
def put_data(url, n, author, header, date, category, article):
    write_csv(url, n, author, header, date, category)
    write_plain(url, n, author, header, date, category, article)
    write_ms_plain(n, date, article)
    write_ms_xml(n, date)

def write_plain(url, n, author, header, date, category, article):
    if not os.path.exists(path_plain(date, n)):
        os.makedirs(path_plain(date, n))
    file = open(path_plain(date, n) + '/' + str(n) + '.txt', 'w', encoding='utf-8')
    string = '@au ' + author + '\n@ti ' + header + '\n@da ' + date + '\n@topic ' + category + '\n@url ' + url + '\n' + article
    file.write(string)
    file.close()

def write_ms_plain(n, date, article):
    if not os.path.exists(path_ms_plain(date, n)):
        os.makedirs(path_ms_plain(date, n))
    file = open(path_ms_plain(date, n) + '/' + str(n) + '.txt', 'w', encoding='utf-8')
    file.close()
    os.system('./mystem -cdi ' + path_plain(date, n) + '/' + str(n) + '.txt' + ' ' + path_ms_plain(date, n) + '/' + str(n) + '.txt')
    file = open(path_ms_plain(date, n) + '/' + str(n) + '.txt', 'r', encoding='utf-8')
    txt = file.read()
    file.close()
    regA = re.compile('\@(.*?)\\n', flags=re.U | re.DOTALL)
    txt = regA.sub('', txt)
    file = open(path_ms_plain(date, n) + '/' + str(n) + '.txt', 'w', encoding='utf-8')
    file.write(txt)
    file.close()

def write_ms_xml(n, date):
    if not os.path.exists(path_ms_xml(date, n)):
        os.makedirs(path_ms_xml(date, n))
    file = open(path_ms_plain(date, n) + '/' + str(n) + '.txt', 'r', encoding='utf-8')
    txt = file.read()
    file.close()
    file = open(path_ms_xml(date, n) + '/' + str(n) + '.xml', 'w', encoding='utf-8')
    file.write(txt)
    file.close()

def write_csv(url, n, author, header, date, category):
    path = path_plain(date, n)
    row = '%s\t%s\t\t\t%s\t%s\tпублицистика\t\t\t%s\t\tнейтральный\tн-возраст\tн-уровень\tрайонная\t%s\tВестник Газета Брасовского района Брянской области\t\t%s\tгазета\tРоссия\tБрянская область\tru\n'
    string = row % (path, author, header, date, category, url, year(date))
    if not os.path.exists('газета'):
        os.makedirs('газета')
    file = open('газета/metadata.csv', 'a', encoding='utf-8')
    file.write(string)
    file.close()

def year(date):
    arr = list(date)
    year = arr[6] + arr[7] + arr[8] + arr[9]
    return year

def month(date):
    arr = list(date)
    month = arr[3] + arr[4]
    return month

def path_plain(date, n):
    path = os.getcwd() + '/газета/plain/' + year(date) + '/' + month(date)
    return path

def path_ms_plain(date, n):
    path = os.getcwd() + '/газета/mystem-plain/' + year(date) + '/' + month(date)
    return path

def path_ms_xml(date, n):
    path = os.getcwd() + '/газета/mystem-xml/' + year(date) + '/' + month(date)
    return path

if __name__ == '__main__':
    go()
