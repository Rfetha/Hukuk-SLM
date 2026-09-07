from atif_dogrula import DOGRULANDI, AYRISTIRILAMADI, MADDE_YOK, KANUN_YOK, \
    atiflari_ayikla, dogrula  # noqa: E402

KORPUS = [
    {"kanun_no": "5271", "kanun_adi": "CEZA MUHAKEMESİ KANUNU", "madde_no": "Madde 161",
     "text": "Cumhuriyet savcısı soruşturmayı bizzat yapar."},
    {"kanun_no": "4857", "kanun_adi": "İŞ KANUNU", "madde_no": "Madde 21",
     "text": "İşe iade davası."},
    {"kanun_no": "6100", "kanun_adi": "HUKUK MUHAKEMELERİ KANUNU", "madde_no": "MADDE 436",
     "text": "Hakem kararının içeriği."},
    {"kanun_no": "634", "kanun_adi": "KAT MÜLKİYETİ KANUNU", "madde_no": "Geçici Madde 1",
     "text": "Geçici hüküm."},
]


def test_ayikla_kanun_adi_madde_kalibini_yakalar():
    a = atiflari_ayikla("CEZA MUHAKEMESİ KANUNU Madde 161, savcı soruşturmayı yapar.")
    assert len(a) == 1
    assert a[0].kanun == "CEZA MUHAKEMESİ KANUNU" and a[0].madde == "161"


def test_ayikla_turkce_ekleri_atar():
    # Gerçek çıktıdan: "HUKUK MUHAKEMELERİ KANUNU MADDE 436'nun (1) fıkrasının"
    a = atiflari_ayikla("HUKUK MUHAKEMELERİ KANUNU MADDE 436'nun (1) fıkrası")
    assert a[0].madde == "436"


def test_ayikla_parantezli_altin_kalibini_yakalar():
    # DEV altın cevap biçimi: "(CEZA MUHAKEMESİ KANUNU, Madde 161)"
    a = atiflari_ayikla("Savcı soruşturur. (CEZA MUHAKEMESİ KANUNU, Madde 161)")
    assert len(a) == 1 and a[0].madde == "161"


def test_ayikla_birden_cok_atifi_ayirir():
    a = atiflari_ayikla("İŞ KANUNU Madde 21 ve CEZA MUHAKEMESİ KANUNU Madde 161 uyarınca.")
    assert [x.madde for x in a] == ["21", "161"]


def test_ayikla_gecici_maddeyi_ayirir():
    a = atiflari_ayikla("KAT MÜLKİYETİ KANUNU Geçici Madde 1 uyarınca.")
    assert a[0].tip == "GECICI"


def test_dogrula_var_olan_maddeyi_onaylar():
    a = atiflari_ayikla("CEZA MUHAKEMESİ KANUNU Madde 161")[0]
    assert dogrula(a, KORPUS).hukum == DOGRULANDI


def test_dogrula_uydurulan_madde_numarasini_yakalar():
    a = atiflari_ayikla("CEZA MUHAKEMESİ KANUNU Madde 9999")[0]
    assert dogrula(a, KORPUS).hukum == MADDE_YOK


def test_dogrula_var_olmayan_kanunu_yakalar():
    a = atiflari_ayikla("UZAY HUKUKU KANUNU Madde 1")[0]
    assert dogrula(a, KORPUS).hukum == KANUN_YOK


def test_dogrula_gecici_madde_normalden_ayri_dogrulanir():
    # ⚠️ Geçici Madde 1 varken normal Madde 1 YOK — karıştırılırsa uydurma atıf onaylanır.
    yok = atiflari_ayikla("KAT MÜLKİYETİ KANUNU Madde 1")[0]
    var = atiflari_ayikla("KAT MÜLKİYETİ KANUNU Geçici Madde 1")[0]
    assert dogrula(yok, KORPUS).hukum == MADDE_YOK
    assert dogrula(var, KORPUS).hukum == DOGRULANDI


def test_ayristirilamayan_atif_sessizce_yutulmaz():
    # ⚠️ EN TEHLİKELİ HATA: ayrıştırıcı bir biçimi tanımazsa atıf YOK sayılır ve
    # red kapısı cevabı GEÇİRİR. Tanınmayan 'madde' bahsi görünür kalmalı.
    a = atiflari_ayikla("Bu durum 5271 sayılı düzenlemenin ilgili maddesinde yer alır.")
    assert len(a) == 1 and a[0].tip == AYRISTIRILAMADI


def test_atifsiz_cevapta_ayristirilamadi_uretilmez():
    assert atiflari_ayikla("Verilen kaynaklarda bu konuyu düzenleyen madde bulunmuyor.") == []


def test_ayikla_baslik_bicimli_kanun_adini_yakalar():
    # ⚠️ Gerçek model çıktısı hem "TÜRK CEZA KANUNU" hem "Türk Ceza Kanunu" yazıyor.
    # Yalnız büyük harfi tanımak, gerçek atıfları AYRISTIRILAMADI'ya düşürüyordu.
    a = atiflari_ayikla("Vücuda cisim sokularak yapılan saldırıda Türk Ceza Kanunu Madde 102 uygulanır.")
    assert len(a) == 1 and a[0].madde == "102"
    assert a[0].tip == "NORMAL"


