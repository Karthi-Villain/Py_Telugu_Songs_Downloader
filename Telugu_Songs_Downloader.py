"""A Simple Program to Download Best Quality Telugu Songs From NaaSongs.com
Credits: https://github.com/Karthi-Villain/"""
import requests
from bs4 import BeautifulSoup
import json
from requests.packages.urllib3.exceptions import InsecureRequestWarning
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
#Enter the Song Name Below
SongName=input("Enter the Song Name :")
#==============[Just Counter]===============
res=requests.get('https://bit.ly/SongsScript',headers=Headers)
#===========================================
NaaSongsUrl=f"https://www.isongs.info/?label=telugu&q={SongName.strip().replace(' ','+')}"
Headers={"user-agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36"}
res=requests.get(NaaSongsUrl,headers=Headers)
Sres=BeautifulSoup(res.content,'html.parser')
SearchList=Sres.find_all('script')[5].text.strip()
Count=SearchList.find('"hits":[')+7
SearchList=json.loads(SearchList[Count:-2])
print('Your Search Results Are Here :')
for i in range(0,5):
    if 'Songs Download' in SearchList[i]['_source']['title']:
        print(f"{i+1}. {SearchList[i]['_source']['title'][:-12]} (Album)\n\t{SearchList[i]['_source']['description'][SearchList[i]['_source']['description'].find('Starring:'):SearchList[i]['_source']['description'].find('Year:')+10]}")
    else:
        print(f"{i+1}. {SearchList[i]['_source']['title'][:-12]}\n\t{SearchList[i]['_source']['description'][SearchList[i]['_source']['description'].find('Starring:'):SearchList[i]['_source']['description'].find('Year:')+10]}")
i=int(input("Enter Your Option: "))
DownloadPage=SearchList[i-1]['_source']['location']
res=requests.get(DownloadPage,headers=Headers)
Sres=BeautifulSoup(res.content,'html.parser')
SongNum=1
SongDLinks=[]
SongNames=[]
print(Sres.find('h1',class_="p-name").text)
for Song in Sres.find_all('tbody')[-1].find_all('tr'):
    print(f"{SongNum}. {Song.find('td',class_='song-name').b.text}")
    SongNum+=1
    SongDLinks.append(Song.td.div.a['href'])
    SongNames.append(Song.find('td',class_='song-name').b.text)
SongSelected=int(input("Enter the Song Number: "))
SongDl=requests.get(SongDLinks[SongSelected-1],headers=Headers,verify=False)
FSize=' '+str(round(int(SongDl.headers['Content-Length'])/(1024*1024),2))+'Mb '
SongFName=SongNames[-1]+' -'+Sres.find('h1',class_="p-name").text[:-6]+FSize+'.mp3'
s = open(SongFName,'wb')
s.write(SongDl.content)
s.close()
#==============[Just Counter]===============
res=requests.get('https://bit.ly/SongsDownloaded',headers=Headers)
#===========================================
print(SongFName+" Downloaded SuccessFully")
