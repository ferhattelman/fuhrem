from django.shortcuts import render
from django.http import HttpResponse
# Create your views here.

def HomePage(request):
    return render(request, 'homePage.html')

def SearchPage(request):
    return render(request, 'searchPage.html')

def AboutPage(request):
    return render(request, 'aboutPage.html')

def ContactPage(request):
    return render(request, 'contactPage.html')

def ResultPage(request):
    return render(request, 'resultPage.html')

def LoadingPage(request):
    return render(request, 'loadingPage.html')


def getTitle ():
    import sqlite3

    conn = sqlite3.connect('db.sqlite3')
    cursor = conn.cursor()
    cursor.execute("SELECT title FROM app1_search_data GROUP BY title ORDER BY COUNT(title) DESC LIMIT 1;")
    value = cursor.fetchone()
    conn.close()
    return value


def getTags ():
    import sqlite3

    conn = sqlite3.connect('db.sqlite3')
    cursor = conn.cursor()
    cursor.execute("SELECT tag,COUNT(tag) FROM app1_search_data GROUP BY tag ORDER BY COUNT(tag) DESC LIMIT 50;")
    value = cursor.fetchall()
    conn.close()
    return value

def addToDatabase (veri_turu, value, title,  tags, arama_sayisi):
    import sqlite3
    from datetime import datetime
    conn = sqlite3.connect('db.sqlite3')
    cursor = conn.cursor()
    add_command = """INSERT INTO app1_search_history (image_type, value, title, tags, search_amount datetime) VALUES (?, ?, ?, ?, ?, ?);"""

    cursor.execute(add_command, (veri_turu, value, title, tags, arama_sayisi, datetime.now().replace(microsecond=0)))

    conn.commit()
    conn.close()

def pwSearch(request):
    try:   
        # verileri js'ten alıyoruz
        if request.method == 'POST':
            veri_turu = request.POST.get('veri_turu').lower()
            arama_sayisi = int(request.POST.get('arama_sayisi'))
            input_degeri = request.POST.get('input_degeri').lower()
        
        from playwright.sync_api import sync_playwright
        from bs4 import BeautifulSoup
        import sqlite3

        # veri tabanı bağlantısı ve veri tabanı komutları
        conn = sqlite3.connect('db.sqlite3')
        cursor = conn.cursor()
        cursor.execute("DELETE FROM app1_search_data;")
        cursor.execute("DELETE FROM sqlite_sequence WHERE name='app1_search_data';")
        add_command = """INSERT INTO app1_search_data (tag, title) VALUES (?, ?);"""

        with sync_playwright() as p:
            browser = p.chromium.launch(headless=False)
            context = browser.new_context()
            context.grant_permissions(['clipboard-read'])
            web_site = "https://www.shutterstock.com"
            
            # seçilen veri türüne göre url düzenlemesi 
            if veri_turu == "vector" or veri_turu =="photo" or veri_turu == "illustration":
                url = web_site + "/tr/search/" + input_degeri + "?image_type=" + veri_turu + "&page="
                populerlik = True
            elif veri_turu == "editorial image":
                url = web_site + "/tr/editorial/search/" + input_degeri
                populerlik = False
            elif veri_turu == "editorial video":
                populerlik = False
                url = web_site + "/tr/editorial/video/search/" + input_degeri
            elif veri_turu == "video":
                populerlik = False
                url = web_site + "/tr/video/search/" + input_degeri + "?page="

            page = context.new_page()
            i = 0
            sayfa_sayaci = 1
            page.goto(url + str(sayfa_sayaci))
            page.mouse.wheel(0, 10000)
            html = page.inner_html("div.mui-1nl4cpc-gridContainer-root")
            soup = BeautifulSoup(html,"html.parser")
            hrefs = [a['href'] for a in soup.find_all('a', href=True)]
            print(len(hrefs))

            while(arama_sayisi>0):
                if(i == len(hrefs)-1):
                    i = 0
                    sayfa_sayaci += 1
                    hrefs.clear()
                    page.goto(url + str(sayfa_sayaci))
                    page.mouse.wheel(0, 10000)
                    html = page.inner_html("div.mui-1nl4cpc-gridContainer-root")
                    soup = BeautifulSoup(html,"html.parser")
                    hrefs = [a['href'] for a in soup.find_all('a', href=True)]
                    print(len(hrefs))

                page.goto(web_site+hrefs[i])
                page.mouse.wheel(0, 1000)
                if (populerlik):
                    if page.is_visible("strong.mui-1isu8w6-empasis"):
                        durum = page.inner_html("strong.mui-1isu8w6-empasis")
                        if durum == "En iyi seçim!":
                            arama_sayisi -= 1
                            page.get_by_role("button", name="Anahtar sözcükleri panoya kopyalayın").click()
                            titles = page.inner_html(".mui-u28gw5-titleRow > h1").split(".")
                            filtered_titles = [title.strip() for title in titles if title.strip()]
                            tags = page.evaluate("navigator.clipboard.readText()").split(',')
                            for tag, title in zip(tags, filtered_titles):
                                cursor.execute(add_command, (tag.strip(), title.strip()))
                            for tag in tags[len(filtered_titles):]:
                                cursor.execute(add_command, (tag.strip(), None))
                else:
                    arama_sayisi -= 1
                    page.get_by_role("button", name="Anahtar sözcükleri panoya kopyalayın").click()
                    titles = page.inner_html(".mui-u28gw5-titleRow > h1").split(".")
                    filtered_titles = [title.strip() for title in titles if title.strip()]
                    tags = page.evaluate("navigator.clipboard.readText()").split(',')
                    for tag, title in zip(tags, filtered_titles):
                        cursor.execute(add_command, (tag.strip(), title.strip()))
                    for tag in tags[len(filtered_titles):]:
                        cursor.execute(add_command, (tag.strip(), None))
                i+=1
            browser.close()
            conn.commit()
            conn.close()

            title = getTitle()[0] if getTitle() else None
            tags_list = getTags()
            tags_str = ', '.join([tag[0] for tag in tags_list])
            addToDatabase(veri_turu, input_degeri, title, tags_str, arama_sayisi)  
        return HttpResponse("pwSearch fonksiyonu çalıştı!")
    except:
        return HttpResponse("pwSearch fonksiyonu hata verdi!")
