# **Hukuk-TR: Vatandaşın Dijital Savunucusu — Evrimsel SLM ve Agentic RAG Entegrasyonu Stratejik Araştırma Raporu**

> ⚠️ **GEÇERSİZ / TARİHSEL BAĞLAM (2026-05-29).** Bu rapor erken bir strateji taslağıdır ve **operatif plan değildir.** Önerdiği baz model (**Gemma 4 26B A4B MoE**, ~25B param) projenin temel kısıtıyla — *consumer ~8 GB GPU'da erişilebilirlik* — çelişir. **Operatif karar (güncellendi 2026-07-01): Gemma 4 12B** (`gemma-4-12B-it-qat-q4_0-unquantized`, QLoRA 4-bit → Q4_0 GGUF; ADR-0003, 2026-06-07). *(Not: bu banner önceden "Qwen3.5-4B" diyordu — o da süpersed oldu; Qwen3.5-4B hiç eğitilmedi, ADR-0003 ile Gemma 4 12B seçildi.)* Çakışmada `docs/VISION.md` + `docs/FINE_TUNING.md` + `docs/TEKNIK_PLAN.md` geçerlidir. Rapor; pazar/evrim/RAG fikirleri için fikir kaynağı olarak tutulur.

2026 yılı, yapay zekanın genel amaçlı bir araç olmaktan çıkıp, yerel mevzuat ve vatandaş ihtiyaçlarına özel dikey uzmanlıklara (Vertical AI) evrildiği dönemi temsil etmektedir. Bu rapor, Türkiye'deki bireylerin hukuki süreçlerini kolaylaştırmak, kanun okuryazarlığını artırmak ve avukatlık hizmetlerine erişim öncesinde ön hazırlık yapmalarını sağlamak amacıyla kurgulanan "Hukuk-TR" projesinin teknik, verisel ve evrimsel yol haritasını sunmaktadır.

## **1\. Teknolojik Temel: Gemma 4 26B A4B (MoE)**

Projenin ana motoru olarak Google'ın 2026 Mart ayında duyurduğu **Gemma 4 26B A4B** modeli seçilmiştir. Bu modelin seçilme nedenleri şunlardır:

* **Aktif Parametre Verimliliği:** Toplam 25,2 milyar parametreye sahip olmasına rağmen, Mixture-of-Experts (MoE) mimarisi sayesinde her işlemde sadece **3,8 milyar parametreyi** aktif ederek yüksek hız ve düşük VRAM kullanımı sunar.  
* **Gelişmiş Akıl Yürütme (Thinking Mode):** Yerleşik "Thinking" modu, modelin bir hukuki çıkarım yapmadan önce ilgili kanun maddelerini adım adım analiz etmesini sağlar.  
* **Geniş Bağlam Penceresi:** 256.000 tokenlik kapasite, kullanıcının tüm dava dosyasını veya yüzlerce sayfalık Yargıtay ilamlarını tek seferde modele "bağlam" olarak sunabilmesine imkan tanır.

## **2\. Evrimsel Yol Haritası (0'dan 1'e Stratejisi)**

Hukuk-TR, tek bir büyük hamle yerine, her aşamada üzerine yeni yetenekler eklenen 5 ana basamakta evrilecektir.

### **2.1. Aşama 1: Hukuk Okuryazarı (SFT Katmanı)**

Vatandaşın günlük dilini hukuki terimlere, karmaşık kanun maddelerini ise anlaşılır bir dile çevirme aşamasıdır.

* **Veri Setleri:** Kaggle üzerindeki 13.000+ örnekli Turkish Law Dataset for LLM Finetuning 1 ve HuggingFace'teki gerçek soru-cevap çiftlerini içeren hukuk\_soru\_cevap seti kullanılacaktır.  
* **Eğitim:** **Google Colab A100 (40GB)** donanımı üzerinde, Unsloth optimizasyonu ve **QLoRA** tekniğiyle model Türk hukuk sistemine adapte edilecektir.  
* **Hedef:** Vatandaşın "Ev sahibi beni haklı sebep olmadan çıkarabilir mi?" gibi sorularına kanun referanslı net yanıtlar vermek.

### **2.2. Aşama 2: Emsal Dedektifi (Agentic RAG Katmanı)**

Kanun maddelerinin sahadaki uygulamasını (içtihatları) modele öğretme aşamasıdır.

* **Veri Havuzu:** HuggingFace üzerindeki 700.000 adet kümelenmiş Yargıtay ve Danıştay belgesini içeren Turkish-Law-Documents-700k-clustered veri seti kullanılacaktır.  
* **Teknik:** Model, bir vektör veritabanı üzerinden kullanıcının durumuna en yakın 5-10 emsal kararı "Agentic RAG" yöntemiyle çeker ve analiz eder.  
* **Hedef:** "Senin durumuna benzer davalarda Yargıtay %80 oranında şu yönde karar vermiş" diyebilen bir içtihat motoru.

