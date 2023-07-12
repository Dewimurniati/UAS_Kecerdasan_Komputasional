# -*- coding: utf-8 -*-
"""Fuzzy_Logic.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1vZKipNDLZBxlJuoZx0RQhJtT7Yfj97fK

###- Impor library Pandas -
"""

import pandas as pd

"""###- Untuk impor data dari Google Drive -"""

import os
from google.colab import drive
drive.mount('/content/drive')

"""###- ini fungsi dari deklarasi cek nilai emosi pull source-"""

def checkEmotion(x):
    eLow, eMedium, eHigh = 0,0,0

    if x >= 0 and x <= 35:
        eLow    = 1

    elif x > 35 and x < 39:
        eLow    = (-1*((x-39)/(39-35)))
        eMedium = ((x-35)/(39-35))

    elif x >= 39 and x <= 61:
        eMedium = 1

    elif x > 61 and x <65:
        eMedium = (-1*((x-65)/(65-61)))
        eHigh   = ((x-61)/(65-1))

    elif x >= 65:
        eHigh   = 1

    return eLow, eMedium, eHigh

"""###- ini fungsi dari deklarasi cek nilai provokasi pull source -"""

def checkProvoke(x):
    pLow, pMedium, pHigh = 0,0,0

    if x >= 0 and x <= 55:
        pLow    = 1

    elif x > 55 and x < 60:
        pLow    = (-1*(x-60)/(60-55))
        pMedium = ((x-55)/(60-55))

    elif x >= 60 and x <= 85:
        pMedium = 1

    elif x > 85 and x < 87:
        pMedium = (-1*(x-87)/(82-87))
        pHigh   = ((x-85)/(87-85))

    elif x >= 87:
        pHigh   = 1

    return pLow, pMedium, pHigh

"""###- Fungsi deklarasi "inference" untuk menghitung nilai output fuzzy menggunakan kombinasi emosi dan provokasi menggunakan google colab -"""

def inference(eLow, eMedium, eHigh, pLow, pMedium, pHigh):
    Y1,Y2,Y3,Y4,Y5 = 0,0,0,0,0
    N1,N2,N3,N4 = 0,0,0,0
    Y,N = 0,0

    if eHigh != 0 and pHigh != 0:
        Y1 = min(eHigh,pHigh)

    if eHigh != 0 and pMedium != 0:
        Y2 = min(eHigh,pMedium)

    if eHigh != 0 and pLow != 0:
        N1 = min(eHigh,pLow)

    if eMedium != 0 and pHigh !=0:
        Y3 = min(eMedium,pHigh)

    if eMedium != 0 and pMedium != 0:
        N2 = min(eMedium,pMedium)

    if eMedium != 0 and pLow != 0:
        N3 = min(eMedium,pLow)

    if eLow != 0 and pHigh != 0:
        Y4 = min(eLow,pHigh)

    if eLow != 0 and pMedium != 0:
        Y5 = min(eLow,pMedium)

    if eLow != 0 and pLow != 0:
        N4 = min(eLow,pLow)

    Y = max(Y1,Y2,Y3,Y4,Y5)
    N = max(N1,N2,N3,N4)
    return Y,N

"""### - Deklarasi fungsi "defuzzification" untuk melakukan defuzzifikasi atau konversi nilai fuzzy menjadi nilai yang konkret dalam mengolah data yang ada -"""

def defuzzification(Y,N):
    if Y != 0 and N != 0:
        return ((Y*60)+(N*40))/(Y+N)
    elif Y != 0:
        return (Y*60)/Y
    elif N != 0:
        return (N*40)/N

"""### - Program utama yang digunakan  -"""

# Membaca file dari excel
data = pd.read_excel('drive/MyDrive/News.xlsx') # jalur file Excel

# Ekstrak value nilai dari excel
news = data['News'].tolist()
emotion = data['Emotion'].tolist()
provoke = data['Provoke'].tolist()

count = 0
while count < len(news):
    eLow, eMedium, eHigh = checkEmotion(emotion[count])
    pLow, pMedium, pHigh = checkProvoke(provoke[count])
    Ya, Tidak = inference(eLow, eMedium, eHigh, pLow, pMedium, pHigh)
    hasil = defuzzification(Ya, Tidak)
    if hasil < 55.0:
        hoax = "No"
    elif hasil >= 55.0:
        hoax = "Yes"
    print("News:", news[count], " Emotion:", emotion[count], " Provoke:", provoke[count], " Hoax:", hoax)

    count += 1

"""###**Kenapa data pada source code otomatis berubah jika data pada excell berubah?**

Data pada kode sumber akan otomatis berubah jika terjadi perubahan pada data di Excel karena kode tersebut mengambil data langsung dari file Excel setiap kali dieksekusi.
Karena kode tersebut selalu membaca data dari file Excel saat dijalankan, setiap kali ada perubahan pada file Excel, perubahan tersebut akan segera tercermin dalam kode sumber. Artinya, jika terdapat perubahan pada data di file Excel, saat kode dijalankan, data yang akan dibaca dan digunakan adalah data terbaru yang telah diperbarui.
Dengan cara ini, kode selalu mengakses data terbaru dari file Excel dan melakukan operasi berdasarkan data tersebut. Akibatnya, ketika data berubah, hasil yang dihasilkan oleh kode juga akan berubah sesuai dengan perubahan pada file Excel.


"""