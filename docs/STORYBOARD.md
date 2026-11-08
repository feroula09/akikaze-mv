# 《秋風恋歌》分鏡

依 `docs/CONCEPT.md`、`docs/CHARACTER.md`。時間單位是秒；`b33` = 第 33 小節（`analysis/audio.json` 的 `bars[].index`）。
102 BPM：一拍 0.588 s，一小節 2.353 s。剪接點在 timeline 裡用 `nb(歌詞起點)`（段落內）與 `B(n)`（段落交界）對齊。
這首歌慢、抒情，所以分鏡比 pipeline 建議的 60–80 鏡少、長鏡頭多（共 61 鏡，其中 5 個超過 9 秒的長鏡頭）。

縮寫：小夜＝S、千鶴＝C；調色盤名稱見 CONCEPT「色彩腳本」。字幕欄：`main`＝直排明朝（JIZURA 預設）、`キメ`＝筆文字（Yuji Syuku）、`手寫`＝千鶴的字（Klee One）、`—`＝不放字幕或由場景自己排字。

## 鏡頭表

### Intro (quiet) b0–8 ・ 和紙

| # | 時間 | 歌詞 | 場景 | 內容 | 素材 | 字 |
|---|---|---|---|---|---|---|
| 01 | 0.00–8.49 (b0–4) | — | `leaves` pair | 和紙白底。綠楓從右上、紅楓從左上沿落葉弧線飄入，在中央相遇、互繞半圈。長鏡頭。 | prop_leaf_red, prop_leaf_green, bg_washi | — |
| 02 | 8.49–17.90 (b4–8) | — | `leaves` part | b6 一陣風把兩片吹散：綠楓往上飄出畫面（天上），紅楓往下落到畫面底部。最後一拍和紙全白。 | 同上 | — |

### Intro (band) b8–17 ・ 3D-A ・ 現在段

| # | 時間 | 歌詞 | 場景 | 內容 | 素材 | 字 |
|---|---|---|---|---|---|---|
| 03 | 17.90–39.07 (b8–17) | — | `seq` 3D-A | **招牌 1＋2**：b8 樂團進入，切進 3D-A 第一格，石板小徑穿過現在段調色的楓林往前推。前 4 小節疊標題：「秋風恋歌」筆文字寫出，下方 `AKIKAZE RENKA` 與「原曲：秋風恋歌 / DeZI：R」。 | blender/renders/pathA | 自訂標題 |
| 04 | 39.07–48.49 (b17–21) | 二人歩いた小径 / ひとり歩いています | `seq` 3D-A（續） | 同一個長鏡頭，鏡頭慢下來，停在小徑前方；S 的背影在 engine 合成，小小一個，身旁空著。 | 同上＋sayo_walk_back | main |

### Verse 1 b17–25 ・ 現在段

| # | 時間 | 歌詞 | 場景 | 內容 | 素材 | 字 |
|---|---|---|---|---|---|---|
| 05 | 48.43–52.53 | 風に揺れる葉の音 | `illust` | 仰看楓樹樹冠，葉子在風裡抖動，鏡頭慢慢旋轉；落葉 fx 稀疏。 | bg_canopy | main |
| 06 | 52.53–57.84 | ひとり歌を口ずさみます | `illust` | S 胸上，閉眼輕哼，褪色手毬抱在胸前。她每哼一句，就有一片紅楓從她身邊落下（主題第一次出現）。 | sayo_hum, bg_path_present | main |

### Pre-chorus 1 b25–33 ・ 現在段 ⇄ 回憶段閃入

| # | 時間 | 歌詞 | 場景 | 內容 | 素材 | 字 |
|---|---|---|---|---|---|---|
| 07 | 57.84–60.25 | 手鞠花 | `illust` | 特寫：S 手中褪色的手毬。 | hands_temari_faded | main |
| 08 | 60.25–62.55 | 色あせるやうに | `illust` | `ink` 轉場（水彩暈開）閃入回憶段：同樣位置是 C 手中嶄新的手毬，暖金色。 | hands_temari_new | main |
| 09 | 62.55–67.27 | この想い消え逝く前に | `illust` | S 側臉，低頭看掌心裡的一片紅楓；畫面四周的顏色慢慢褪掉。 | sayo_side_leaf, bg_path_present | main |
| 10 | 67.27–71.98 | 手毬歌歌う貴女の | `illust` | 回憶段：C 在夏天的小徑上拍手毬、張口唱歌，暖金色光。 | chizuru_sing, bg_path_summer | main（手毬歌 強調） |
| 11 | 71.98–76.06 | 声をこの胸に響かせて | `illust` | S 胸上，手按胸口、閉眼；水彩圈從她胸口一圈圈暈開。最後一拍停住（溜め）。 | sayo_hand_chest, bg_path_present | main |

