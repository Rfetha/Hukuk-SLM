## 2026-07-05 · v3 genelleme eval-dilimleri (SAFE, train-dokunmaz) + 🔴 OOD-bloklu bulgusu

**Bağlam:** v3 train + eval'in ikisi de tek tuzak-ailesi (aynı-kanun leksik-komşu) içeriyor → "v3 bir aileyi öğrenip başkasında çöküyor mu" ve "eval-mirror'a ezber mi" ölçülemiyordu. Train'e DOKUNMADAN (yeni sınav kâğıdı) genelleme dilimleri kuruldu. Kod: `scripts/build_eval_ood.py` (yeni; `build_eval_sets.py` import-reuse, DEĞİŞTİRİLMEDİ). Yürütme: subagent, seed=3407.

**✅ `data/eval/trap_xkanun.jsonl` — ÇAPRAZ-KANUN near-miss DRAFT (35 örnek).** Yöntem: her soru için TÜM havuzdan `kanun_no ≠ soru-kanunu` max-Jaccard madde = başka kanunun konu-yakın (ama cevaplamayan) maddesi. Şema canon `trap.jsonl` uyumlu (`kanun_no|madde_no`=tuzak, gen_eval_grounded join eder). Doğrulama: 35/35 benzersiz, injection-resolve fail=0, cross-law ihlali=0, **sızıntı=0** (yapısal 2914 çift + metin-bazlı 14.618 anahtar; packed_v3 distractor'ları dahil — ilk denemede 1 distractor sızıntısı metin-dışlamayla giderildi). `_overlap` med=0.103 (canon trap 0.123 ile kıyaslanabilir). Tek-kanun cap=7 tuttu, 27 farklı tuzak-kanun. **Geçici-madde guard:** ilk EDA'da bir tuzak (ov=0.588) kirliydi (soru trivia + tuzak tarihi içeriyordu) → geçici maddeler soru+tuzak havuzundan çıkarıldı (17/1022 soru etkilendi). Gözle 5 örnek doğrulandı (İİK 270 hapis-hakkı vs TTK 1206 taşıyan-hapis; CMK 134 vs 5549 elkoyma) → hepsi temiz near-miss, kazara-cevaplamıyor.

**🔴 `trap_ood.jsonl` — BLOKLU (kurulamadı, paper-değerli bulgu).** Held-out (v3-görülmemiş) kanunlar için **HİÇ SORU YOK.** Envanter: madde havuzu **892 kanun** ama soru kaynağı `sft_v1/test.jsonl` yalnız **11 kanun** — ve bu 11, v3-eğitiminde görülen 11 kanunla **BİREBİR AYNI** (`test_laws == seen_laws`, held-out-soru=0). **Sonuç: mevcut eval'imiz eğitimle özdeş 11 kanuna hapsedilmiş** → "görülmemiş kanunda genelleme" ölçülemiyor. Kapatmak için held-out kanunlara grounded-sentetik SORU üretimi gerekir (madde → LLM soru). → **kapı-sonrası iş.** Bu, "eval-mirror overfit" endişesini ölçülü olgu haline getirir: eval-mirror sadece zorluk değil **kanun-kapsamı** olarak da dar.

**Defer (yeni veri kaynağı gerekir):** temporal (mülga/değişmiş) — ham şema `{kanun_adi,kanun_no,madde_no,text}`, yapısal mülga-flag/yürürlük-tarihi/versiyon-çifti YOK (serbest-metin "mülga" 4828 madde var ama parse edilmemiş); çok-hop (madde→madde atıf) — atıf-grafiği parse edilmemiş (4347 madde serbest-metin atıf içerir). **#3a çok-kaynak:** ayrı jsonl GEREKMEZ — `gen_eval_grounded.py --distractors`/`raft_pack.pack_context` eval-run anında zaten çoklu-chunk paketliyor → harness-config notu.

**Durum güncellemesi (data panosu):** #2a çapraz-kanun = DRAFT hazır (ADIM 9'da kullanılır) · #1 OOD = **bloklu** (görülmemiş-kanun sorusu yok → sentetik-soru üretimi, kapı-sonrası) · temporal/çok-hop = defer · #3a = harness-only. Hiçbiri train'e dokunmadı (git: yalnız `build_eval_ood.py` yeni; `data/` gitignore → jsonl commit'lenmez, reprodüksiyon `build_eval_ood.py` ile).

**Kaynak:** `scripts/build_eval_ood.py` · `data/eval/trap_xkanun.jsonl` (35, seed 3407) · envanter kanıtı test_laws==seen_laws.
**Paper eşleme:** OOD-bloklu = metodoloji-sınırı bulgusu (eval kanun-kapsamı = train kanun-kapsamı → genelleme iddiası için sentetik held-out şart); çapraz-kanun dilimi = "tek-aile körlüğü" testi (near-miss genellemesini aile-ötesi ölçer).

---

