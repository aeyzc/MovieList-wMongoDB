import pymongo
from os import system
import random
import requests
from bs4 import BeautifulSoup

myclient=pymongo.MongoClient("yourDB")

mydb=myclient["movielist"]
users=mydb["users"]
logcontrol=1

while True:
    print(''' __ __            _        _    _        _   
|  \  \ ___  _ _ <_> ___  | |  <_> ___ _| |_ 
|     |/ . \| | || |/ ._> | |_ | |<_-<  | |  
|_|_|_|\___/|__/ |_|\___. |___||_|/__/  |_| 
                                   by aeyzc''')
    selectlogin=input("\n\n1-Giriş Yap\n2-Kayıt Ol\n3-Cıkıs")
    system("cls")
    if selectlogin=="1":
        username=input("kullanıcı adı:")
        password=input("Şifre:")

        filter={"username":username,"password":password}

        if filter not in users.find({},{"_id":0,"username":1,"password":1}):
            system("cls")
            print("Hatalı Giriş!")

    
        else:
            break



    
    
    elif selectlogin=="2":
        while True:
            username=input("kullanıcı adı:")
            if len(username)<6:
                print("kullanıcı adı en az 6 karakterden oluşmalıdır!")
            else:
                break

        while True:
            password=input("Şifre:")
            if len(password)<6:
                print("şifre en az 6 karakterden oluşmalıdır!")
            else:
                break
        
        users.insert_one({"username":username,"password":password})
        system("cls")
    
    else:
        logcontrol=0
        break
        

        
if logcontrol==0:
    username="a"



watched=mydb[username+"watched"]
todo=mydb[username+"todo"]


while True:
    if logcontrol==0:
        break
    system("cls")
    print(''' __ __            _        _    _        _   
|  \  \ ___  _ _ <_> ___  | |  <_> ___ _| |_ 
|     |/ . \| | || |/ ._> | |_ | |<_-<  | |  
|_|_|_|\___/|__/ |_|\___. |___||_|/__/  |_| 
                                   by aeyzc''')
    select=int(input('\n\nAktif Kullanıcı:'+username+'\n1-İzlenecek Filmler\n2-İzlediğim Filmler\n3-IMDb Menüsü\n4-Cıkıs'))
    system('cls')
    #ToDo List

    if select==1:
        selectToDoList=int(input('İZLENECEK FİLMLER\n\n1-İzlenecekler Listesini Göster\n2-Listeye Film Ekle\n3-Listeden Film Sil\n4-Rastgele Film Seç\n5-Ana Menüye Dön\n\n'))
        system('cls')
        if selectToDoList==1:
            print('İZLENİLECEKLER LİSTESİ\n')
            counter=1
            for i in todo.find():
                print(str(counter)+'-'+i["title"])
                counter+=1

        elif selectToDoList==2:
            eklenen=input('Ekleyeceğiniz Filmin İsmini Girin: ')
            todo.insert_one({"title":eklenen})
            print(eklenen+' Listenize Eklendi!')

        elif selectToDoList==3:
            try:
                deletingToDo=input('(LÜTFEN BÜYÜK KÜÇÜK HARFLERE DİKKAT EDİN!)\nSilinecek Filmin İsmini Girin: ')
                todo.delete_one({'title':deletingToDo})
            except Exception:
                print('Film Bulunamadı!')
            else:
                print(deletingToDo+' Listenizden Silindi!')

        elif selectToDoList==4:
            forand=[]
            forand.clear()
            for i in todo.find():
                forand.append(i["title"])
            randomMovie=random.choice(forand)
            print('Seçilen Film: '+randomMovie)

        elif selectToDoList==5:
            continue

        else:
            print('Hatalı Seçim Yaptınız!')
            continue

    #Watched List        

    if select==2:
        selectWatched=int(input('İZLEDİĞİM FİLMLER\n\n1-Eklenme Tarihine Göre Göster\n2-Puanıma Göre Göster\n3-Listeye Film Ekle\n4-Listeden Film Sil\n5-Ana Menüye Dön'))
        system('cls')
        if selectWatched==1:
            print('İZLEDİĞİM FİLMLER (EKLENME SIRASINA GÖRE)\n')
            counter=1
            for i in watched.find():
                print(str(counter)+"-"+i["title"]+" ("+str(i["points"])+")")
                counter+=1
                

        elif selectWatched==2:
            print('İZLEDİĞİM FİLMLER (PUANLARIMA GÖRE)\n')
            counter=1
            for i in watched.find().sort('points',-1):
                print(str(counter)+"-"+i["title"]+" ("+str(i["points"])+")")
                counter+=1

        elif selectWatched==3:
            while True:
                title=input('Ekleyeceğiniz Filmin Adını Girin: ')
                if len(title)<=1:
                    print('\nLütfen Geçerli Film İsmi Girin!\n')
                else:
                    break

            while True:
                try:
                    points=float(input('\nEkleyeceğiniz Filme Puanınızı Girin (Örn:4.2): '))
                    if (points>10 or points<0):
                        raise Exception('\nlütfen 0-10 arası sayı giriniz!\n')
                except Exception:
                    print('\nlütfen 0-10 arası sayı giriniz!\n')
                else:
                    break

            watched.insert_one({"title":title,"points":points})
            print(title+' Listenize Eklendi!')

        
        elif selectWatched==4:
            try:
                deleting=input('(LÜTFEN BÜYÜK KÜÇÜK HARFLERE DİKKAT EDİN!)\nLütfen Silinecek Filmin İsmini Girin: ')
                watched.delete_one({'title':deleting})
            except Exception:
                print('Film Bulunamadı!')
            else:
                print(deleting+' Listenizden Silindi!')

        elif selectWatched==5:
            continue
            
        else:
            print('Hatalı Seçim Yaptınız!')
            continue

    if select==3:
        selectimdb=input("IMDb MENUSU\n\n1-Top 50\n2-Popüler Filmler\n3-Cıkıs")
        system('cls')


        if selectimdb=='1' or selectimdb=='2':
            
            if selectimdb=='1':
                url="https://www.imdb.com/chart/top/?ref_=nv_mv_250"
                header='TOP 50'

            elif selectimdb=='2':
                url="https://www.imdb.com/chart/moviemeter/?ref_=nv_mv_mpm"
                header="POPÜLER FİLMLER"

            html =requests.get(url).content
            soup = BeautifulSoup(html,'html.parser')




            alist=soup.find('tbody',{"class":"lister-list"}).find_all('tr',limit=50)
            listmdb=[]


            i=1
            print("\n"+header+"\n")
            for tr in alist:
                listmdb.append(tr.find('td',{'class':'titleColumn'}).find('a').text)
                title = tr.find('td',{'class':'titleColumn'}).find('a').text
                print(str(i)+" - "+title)
                i+=1

        else:
            continue

    if select==4:
        break

    
    wait=input('\n1-Ana Menü\n2-Çıkış')
    system('cls')
    if wait=='2':
        break
    
