import pandas as pd
import json

# Temizlenmiş verileri main.py dosyasından al
from main import df

print("Rapor için veriler başarıyla alındı!")
print("Toplam katılımcı:", len(df))
print("Şehir sayısı:", df["Şehir"].nunique())
# Verileri HTML dosyasina aktarilabilecek hale getir
veriler = df.to_json(
    orient="records",
    force_ascii=False,
    date_format="iso"
)

# HTML raporunu oluştur
html_icerik = """
<!DOCTYPE html>
<html lang="tr">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Anket Sonuçları Analiz Raporu</title>

    <style>
        body {
            font-family: Arial, sans-serif;
            background: #f3f4f6;
            margin: 0;
            padding: 30px;
            color: #222;
        }

        h1 {
            text-align: center;
        }

        .kartlar {
            display: flex;
            gap: 20px;
            justify-content: center;
            flex-wrap: wrap;
            margin: 30px 0;
        }

        .kart {
            background: white;
            padding: 25px;
            border-radius: 12px;
            min-width: 180px;
            text-align: center;
            box-shadow: 0 2px 8px #0001;
        }

        .kart h2 {
            color: #2563eb;
        }

        select {
            display: block;
            margin: 20px auto;
            padding: 12px;
            border-radius: 8px;
            font-size: 16px;
        }
    </style>
    <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
</head>

<body>

    <h1>Anket Sonuçları Analiz Raporu</h1>

    <select id="sehirFiltresi">
        <option value="Tümü">Tüm Şehirler</option>
    </select>

    <div class="kartlar">
        <div class="kart">
            <h3>Katılımcı Sayısı</h3>
            <h2 id="katilimci">0</h2>
        </div>

        <div class="kart">
            <h3>Ortalama Memnuniyet</h3>
            <h2 id="memnuniyet">0</h2>
        </div>

        <div class="kart">
            <h3>Ortalama Bekleme</h3>
            <h2 id="bekleme">0</h2>
        </div>

        <div class="kart">
            <h3>Ortalama Tavsiye</h3>
            <h2 id="tavsiye">0</h2>
        </div>
    </div>
<h2 style="text-align:center; margin-top:40px;">
    Detaylı Anket Analizleri
</h2>

<div style="
    display:grid;
    grid-template-columns:repeat(auto-fit, minmax(350px, 1fr));
    gap:25px;
    margin-top:30px;
">

    <div class="kart">
        <h3>Memnuniyet Dağılımı</h3>
        <canvas id="memnuniyetGrafik"></canvas>
    </div>

    <div class="kart">
        <h3>Tavsiye Puanı Dağılımı</h3>
        <canvas id="tavsiyeGrafik"></canvas>
    </div>

    <div class="kart">
        <h3>Bekleme Süresi Dağılımı</h3>
        <canvas id="beklemeGrafik"></canvas>
    </div>

    <div class="kart">
        <h3>Şehirlere Göre Memnuniyet</h3>
        <canvas id="sehirGrafik"></canvas>
    </div>

    <div class="kart">
        <h3>Yaş Gruplarına Göre Memnuniyet</h3>
        <canvas id="yasGrafik"></canvas>
    </div>

    <div class="kart">
        <h3>Aylara Göre Katılımcı Sayısı</h3>
        <canvas id="ayGrafik"></canvas>
    </div>

</div>


<!-- Sehir tablosu -->
<div class="kart" style="margin-top:30px; overflow-x:auto;">
    <h2>Sehir Bazinda Ozet Tablosu</h2>

    <input
        type="text"
        id="tabloArama"
        placeholder="Sehir ara..."
        style="padding:10px; width:250px; margin-bottom:15px;"
    >

    <table id="sehirTablosu" style="width:100%; border-collapse:collapse;">
        <thead>
            <tr>
                <th onclick="tabloSirala(0)">Sehir</th>
                <th onclick="tabloSirala(1)">Katilimci Sayisi</th>
                <th onclick="tabloSirala(2)">Ortalama Memnuniyet</th>
                <th onclick="tabloSirala(3)">Ortalama Bekleme</th>
            </tr>
        </thead>
        <tbody id="tabloGovdesi"></tbody>
    </table>
</div>

<script>
    const veriler = VERI_BURAYA;
   

        const sehirFiltresi = document.getElementById("sehirFiltresi");

        const sehirler = [...new Set(
            veriler.map(kayit => kayit["Şehir"])
        )].sort();

        sehirler.forEach(sehir => {
            const secenek = document.createElement("option");
            secenek.value = sehir;
            secenek.textContent = sehir;
            sehirFiltresi.appendChild(secenek);
        });

        function raporuGuncelle() {
            const secilenSehir = sehirFiltresi.value;

            const filtreliVeriler = secilenSehir === "Tümü"
                ? veriler
                : veriler.filter(kayit => kayit["Şehir"] === secilenSehir);

            function ortalama(sutun) {
    const sayilar = filtreliVeriler
        .filter(kayit =>
            kayit[sutun] !== null &&
            kayit[sutun] !== undefined &&
            kayit[sutun] !== ""
        )
        .map(kayit => Number(kayit[sutun]))
        .filter(sayi => Number.isFinite(sayi));

    if (sayilar.length === 0) return 0;

    return sayilar.reduce((toplam, sayi) => toplam + sayi, 0)
        / sayilar.length;
}

            document.getElementById("katilimci").textContent =
                filtreliVeriler.length;

            document.getElementById("memnuniyet").textContent =
                ortalama("Memnuniyet (1-5)").toFixed(2);

            document.getElementById("bekleme").textContent =
                ortalama("Bekleme (dk)").toFixed(2) + " dk";

            document.getElementById("tavsiye").textContent =
                ortalama("Tavsiye (0-10)").toFixed(2);
        }

        sehirFiltresi.addEventListener("change", raporuGuncelle);

        raporuGuncelle();
        // Grafiklerin tutulacağı alan
const grafikler = {};
Chart.register({
    id: "degerEtiketleri",
    afterDatasetsDraw(chart) {

        if (chart.canvas.id !== "memnuniyetGrafik") {
            return;
        }

        const { ctx } = chart;

        ctx.save();
        ctx.font = "bold 12px Arial";
        ctx.fillStyle = "#1e40af";
        ctx.textAlign = "center";

        chart.data.datasets[0].data.forEach((deger, index) => {

            const nokta = chart.getDatasetMeta(0).data[index];

            ctx.fillText(
                deger,
                nokta.x,
                nokta.y - 8
            );
        });

        ctx.restore();
    }
});

function grafikOlustur(id, tur, etiketler, degerler, sayilar) {

    // Eski grafiği varsa kaldır
    if (grafikler[id]) {
        grafikler[id].destroy();
    }

    const toplam = sayilar.reduce((a, b) => a + b, 0);

    grafikler[id] = new Chart(document.getElementById(id), {
        type: tur,

        data: {
            labels: etiketler,
            datasets: [{
                label: "Anket Sonuçları",
                data: degerler,
                backgroundColor: id === "memnuniyetGrafik"
    ? "#3b82f6"
    : [
        "#3b82f6", "#8b5cf6", "#06b6d4",
        "#10b981", "#f59e0b", "#ef4444",
        "#64748b", "#ec4899", "#84cc16", "#a855f7"
    ],
                borderWidth: 1,
                borderRadius: 5
            }]
        },

        options: {
            responsive: true,
            maintainAspectRatio: true,

            plugins: {
                tooltip: {
                    callbacks: {
                        label: function(context) {
                            const i = context.dataIndex;
                            const oran = toplam > 0
                                ? (sayilar[i] / toplam * 100).toFixed(1)
                                : 0;

                            if (id === "memnuniyetGrafik") {
    return [
        "Memnuniyet puanı: " + context.label,
        "Katılımcı sayısı: " + sayilar[i],
        "Oran: %" + oran
    ];
}

return [
    "Değer: " + context.raw,
    "Katılımcı: " + sayilar[i],
    "Oran: %" + oran
];
                        }
                    }
                }
            }
        }
    });
}


// Altı grafiği güncelle
function grafikleriGuncelle() {

    const sehir = sehirFiltresi.value;

    const liste = sehir === "Tümü"
        ? veriler
        : veriler.filter(k => k["Şehir"] === sehir);

    // 1. Memnuniyet dağılımı
    const memnuniyetPuanlari = [1, 2, 3, 4, 5];

    const memnuniyetSayilari = memnuniyetPuanlari.map(puan =>
        liste.filter(k => Number(k["Memnuniyet (1-5)"]) === puan).length
    );

    grafikOlustur(
        "memnuniyetGrafik",
        "bar",
        memnuniyetPuanlari.map(String),
        memnuniyetSayilari,
        memnuniyetSayilari
    );


    // 2. Tavsiye puanı dağılımı
    const tavsiyePuanlari = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10];

    const tavsiyeSayilari = tavsiyePuanlari.map(puan =>
        liste.filter(k => Number(k["Tavsiye (0-10)"]) === puan).length
    );

    grafikOlustur(
        "tavsiyeGrafik",
        "bar",
        tavsiyePuanlari.map(String),
        tavsiyeSayilari,
        tavsiyeSayilari
    );


    // 3. Bekleme süresi dağılımı
    const beklemeAraliklari = [
        { etiket: "0-10 dk", min: 0, max: 10 },
        { etiket: ">10-20 dk", min: 10, max: 20 },
        { etiket: ">20-30 dk", min: 20, max: 30 },
        { etiket: ">30-45 dk", min: 30, max: 45 },
        { etiket: ">45-60 dk", min: 45, max: 60 },
        { etiket: ">60 dk", min: 60, max: Infinity }
    ];

    const beklemeSayilari = beklemeAraliklari.map((aralik, index) =>
        liste.filter(k => {
            const deger = Number(k["Bekleme (dk)"]);

            if (k["Bekleme (dk)"] === null ||
                k["Bekleme (dk)"] === "") return false;

            return index === 0
                ? deger >= aralik.min && deger <= aralik.max
                : deger > aralik.min && deger <= aralik.max;
        }).length
    );

    grafikOlustur(
        "beklemeGrafik",
        "bar",
        beklemeAraliklari.map(a => a.etiket),
        beklemeSayilari,
        beklemeSayilari
    );


    // 4. Şehirlere göre memnuniyet
    const sehirler = [...new Set(liste.map(k => k["Şehir"]))].sort();

    const sehirSayilari = sehirler.map(sehir =>
        liste.filter(k => k["Şehir"] === sehir).length
    );

    const sehirOrtalamalari = sehirler.map(sehir => {
        const kayitlar = liste.filter(k =>
            k["Şehir"] === sehir &&
            k["Memnuniyet (1-5)"] !== null
        );

        const puanlar = kayitlar
            .map(k => Number(k["Memnuniyet (1-5)"]))
            .filter(Number.isFinite);

        return puanlar.length
            ? Number((puanlar.reduce((a, b) => a + b, 0) / puanlar.length).toFixed(2))
            : 0;
    });

    grafikOlustur(
        "sehirGrafik",
        "bar",
        sehirler,
        sehirOrtalamalari,
        sehirSayilari
    );


    // 5. Yaş gruplarına göre memnuniyet
    const yasGruplari = [
        { etiket: "18 altı", min: 0, max: 18 },
        { etiket: "18-25", min: 18, max: 26 },
        { etiket: "26-35", min: 26, max: 36 },
        { etiket: "36-45", min: 36, max: 46 },
        { etiket: "46-55", min: 46, max: 56 },
        { etiket: "56-65", min: 56, max: 66 },
        { etiket: "65 üzeri", min: 65, max: 101 }
    ];

    const yasSayilari = [];
    const yasOrtalamalari = [];

    yasGruplari.forEach(grup => {

        const kayitlar = liste.filter(k => {
            const yas = Number(k["Yaş"]);

            return k["Yaş"] !== null &&
                k["Yaş"] !== "" &&
                yas >= grup.min && yas < grup.max;
        });

        yasSayilari.push(kayitlar.length);

        const puanlar = kayitlar
            .map(k => Number(k["Memnuniyet (1-5)"]))
            .filter(Number.isFinite);

        yasOrtalamalari.push(
            puanlar.length
                ? Number((puanlar.reduce((a, b) => a + b, 0) / puanlar.length).toFixed(2))
                : 0
        );
    });

    grafikOlustur(
        "yasGrafik",
        "bar",
        yasGruplari.map(g => g.etiket),
        yasOrtalamalari,
        yasSayilari
    );


    // 6. Aylara göre katılımcı sayısı
    const aylar = [
        "Ocak", "Şubat", "Mart", "Nisan",
        "Mayıs", "Haziran", "Temmuz", "Ağustos",
        "Eylül", "Ekim", "Kasım", "Aralık"
    ];

    const aySayilari = Array(12).fill(0);

    liste.forEach(k => {
        if (k["Tarih"]) {
            const ay = new Date(k["Tarih"]).getMonth();
            if (!isNaN(ay)) aySayilari[ay]++;
        }
    });

    grafikOlustur(
        "ayGrafik",
        "line",
        aylar,
        aySayilari,
        aySayilari
    );
}

// Tabloyu olustur
function tabloGuncelle() {

    const sehir = sehirFiltresi.value;

    const liste = sehir === "Tümü"
        ? veriler
        : veriler.filter(k => k["Şehir"] === sehir);

    const sehirler = [...new Set(
        liste.map(k => k["Şehir"])
    )].sort();

    const govde = document.getElementById("tabloGovdesi");

    govde.innerHTML = "";

    sehirler.forEach(sehirAdi => {

        const kayitlar = liste.filter(
            k => k["Şehir"] === sehirAdi
        );

        const memnuniyetler = kayitlar
            .map(k => k["Memnuniyet (1-5)"])
            .filter(v => v !== null && v !== "")
            .map(Number)
            .filter(Number.isFinite);

        const beklemeler = kayitlar
            .map(k => k["Bekleme (dk)"])
            .filter(v => v !== null && v !== "")
            .map(Number)
            .filter(Number.isFinite);

        const ortalamaMemnuniyet = memnuniyetler.length
            ? (memnuniyetler.reduce((a, b) => a + b, 0)
                / memnuniyetler.length).toFixed(2)
            : "-";

        const ortalamaBekleme = beklemeler.length
            ? (beklemeler.reduce((a, b) => a + b, 0)
                / beklemeler.length).toFixed(2)
            : "-";

        const satir = document.createElement("tr");

        [
            sehirAdi,
            kayitlar.length,
            ortalamaMemnuniyet,
            ortalamaBekleme
        ].forEach(deger => {

            const hucre = document.createElement("td");

            hucre.textContent = deger;
            hucre.style.padding = "12px";
            hucre.style.borderBottom = "1px solid #ddd";

            satir.appendChild(hucre);
        });

        govde.appendChild(satir);
    });
}


const tabloArama = document.getElementById("tabloArama");

if (tabloArama) {
    tabloArama.addEventListener("input", function() {

        const arama = this.value.toLocaleLowerCase("tr-TR");

        const satirlar = document.querySelectorAll(
            "#tabloGovdesi tr"
        );

        satirlar.forEach(satir => {

            const sehir = satir.cells[0].textContent
                .toLocaleLowerCase("tr-TR");

            satir.style.display = sehir.includes(arama)
                ? ""
                : "none";
        });
    });
}

// Tablo siralama
let siralamaYonleri = {};

function tabloSirala(sutun) {

    const govde = document.getElementById("tabloGovdesi");

    const satirlar = [...govde.querySelectorAll("tr")];

    siralamaYonleri[sutun] = !siralamaYonleri[sutun];

    satirlar.sort((a, b) => {

        let degerA = a.cells[sutun].textContent;
        let degerB = b.cells[sutun].textContent;

        if (sutun === 0) {
            return siralamaYonleri[sutun]
                ? degerA.localeCompare(degerB, "tr")
                : degerB.localeCompare(degerA, "tr");
        }

        degerA = Number(degerA);
        degerB = Number(degerB);

        return siralamaYonleri[sutun]
            ? degerA - degerB
            : degerB - degerA;
    });

    satirlar.forEach(satir => govde.appendChild(satir));
}


// Ilk acilista tabloyu doldur
tabloGuncelle();


// Sehir filtresi degisince tabloyu da guncelle
sehirFiltresi.addEventListener("change", tabloGuncelle);
// İlk açılışta ve şehir değişince grafikleri güncelle
sehirFiltresi.addEventListener("change", grafikleriGuncelle);

grafikleriGuncelle();
    </script>

</body>
</html>
"""

# Verileri HTML kodunun içine yerleştir
html_icerik = html_icerik.replace("VERI_BURAYA", veriler)

# HTML dosyasını kaydet
with open("anket_raporu.html", "w", encoding="utf-8") as dosya:
    dosya.write(html_icerik)

print("\nHTML raporu başarıyla oluşturuldu!")
print("Dosya adı: anket_raporu.html")