### Chorus 1 b33–42 ・ 現在段，落葉全開

| # | 時間 | 歌詞 | 場景 | 內容 | 素材 | 字 |
|---|---|---|---|---|---|---|
| 12 | 76.06–78.49 | 舞い散る落ち葉は、 | `illust` | b33 全景：滿天落葉一起落下，S 小小站在小徑中央的背影。 | sayo_back_lookup, bg_path_present | main |
| 13 | 78.49–80.78 | ひらひらと | `illust` | S 上半身仰望，落葉從鏡頭前擦過（前景葉）。 | sayo_lookup, bg_canopy | main |
| 14 | 80.78–85.49 | 緑と紅、つがいの楓! | `leaves` pair | **招牌 3**：b35 紅綠兩片葉在畫面中央互繞一圈，背後是淡淡的楓林。 | prop_leaf_red/green, bg_path_present | キメ |
| 15 | 85.49–87.84 | 木枯らしが、 | `illust` | 一陣強風：S 全身，紅緞帶與長髮被吹得橫飛，葉子成橫線掠過。 | sayo_wind, bg_path_present | main |
| 16 | 87.84–90.17 | 連れ去るひとひら | `leaves` solo | 一片綠楓被風捲起，往上飛出畫面。 | prop_leaf_green, bg_sky_overcast | main |
| 17 | 90.17–93.19 | 見上げた空には | `illust` | S 背影仰望天空，鏡頭往上搖。 | sayo_back_lookup, bg_sky_overcast | main |
| 18 | 93.19–97.90 | 片時雨 | `illust`＋`katashigure` fx | **招牌 4**：b40 天空一半晴一半雨，雨線只落在一側；長音延到 b42。 | bg_sky_overcast | キメ |

### Interlude 1 b42–49 ・ 回憶段（完整）

| # | 時間 | 歌詞 | 場景 | 內容 | 素材 | 字 |
|---|---|---|---|---|---|---|
| 19 | 97.90–102.61 (b42–44) | — | `illust` | `ink` 轉場進夏天：同一條小徑，嫩綠與暖金，兩人並肩走的背影。 | sayo_walk_back, chizuru_walk_back, bg_path_summer | — |
| 20 | 102.61–104.97 (b44–45) | — | `illust` | C 笑著拍手毬。 | chizuru_bounce, bg_path_summer | — |
| 20b | 104.97–107.31 (b45–46) | — | `illust` | S 看著她微笑。（原本是 `panels` 兩格；panels 每拍會閃一格負片，不適合這首歌，改成兩個單鏡） | sayo_smile, bg_path_summer | — |
| 21 | 107.31–110.84 (b46–47.5) | — | `illust` | 石階上並坐，綠楓樹下。 | sayo_sit, chizuru_sit, bg_steps_summer | — |
| 22 | 110.84–112.02 | — | `illust` | 特寫：兩隻手各拿一片葉（C 綠、S 紅），對著陽光並在一起——つがいの楓的由來。 | hands_two_leaves | — |
| 23 | 112.02–114.37 (b48–49) | — | `illust` | 回憶畫面被雨打濕，顏色慢慢褪成灰藍，回到現在。（`ref` melt 會變成霓虹藍，改用雨＋褪色） | hands_two_leaves | — |

### Verse 2 b49–57 ・ 現在段

| # | 時間 | 歌詞 | 場景 | 內容 | 素材 | 字 |
|---|---|---|---|---|---|---|
| 24 | 114.34–118.43 | 風が木々を揺らして、 | `illust` | 楓林全景，風搖樹梢，鏡頭橫搖。 | bg_path_present | main |
| 25 | 118.43–123.81 | 交わりを歌えば | `illust` | 和 21 同構圖：石階上只剩 S 一人，身旁空著。 | sayo_sit, bg_steps_autumn | main |
| 26 | 123.81–127.78 | 貴女の歌声が、 | `illust`＋`songLeaves` fx | S 臉部特寫，閉眼聆聽；手毬歌的手寫假名像落葉一樣在她周圍飄落。 | sayo_listen（不透明 16:9） | main |
| 27 | 127.78–133.19 | 胸の奥に響いてきます | `illust` | S 手按胸口（重用 11，構圖改成側面中景），水彩圈暈開。 | sayo_hand_chest, bg_steps_autumn | main |