### **2.3. Aşama 3: Sanal Sekreter (e-Devlet ve UYAP Entegrasyonu)**

Sistemin kullanıcıya özel veriye (kendi davasına) erişim yetkisi kazandığı aşamadır.

* **Entegrasyon:** **yargi-mcp** (Model Context Protocol) sunucusu aracılığıyla modelin doğrudan UYAP Vatandaş Portalı verilerine Markdown formatında erişmesi sağlanır.  
* **Canlı Takip:** e-Tebligat Bütünleşik Hizmeti ve UYAP Dosya Sorgulama sistemlerinden gelen verilerle model, kullanıcının duruşma takvimi ve yeni eklenen evraklar hakkında otonom bildirimler yapar.  
* **Hedef:** "Davanıza yeni bir bilirkişi raporu eklendi, özeti şudur..." diyebilen kişisel hukuki asistan.

### **2.4. Aşama 4: Strateji ve Dilekçe Yazarı (Alignment & HITL)**

Modelin sadece bilgi vermeyip, hukuki geçerliliği olan belgeler üretmeye başladığı profesyonel aşamadır.

* **Hizalama (Alignment):** Uzman avukatların model çıktılarını puanladığı bir **Human-in-the-Loop (HITL)** döngüsü kurulacaktır.  
* **Optimizasyon:** Direct Preference Optimization (DPO) yöntemiyle model, avukatların tercih ettiği üslup ve argüman yapısına göre hizalanacaktır.  
* **Hedef:** Mahkemeye sunulmaya hazır, emsal kararlara nokta atışı atıfta bulunan profesyonel dilekçe taslakları üretmek.

### **2.5. Aşama 5: Dev Hedef \- Otonom Mevzuat Ekosistemi**

Hukuk, maliye ve uyum (compliance) süreçlerinin birleştiği devasa bir zeka ekosistemi. Bu aşamada sistem, sadece bireyler için değil, kurumlar için de otonom bir yasal yönetim kurulu üyesi gibi çalışarak riskleri önceden sezer ve otonom çözümler üretir.

## **3\. Donanım ve Uygulama Gereksinimleri**

| Gereksinim | Detay | Gerekçe |
| :---- | :---- | :---- |
| **İşlemci (Training)** | Google Colab NVIDIA A100 (40GB) | QLoRA ile 16-20 GB VRAM kullanımıyla en verimli eğitim |
| **Yazılım Altyapısı** | Unsloth \+ yargi-mcp | %60 daha az VRAM tüketimi ve hızlı çıkarım |
| **Kuantizasyon** | 4-bit (Q4\_K\_M) | Bellek gereksinimini \~18GB'a indirerek tüketici sınıfı donanımda çalışma imkanı |
| **Doğrulama Aracı** | Label Studio / Argilla | HITL ve DPO süreçleri için profesyonel etiketleme arayüzü |

## **4\. Güvenlik ve Veri Gizliliği (2026 Mevzuatı)**

Proje, Türk Veri Koruma Kanunu (KVKK) ve 2026 yılındaki güncel yapay zeka regülasyonlarına tam uyumlu olacak şekilde tasarlanmıştır. SLM'lerin yerel cihazlarda veya özel bulut ortamlarında (VPC) çalışabilme yeteneği, vatandaşın hassas yasal verilerinin (dava dosyaları, kimlik bilgileri) dış dünyaya sızmasını engeller.2

## **5\. Gelecek Vizyonu**

Hukuk-TR'nin nihai vizyonu, adaleti demokratikleştirmektir. Vatandaşın e-Devlet şifresiyle bağlandığı, kendi dosyasının risk analizini yaptığı ve profesyonel avukatlık hizmeti almadan önceki süreçte tam donanımlı hale geldiği bu ekosistem; 2026 sonrasında mali danışmanlık ve kurumsal uyum modülleriyle birleşerek Türkiye'nin dijital egemen AI altyapısının temel taşlarından biri olacaktır.

#### **Alıntılanan çalışmalar**

1. Turkish Law Dataset for LLM Finetuning \- Kaggle, erişim tarihi Nisan 15, 2026, [https://www.kaggle.com/datasets/batuhankalem/turkish-law-dataset-for-llm-finetuning](https://www.kaggle.com/datasets/batuhankalem/turkish-law-dataset-for-llm-finetuning)  
2. Small Language Models: A Complete Guide for 2026 \- Knolli.ai, erişim tarihi Nisan 15, 2026, [https://www.knolli.ai/post/small-language-models](https://www.knolli.ai/post/small-language-models)  
3. Global Privacy Trends and Best Practices for Compliance in 2026 \- Schellman, erişim tarihi Nisan 15, 2026, [https://www.schellman.com/blog/privacy/global-privacy-compliance-trends-in-2026](https://www.schellman.com/blog/privacy/global-privacy-compliance-trends-in-2026)