def test_ayikla_baslik_bicimli_ekli_adi_yakalar():
    a = atiflari_ayikla("Şartlar Türk Medeni Kanunu'nun Madde 313 hükmünde düzenlenmiştir.")
    assert a[0].madde == "313"


def test_dogrula_ayni_adi_tasiyan_iki_kanunu_karistirmaz():
    # ⚠️ Korpusta "İŞ KANUNU" adı İKİ kanuna ait: 4857 (yürürlükte) ve 1475 (mülga).
    # Ad→tek kanun_no eşlemesi sessizce birini seçiyor ve GERÇEK atıfı MADDE_YOK
    # sayıyordu. Ad çok anlamlıysa, maddeyi TAŞIYAN kanun doğrulamayı geçirmeli.
    korpus = [
        {"kanun_no": "1475", "kanun_adi": "İŞ KANUNU", "madde_no": "Madde 14", "text": "kıdem"},
        {"kanun_no": "4857", "kanun_adi": "İŞ KANUNU", "madde_no": "Madde 21", "text": "işe iade"},
    ]
    h = dogrula(atiflari_ayikla("İŞ KANUNU Madde 21")[0], korpus)
    assert h.hukum == DOGRULANDI and h.kanun_no == "4857"
    h2 = dogrula(atiflari_ayikla("İŞ KANUNU Madde 14")[0], korpus)
    assert h2.hukum == DOGRULANDI and h2.kanun_no == "1475"
    h3 = dogrula(atiflari_ayikla("İŞ KANUNU Madde 9999")[0], korpus)
    assert h3.hukum == MADDE_YOK


def test_dogrula_turkce_buyuk_harf_donusumunu_dogru_yapar():
    # ⚠️ Python'ın upper()'ı Türkçe değil: "Medeni" → "MEDENI" (ASCII I), korpusta
    # ise "MEDENİ". Bu, GERÇEK atıfları KANUN_YOK sayıyordu.
    korpus = [{"kanun_no": "4721", "kanun_adi": "TÜRK MEDENİ KANUNU",
               "madde_no": "Madde 313", "text": "evlât edinme"}]
    h = dogrula(atiflari_ayikla("Türk Medeni Kanunu Madde 313")[0], korpus)
    assert h.hukum == DOGRULANDI


def test_dogrula_ad_onune_kacan_sozcugu_tolere_eder():
    # ⚠️ "Ayrıca TÜRK BORÇLAR KANUNU Madde 6" → ayrıştırıcı "Ayrıca"yı da ada katıyor
    # ve ad bulunamıyordu. Bilinen bir kanun adına denk gelen en uzun SONEK aranır.
    korpus = [{"kanun_no": "6098", "kanun_adi": "TÜRK BORÇLAR KANUNU",
               "madde_no": "Madde 6", "text": "örtülü kabul"}]
    h = dogrula(atiflari_ayikla("Ayrıca TÜRK BORÇLAR KANUNU Madde 6 uygulanır.")[0], korpus)
    assert h.hukum == DOGRULANDI and h.kanun_no == "6098"


def test_dogrula_gercekten_olmayan_kanunu_hala_yakalar():
    korpus = [{"kanun_no": "6098", "kanun_adi": "TÜRK BORÇLAR KANUNU",
               "madde_no": "Madde 6", "text": "x"}]
    assert dogrula(atiflari_ayikla("UZAY HUKUKU KANUNU Madde 6")[0], korpus).hukum == KANUN_YOK


def test_dogrula_resmi_adin_kisa_halini_taniyor():
    # ⚠️ Ölçüldü (harness AÇIK koşusu): 5 KANUN_YOK'un TAMAMI yanlış negatifti —
    # model resmî adın yaygın kısa hâlini yazıyor ve bu ad, resmî adın SONEKİ:
    #   "İflas Kanunu"            ⊂ "İCRA VE İFLAS KANUNU" (2004)
    #   "Teknik Düzenlemeler K."  ⊂ "ÜRÜN GÜVENLİĞİ VE TEKNİK DÜZENLEMELER KANUNU"
    # Katı kapıda her yanlış negatif doğrudan coverage kaybıdır (ADR-0038).
    korpus = [{"kanun_no": "2004", "kanun_adi": "İCRA VE İFLAS KANUNU",
               "madde_no": "Madde 85", "text": "haciz"}]
    h = dogrula(atiflari_ayikla("İflas Kanunu Madde 85")[0], korpus)
    assert h.hukum == DOGRULANDI and h.kanun_no == "2004"


def test_dogrula_tek_sozcuklu_sonek_her_kanuna_uymaz():
    # ⚠️ Sonek gevşetmesinin sınırı: "Kanunu" tek başına HER kanuna uyar ve
    # doğrulayıcıyı işe yaramaz hale getirirdi.
    korpus = [{"kanun_no": "2004", "kanun_adi": "İCRA VE İFLAS KANUNU",
               "madde_no": "Madde 85", "text": "haciz"}]
    assert dogrula(atiflari_ayikla("Kanunu Madde 85")[0], korpus).hukum == KANUN_YOK
