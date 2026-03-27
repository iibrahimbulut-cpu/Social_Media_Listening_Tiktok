import time
import random
import pandas as pd
import re
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from webdriver_manager.chrome import ChromeDriverManager

def html_icinden_izlenme_bul(html_kodu):
    """
    Selenium'un getiremediği veriyi, HTML kodunun içinden
    Regex ile zorla söküp alır.
    Aranan desenler: >1.2M<, >500.5K<, "1.2M" vb.
    """
    desen = r'>(\d+(\.\d+)?[KMB])<'
    bulunan = re.search(desen, html_kodu)
    
    if bulunan:
        return bulunan.group(1) # Sadece sayıyı döndür (örn: 1.2M)
    
    desen2 = r'"(\d+(\.\d+)?[KMB])"'
    bulunan2 = re.search(desen2, html_kodu)
    
    if bulunan2:
        return bulunan2.group(1)
        
    return "Bilinmiyor"

def captcha_kontrol(driver):
    try:
        if "captcha" in driver.page_source.lower() or "verify" in driver.page_source.lower():
            print("\n🔴 CAPTCHA TESPİT EDİLDİ! Lütfen elle çözüp buraya gelip ENTER'a bas.")
            input("✅ Devam etmek için ENTER...")
            time.sleep(3)
    except:
        pass

def toplu_tiktok_analiz(yemek_listesi, kaydirma_sayisi=3):
    options = webdriver.ChromeOptions()
    options.add_argument("--start-maximized")
    options.add_argument("--disable-notifications")
    options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.212 Safari/537.36")
    
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    tum_veriler = [] 
    
    try:
        for yemek in yemek_listesi:
            print(f"\n==========================================")
            print(f"🌍 Taranıyor: {yemek.upper()}")
            print(f"==========================================")
            
            url = f"https://www.tiktok.com/tag/{yemek}"
            driver.get(url)
            time.sleep(5)
            captcha_kontrol(driver)
            
            for i in range(kaydirma_sayisi):
                print(f"   ⬇️ {yemek} ({i+1}/{kaydirma_sayisi}) kaydırılıyor...")
                driver.find_element(By.TAG_NAME, 'body').send_keys(Keys.END)
                time.sleep(random.uniform(3, 6))
                if i % 2 == 0: captcha_kontrol(driver)
            
            print(f"   🔍 {yemek} HTML kodları taranıyor...")
            
            video_kutulari = driver.find_elements(By.XPATH, "//div[contains(@class, 'DivItemContainer')]")
            
            if len(video_kutulari) > 0:
                print(f"\n🐛 DEBUG (HTML Kodu): İlk videonun içinde 'M' veya 'K' harfi var mı?")
                ilk_html = video_kutulari[0].get_attribute('innerHTML')
                if "M<" in ilk_html or "K<" in ilk_html:
                    print("✅ EVET! HTML içinde sayılar gizli, çekebiliriz.")
                else:
                    print("⚠️ UYARI: HTML içinde de sayı görünmüyor. TikTok yapıyı değiştirmiş olabilir.")
            
            sayac = 0
            for kutu in video_kutulari:
                try:
                    html_kodu = kutu.get_attribute('innerHTML')
                    
                    izlenme = html_icinden_izlenme_bul(html_kodu)
                    
                    aciklama = kutu.text.replace("\n", " ").strip()
                    
                    if izlenme != "Bilinmiyor":
                        aciklama = aciklama.replace(izlenme, "").strip()

                    if len(aciklama) > 3:
                        tum_veriler.append({
                            "Kategori": yemek,
                            "İzlenme (Ham)": izlenme,
                            "Video Açıklaması": aciklama[:200] # Çok uzunsa kırp
                        })
                        sayac += 1
                except:
                    continue
            
            print(f"   ✅ {yemek} için {sayac} veri çekildi.")
            time.sleep(4)

        if len(tum_veriler) > 0:
            df = pd.DataFrame(tum_veriler)
            
            def cevir(x):
                if x == "Bilinmiyor": return 0
                x = x.replace(',', '.')
                carpan = 1
                if 'K' in x: carpan = 1000
                elif 'M' in x: carpan = 1000000
                elif 'B' in x: carpan = 1000000000
                
                temiz = re.sub(r'[^\d.]', '', x)
                try:
                    return int(float(temiz) * carpan)
                except:
                    return 0

            df["İzlenme (Sayısal)"] = df["İzlenme (Ham)"].apply(cevir)
            df = df.sort_values(by="İzlenme (Sayısal)", ascending=False)
            
            dosya_adi = "tiktok_final_html.xlsx"
            df.to_excel(dosya_adi, index=False)
            print(f"\n🎉 DOSYA HAZIR: {dosya_adi}")
            print(df[["Kategori", "İzlenme (Ham)", "Video Açıklaması"]].head(5)) # İlk 5'i ekrana bas
        else:
            print("❌ Hiç veri çekilemedi.")

    except Exception as e:
        print(f"❌ Hata: {e}")
    finally:
        driver.quit()

aranacaklar = [
    "keyword1",
    "key word2"
]

toplu_tiktok_analiz(aranacaklar, kaydirma_sayisi=3)