### Pre-chorus 2 b57–65 ・ 時雨

| # | 時間 | 歌詞 | 場景 | 內容 | 素材 | 字 |
|---|---|---|---|---|---|---|
| 28 | 133.22–137.93 | 言えない恋は その胸に | `iienai` | **招牌 5**：b57 灰藍和紙上，「言えない」直排筆文字一筆一筆打下，旁邊小字「恋は　その胸に」，然後被雨滴化開。 | bg_washi | 場景排字（不用 JIZURA，避免關鍵詞出現兩次） |
| 29 | 137.93–142.53 | 癒えない傷を 重ねたね | `iienai` | b59「癒えない」，同上。 | 同上 | 同上 |
| 30 | 142.53–147.26 | 消えない愛よ 叶うなら | `iienai` | b61「消えない」，同上；三個字最後並排，全部被雨水化開。 | 同上 | 同上 |
| 31 | 147.26–151.36 | せめてこの歌を響かせて | `illust` | S 胸上，在雨中輕聲唱，髮梢滴水。最後一拍溜め。 | sayo_sing_rain, bg_path_rain | main |

### Chorus 2 b65–73 ・ 現在段＋時雨，只剩紅楓

| # | 時間 | 歌詞 | 場景 | 內容 | 素材 | 字 |
|---|---|---|---|---|---|---|
| 32 | 151.36–153.70 | 舞い散るひとひら、 | `illust` | 雨中的小徑全景，S 小小的背影；落葉混在雨裡。 | sayo_back_lookup, bg_path_rain | main |
| 33 | 153.70–156.16 | ひらひらと | `leaves` solo | 雨中只有一片紅楓落下，看不到綠楓。 | prop_leaf_red, bg_path_rain | main |
| 34 | 156.16–158.49 | 今も口ずさむ | `illust` | 褪色的手毬躺在雨中的小徑邊。 | prop_temari_faded, bg_path_rain | main |
| 35 | 158.49–160.87 | 手毬歌! | `illust` | S 閉眼哼唱（重用 06，加雨），キメ。 | sayo_hum, bg_path_rain | キメ |
| 36 | 160.87–162.05 | 詠い、 | `illust` | S 在雨中唱。 | sayo_sing_rain, bg_path_rain | main |
| 36b | 162.05–163.51 | 詠え、 | `illust` | 手中的褪色手毬。 | hands_temari_faded | main |
| 36c | 163.51–165.49 | 詠う想いを | `illust` | S 閉眼的臉。（三個字的起點取自 `analysis/lyrics.json`） | sayo_listen | main |
| 37 | 165.49–170.84 | この歌に隠して、袖時雨 | `illust` | S 用袖子遮住臉，雨落在袖上；キメ「袖時雨」。 | sayo_sleeve, bg_path_rain | キメ |

### Break b73–79 ・ 時雨（最灰）

| # | 時間 | 歌詞 | 場景 | 內容 | 素材 | 字 |
|---|---|---|---|---|---|---|
| 38 | 170.84–180.25 (b73–77) | — | `illust` | 全片最長、最灰的靜止鏡頭：S 在雨中的小徑上蹲下，抱著膝。極慢推近。 | sayo_crouch, bg_path_rain | — |
| 39 | 180.25–184.96 (b77–79) | — | `illust` | 特寫：S 手中的褪色手毬，雨滴落在上面。 | hands_temari_faded | — |

### Build b79–82 ・ 一點光

| # | 時間 | 歌詞 | 場景 | 內容 | 素材 | 字 |
|---|---|---|---|---|---|---|
| 40 | 184.96–189.66 (b79–81) | — | `illust` | 雨雲的天空，雨勢變細；雲縫透出一道光。 | bg_sky_rain | — |
| 41 | 189.66–191.92 (b81–82) | — | `illust` | S 臉旁，雨變慢；一片綠楓飄進畫面（Chorus 1 之後第一次出現綠楓）。 | sayo_crouch（裁切）, prop_leaf_green | — |

### Bridge b82–89 ・ 雲開

