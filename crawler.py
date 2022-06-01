import re
import urllib
from bs4 import BeautifulSoup


def main():
    baseurl = "https://movie.douban.com/top250?start="
    #
    # datalist = getData(baseurl);
    #
    # savepath = ".\\豆瓣电影Top250.xls"
    #
    # saveData(savepath)
    getData(baseurl)


findLink = re.compile(r'<a href="(.*?)">')
findImgSrc = re.compile(r'img.*src=(.*?)"',re.S)
findTitle = re.compile(r'<span class="title">(.*)</span>')
findRating = re.compile(r'<span class="rating_num" property="v:average">(.*)</span>')
findJudge = re.compile(r'<span>(\d*)人评价</span>')
findInq = re.compile(r'<span class="inq">(.*)</span>')
findBd = re.compile(r'<p class="">(.*)</p>',re.S)


def getData(baseurl):
    datalist = []
    for i in range(0,1):
        url = baseurl + str(i*25)
        html = askURL(url)
        soup = BeautifulSoup(html,"html.parser")
        for item in soup.find_all('div',class_="item"):
            data = []
            item = str(item)

            link = re.findall(findLink,item)[0]
            data.append(link)
            imgSrc = re.findall(findImgSrc,item)[0]
            data.append(imgSrc)
            titles = re.findall(findTitle,item)
            if(len(titles) == 2):
                ctitle = titles[0]
                data.append(ctitle)
                otitle = titles[1].replace("/","")
                data.append(otitle)
            else:
                data.append(titles[0])
                data.append(' ')
            rating = re.findall(findRating,item)[0]
            data.append(rating)
            judge = re.findall(findJudge,item)[0]
            data.append(judge)

            inq = re.findall(findInq,item)
            if(len(inq)!=0):
                inq = inq[0].replace("。","")
                data.append(inq)
            else:
                data.append(" ")

            bd = re.findall(findBd,item)[0]
            bd = re.sub("<br(\s+)?/>(\s+)?"," ",bd)
            bd = re.sub("/"," ",bd)
            data.append(bd.strip())
            datalist.append(data)

    print(datalist)
    return datalist



def saveData(savepath):
    print()


def askURL(url):
    head = {
        "User-Agent": "Mozilla/5.0(WindowsNT10.0;Win64;x64) AppleWebKit / 537.36(KHTML, likeGecko) Chrome / 101.0.4951.64Safari / 537.36Edg / 101.0.1210.53"

    }
    request = urllib.request.Request(url, headers=head)
    html = ""
    try:
        response = urllib.request.urlopen(request)
        html = response.read().decode("utf-8")
        # print(html)
    except urllib.error.URLError as e:
        if hasattr(e, "code"):
            print(e.code)

    return html


if __name__ == main():
    main()
