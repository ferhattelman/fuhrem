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

def pwSearch(request):
    try:   
        if request.method == 'POST':
            veri_turu = request.POST.get('veri_turu').lower()
            arama_sayisi = int(request.POST.get('arama_sayisi'))
            input_degeri = request.POST.get('input_degeri').lower()
        
        from playwright.sync_api import sync_playwright
        from bs4 import BeautifulSoup
        import sqlite3

        conn = sqlite3.connect('deneme.db')
        cursor = conn.cursor()

        cursor.execute("DROP TABLE IF EXISTS tagler")
        cursor.execute("CREATE TABLE tagler(tag text)")
        add_command = """INSERT INTO tagler VALUES(?)"""

        with sync_playwright() as p:
            browser = p.chromium.launch(headless=False)
            context = browser.new_context()
            context.grant_permissions(['clipboard-read'])
            web_site = "https://www.shutterstock.com"

            if veri_turu == "vector" or veri_turu =="photo" or veri_turu == "illustration":
                url = web_site + "/tr/search/" + input_degeri + "?image_type=" + veri_turu
            elif veri_turu == "editorial image":
                url = web_site + "/tr/editorial/search/" + input_degeri
            elif veri_turu == "editorial video":
                url = web_site + "/tr/editorial/video/search/" + input_degeri
            elif veri_turu == "video":
                url = web_site + "/tr/video/search/" + input_degeri

            page = context.new_page()
            page.goto(url)
            page.mouse.wheel(0, 10000)
            html = page.inner_html("div.mui-1nl4cpc-gridContainer-root")
            soup = BeautifulSoup(html,"html.parser")
            hrefs = [a['href'] for a in soup.find_all('a', href=True)]
            print(len(hrefs))
            for i in range(arama_sayisi):
                page.goto(web_site+hrefs[i])
                page.mouse.wheel(0, 1000)
                durum = page.inner_html("strong.mui-1isu8w6-empasis")
                if durum == "En iyi seçim!":
                    page.get_by_role("button", name="Anahtar sözcükleri panoya kopyalayın").click()
                    title = page.inner_html(".mui-u28gw5-titleRow > h1")
                    datas = page.evaluate("navigator.clipboard.readText()").split(',')
                    for data in datas:
                        cursor.execute(add_command,(data.strip(),))
                    #print(title)
            browser.close()
            conn.commit()
            conn.close()
        return HttpResponse("pwSearch fonksiyonu çalıştı!")
    except:
        return HttpResponse("pwSearch fonksiyonu çalıştı!")