| # | 時間 | 歌詞 | 場景 | 內容 | 素材 | 字 |
|---|---|---|---|---|---|---|
| 42 | 191.92–198.75 | 泣かないで、顔上げて、 | `illust` | **招牌 6**：S 抬起頭，臉上有淚；千鶴的話用手寫字從她身後穿過（文字在角色後方）。 | sayo_lookup_tears, bg_sky_rain | 手寫（後層） |
| 43 | 198.75–201.43 | この空で、 | `illust` | 天空，雲開始散開。 | bg_sky_open | 手寫 |
| 44 | 201.43–206.06 | あなたを、 | `illust` | b86（全曲最大能量跳升）雲完全打開，C 在光裡，往下看、伸出手；半透明＋光暈。 | chizuru_float, bg_sky_open | 手寫 |
| 45 | 206.06–207.82 | 見ているわ | `illust` | C 臉部特寫，溫柔地笑。 | chizuru_smile | 手寫キメ |

### Last chorus b89–97 ・ 紅楓全滿

| # | 時間 | 歌詞 | 場景 | 內容 | 素材 | 字 |
|---|---|---|---|---|---|---|
| 46 | 207.82–215.55 (b89–92) | 染まり逝く、木々のように赤く / この胸に散る楓、ひとひら! | `seq` 3D-B | **招牌 7**：鏡頭在密集落下的紅楓中穿梭（全彩紅楓第一次出現），每個小節頭加速；「楓」（214.91）那拍颳起一陣風，葉子朝鏡頭撲來、鏡頭仰向樹冠。キメ「楓」由 JIZURA 打（離鏡頭結尾只剩 0.6 s，不另做 3D 字）。 | blender/renders/stormB | main＋キメ |
| 47 | 215.55–221.94 | 木枯らしに抱かれ眠りたい | `illust`＋`leafLine` fx | 地上的 S 伸手向上，天上的 C 伸手向下；落葉在兩人之間連成一條線，沿線往上流。 | sayo_reach_up, chizuru_reach_down, bg_forest_red, bg_sky_open | main |
| 48 | 221.94–226.68 | 胸に散らす紅時雨! | `illust` | **招牌 8**：b95 紅葉像驟雨一樣直落，S 全力唱，紅緞帶飛揚；キメ「紅時雨」。 | sayo_sing_power, bg_forest_red | キメ |

### Coda b97–105 ・ 時雨 → 風花

| # | 時間 | 歌詞 | 場景 | 內容 | 素材 | 字 |
|---|---|---|---|---|---|---|
| 49 | 226.68–231.35 | 風は歌う、秋風恋歌! | `leaves` pair | 標題句：和紙上兩片葉再一次互繞，這次一起往上；「秋風恋歌」筆文字大字。 | prop_leaf_red/green, bg_washi | キメ |
| 50 | 231.35–236.07 | 時雨はいつしか、風花に | `illust`＋`kazahana` fx | **招牌 9**：雨線在空中慢下來、變白、化成風花；S 仰望微笑。 | sayo_smile_snow, bg_path_snow | main（風花 強調） |
| 51 | 236.07–240.80 | 風に吹かれ消える想いは | `illust` | C 在風花裡微笑揮手，身影隨風花慢慢散去。 | chizuru_wave, bg_path_snow | main |
| 52 | 240.80–245.84 | 私を濡らしてゆく、恋しぐれ! | `illust` | S 臉部特寫，臉頰上一滴淚和一片雪；她笑了。キメ「恋しぐれ」。 | sayo_tear_smile（不透明 16:9） | キメ |

### Outro b105–118＋尾巴 ・ 風花 → 白

| # | 時間 | 歌詞 | 場景 | 內容 | 素材 | 字 |
|---|---|---|---|---|---|---|
| 53 | 245.84–255.55 (b105–109) | — | `illust`＋`kazahana` | 雪中的小徑全景，S 往前走遠的背影，風花越來越密。 | sayo_walk_back, bg_path_snow | — |
| 54 | 255.55–264.96 (b109–113) | — | `illust` | 畫面慢慢轉白（風花覆蓋一切）。 | bg_path_snow | — |
| 55 | 264.96–272.02 (b113–116) | — | `oshiba` | **招牌 10**：白色和紙上，一對押し葉（紅楓與綠楓）像墨透出來一樣慢慢浮現。 | prop_oshiba | — |
| 56 | 272.02–276.72 (b116–118) | — | `oshiba` | 押し葉旁淡淡出現小標題「秋風恋歌」。 | 同上 | 場景排字 |
| 57 | 276.72–280.12 (b118–end) | — | `oshiba` card | 片尾字卡：「原曲：秋風恋歌 / DeZI：R」「制作：Claude Opus 5.5」。 | 同上 | 場景排字 |
| 58 | 280.12–283.12 | — | `oshiba` hold | 音樂在 280.12 停，畫面停在這一頁 3 秒後結束。 | 同上 | — |

