import pandas as pd

# CSV dosyasını oku
df = pd.read_csv("data/anket_sonuclari.csv")

print("İlk kayıt sayısı:", len(df))

# Tekrarlanan katılımcıları kaldır
df = df.drop_duplicates(subset=["Katılımcı No"])

# Sayısal sütunları sayıya dönüştür
sayisal_sutunlar = [
    "Yaş",
    "Memnuniyet (1-5)",
    "Hizmet Hızı (1-5)",
    "Personel İlgisi (1-5)",
    "Tavsiye (0-10)",
    "Bekleme (dk)",
    "Harcama (TL)"
]

for sutun in sayisal_sutunlar:
    df[sutun] = pd.to_numeric(df[sutun], errors="coerce")

# Geçersiz puanları boş olarak işaretle
puan_sutunlari = [
    "Memnuniyet (1-5)",
    "Hizmet Hızı (1-5)",
    "Personel İlgisi (1-5)"
]

for sutun in puan_sutunlari:
    df.loc[~df[sutun].between(1, 5), sutun] = None

df.loc[~df["Tavsiye (0-10)"].between(0, 10), "Tavsiye (0-10)"] = None

# Tarihleri düzenle
df["Tarih"] = pd.to_datetime(
    df["Tarih"],
    format="%d.%m.%Y",
    errors="coerce"
)

# Şehir isimlerini düzenle
import unicodedata

def sehir_duzenle(sehir):
    if pd.isna(sehir):
        return "Bilinmiyor"

    sehir = unicodedata.normalize("NFKD", str(sehir))
    sehir = "".join(
        karakter for karakter in sehir
        if not unicodedata.combining(karakter)
    )

    sehir = sehir.strip().casefold().replace("ı", "i")

    sehirler = {
        "istanbul": "İstanbul",
        "izmir": "İzmir",
        "bursa": "Bursa",
        "ankara": "Ankara",
        "antalya": "Antalya",
        "adana": "Adana",
        "kayseri": "Kayseri",
        "konya": "Konya"
    }

    return sehirler.get(sehir, sehir.title())


df["Şehir"] = df["Şehir"].apply(sehir_duzenle)

print("\n--- DÜZELTİLMİŞ ŞEHİRLER ---")
print(df["Şehir"].value_counts())

print("\n--- TEMİZLİK SONUCU ---")
print("Kalan katılımcı:", len(df))
print("\nEksik veriler:")
print(df.isnull().sum())

print("\nVeriler başarıyla temizlendi!")
# ==================================
# TEMEL İSTATİSTİKLER
# ==================================

print("\n========== ANKET ANALİZ RAPORU ==========")

# Toplam katılımcı
print("\nToplam katılımcı:", len(df))

# Ortalama memnuniyet
ortalama_memnuniyet = df["Memnuniyet (1-5)"].mean()
print("Ortalama memnuniyet:", round(ortalama_memnuniyet, 2))

# Ortalama bekleme süresi
ortalama_bekleme = df["Bekleme (dk)"].mean()
print("Ortalama bekleme süresi:", round(ortalama_bekleme, 2), "dakika")

# Ortalama tavsiye puanı
ortalama_tavsiye = df["Tavsiye (0-10)"].mean()
print("Ortalama tavsiye puanı:", round(ortalama_tavsiye, 2))


# ==================================
# ŞEHİR BAZINDA ANALİZ
# ==================================

print("\n========== ŞEHİR BAZINDA SONUÇLAR ==========")

sehir_ozeti = df.groupby("Şehir").agg(
    Katilimci_Sayisi=("Katılımcı No", "count"),
    Ortalama_Memnuniyet=("Memnuniyet (1-5)", "mean"),
    Ortalama_Bekleme=("Bekleme (dk)", "mean")
).round(2)

print(sehir_ozeti)


# ==================================
# TAVSİYE PUANI DAĞILIMI
# ==================================

print("\n========== TAVSİYE PUANI DAĞILIMI ==========")

tavsiye_dagilimi = df["Tavsiye (0-10)"].value_counts().sort_index()

print(tavsiye_dagilimi)


# ==================================
# MEMNUNİYET DAĞILIMI
# ==================================

print("\n========== MEMNUNİYET DAĞILIMI ==========")

memnuniyet_dagilimi = df["Memnuniyet (1-5)"].value_counts().sort_index()

print(memnuniyet_dagilimi)


print("\n========== ANALİZ TAMAMLANDI ==========")
# YAŞ GRUBUNA GÖRE MEMNUNİYET

df["Yaş Grubu"] = pd.cut(
    df["Yaş"],
    bins=[0, 18, 25, 35, 45, 55, 65, 100],
    labels=[
        "18 altı",
        "18-25",
        "26-35",
        "36-45",
        "46-55",
        "56-65",
        "65 üzeri"
    ]
)

print("\n--- YAŞ GRUBUNA GÖRE MEMNUNİYET ---")

yas_ozeti = df.groupby(
    "Yaş Grubu", observed=False
)["Memnuniyet (1-5)"].mean().round(2)

print(yas_ozeti)


# AYLARA GÖRE ANALİZ

df["Ay"] = df["Tarih"].dt.month

print("\n--- AYLARA GÖRE ANALİZ ---")

ay_ozeti = df.groupby("Ay").agg(
    Katilimci_Sayisi=("Katılımcı No", "count"),
    Ortalama_Memnuniyet=("Memnuniyet (1-5)", "mean")
).round(2)

print(ay_ozeti)