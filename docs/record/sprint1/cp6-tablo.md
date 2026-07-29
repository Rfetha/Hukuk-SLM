| eksen | base | gem | tg |
| :--- | ---: | ---: | ---: |
| **M1** faith_macro (ALL) | 0.8385 | 0.8734 | 0.8371 |
| M1 **A1** (cevaplanan) | 0.9730 | 0.9729 | 0.8472 |
| M1 **coverage** | 35/80 = %43.8 | 61/80 = %76.2 | 68/80 = %85.0 |
| M1 cit_precision | 0.9775 | 0.9900 | 0.9500 |
| **M4** faith_macro (ALL) | 0.9810 | 0.9736 | 0.9771 |
| M4 **A1** (cevaplanan) | 0.9800 | 0.9793 | 0.9794 |
| M4 **coverage** | 76/80 = %95.0 | 78/80 = %97.5 | 77/80 = %96.2 |
| M4 cit_precision | 1.0000 | 1.0000 | 1.0000 |
| **M2** Rej (LLM hakemi) | 0.6330 | 0.8420 | 0.4580 |
| M2 Rej (regex) | 0.5670 | ⚠️ 0.8070 | 0.4240 |
| M2 geçerli tuzak *(payda)* | 60 | 57 | 59 |
| **M2B** Rej (LLM hakemi) | 0.9730 | 0.9700 | 1.0000 |
| M2B Rej (regex) | 0.9870 | ⚠️ 0.9700 | 1.0000 |
| M2B geçerli tuzak *(payda)* | 75 | 67 | 80 |
| **M3** Rej (LLM hakemi) | 1.0000 | 1.0000 | 1.0000 |
| M3 Rej (regex) | 1.0000 | ⚠️ 1.0000 | 1.0000 |
| M3 geçerli tuzak *(payda)* | 57 | 57 | 50 |
| **M5** faith_macro *(ANTİ-HEDEF ↓)* | 0.3992 | 0.5786 | 0.4421 |
| M5 **coverage** *(kör cevaplama ↓)* | 30/80 = %37.5 | 19/80 = %23.8 | 29/80 = %36.2 |
| register proxy M1 | 0.9730 | 0.9830 | 1.0000 |
| register proxy M4 | 0.9610 | 0.9230 | 0.9750 |
| register proxy M2 | 0.9640 | 0.9190 | 0.9450 |
| register proxy M2B | 0.9810 | 0.9880 | 1.0000 |

*Hakem: `gpt-4o-mini` / `openai` · seed 3407 · harness KAPALI · DEV havuzu.*
*⚠️ **regex-red kalibre edilmedi**: gem — o satırlar raporlanamaz, LLM-red satırı okunur (TASARIM §3.4).*
*Rej paydaları modele göre değişir (`geçerli tuzak` satırı) — oranlar payda ile birlikte okunur.*