## 需要新寫的場景與 fx

| 名稱 | 用在 | 做什麼 |
|---|---|---|
| `leaves`（scene，`pair` / `part` / `solo`） | 01 02 14 16 33 49 | 葉子 sprite 沿落葉弧線（左右擺盪＋翻面）飄落；pair 模式兩片互繞 |
| `leaves`（fx，給 `illust` 用） | 05 06 12 13 15 24 32 46 48 | 背景／前景的落葉群，可設紅綠比例、密度、風向、雨中模式 |
| `katashigure`（fx） | 18 | 雨只落在畫面一側，另一側有陽光 |
| `songLeaves`（fx） | 26 | 手毬歌的手寫假名像落葉般飄落 |
| `iienai`（scene） | 28–30 | 直排筆文字逐筆寫出，再被雨滴暈開 |
| `leafLine`（fx） | 47 | 兩點之間沿曲線流動的葉子 |
| `kazahana`（fx） | 50 53 54 | 雨線減速、變白、變成雪片 |
| `oshiba`（scene） | 55–58 | 和紙＋押し葉浮現＋片尾字卡 |
| 標題（`seq` 的文字層） | 03 | 筆文字逐筆寫出「秋風恋歌」＋副標＋原曲署名 |
| 轉場 `ink` | 08 19 | 現有；顏色改成水彩 |

## 素材清單（由分鏡推出）

**小夜**（附 `REF_sayo.png`，綠鍵）：sayo_walk_back、sayo_hum、hands_temari_faded（不透明 16:9）、sayo_side_leaf、sayo_hand_chest、sayo_back_lookup、sayo_lookup、sayo_wind、sayo_smile、sayo_sit、sayo_listen（不透明 16:9）、sayo_sing_rain、sayo_sleeve、sayo_crouch、sayo_lookup_tears、sayo_reach_up、sayo_sing_power、sayo_smile_snow、sayo_tear_smile（不透明 16:9）— 19 張

**千鶴**（附 `REF_chizuru.png`，洋紅鍵）：hands_temari_new（不透明 16:9）、chizuru_sing、chizuru_walk_back、chizuru_bounce、chizuru_sit、chizuru_float、chizuru_smile、chizuru_reach_down、chizuru_wave — 9 張

**兩人**：hands_two_leaves（不透明 16:9，附兩張定稿）— 1 張

**背景**（不透明 16:9，無人物、無文字）：bg_washi、bg_path_present、bg_path_summer、bg_path_rain、bg_path_snow、bg_canopy、bg_sky_overcast、bg_sky_rain、bg_sky_open、bg_steps_summer、bg_steps_autumn、bg_forest_red — 12 張
同一條小徑的四季版本（summer / present / rain / snow）要同構圖、同光源方向。

**道具**（透明）：prop_leaf_red ×3 款、prop_leaf_green ×3 款（洋紅鍵）、prop_temari_faded、prop_temari_new（洋紅鍵）、prop_oshiba（不透明）— 9 張

共約 50 張。困難姿勢（sayo_crouch、chizuru_float、sayo_reach_up、chizuru_reach_down、sayo_sleeve）各生兩版。

## 3D（Blender）

- **3D-A 小徑長鏡頭**（03–04，17.90–48.49，約 30.6 s）：石板小徑、兩側楓樹、落葉；現在段調色（褪色朽葉紅褐）。卡通渲染＋線稿，與水彩插畫一致。
- **3D-B 紅楓漫天**（46，207.82–215.55，約 7.7 s）：鏡頭在大量落下的紅楓中穿梭；全彩紅楓。

腳本 `blender/shots/pathA.py`、`stormB.py`（共用 `ak_common.py`）：EEVEE 卡通材質＋GP 線稿；樹冠與落葉是楓葉素材 `prop_leaf_red_*` 貼在半透明卡片上（幾萬片，Geometry Nodes 實例化），所以葉子和 2D 畫面同一種筆觸。3D-A 隔格渲染（459 張，engine 以 15 fps 播），3D-B 全 30 fps（230 張）；都是 960×540，由 engine 放大加 boil／grain。小夜（s04）與飄落葉 fx 由 engine 的 `seqx` 場景疊在 3D 畫面上。
重渲：`blender -b --factory-startup -P blender/shots/pathA.py -- --mode full --res 50`（stormB 同）。
