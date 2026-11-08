# -*- coding: utf-8 -*-
"""PER-SONG DATA: the reconciled lyric line table + song metadata used by the transcribe_*.py tools.

This copy holds 秋風恋歌 (DeZI：R). For another song REPLACE everything in this file
(keep the names): LINES (one entry per sung line, official text + hiragana reading + a rough start from a
Whisper pass), SONG, START_OVERRIDE / MORA_OVERRIDE (empty until you verified an onset by ear) and SCORE_TESTS.
Translations / hand-checked romaji live in transcribe_translation.py.

Each LINES entry: (text, reading_hiragana, section, approx_start_from_whisper, confidence, alternatives, note)
Text is the official lyric (analysis/lyrics_official.txt) without punctuation, phrases separated by ASCII spaces;
approx starts come from one faster-whisper large-v3 pass on the Kim vocal stem; uncertain readings were settled with
forced-decoding scores (tools/transcribe_score.py, SCORE_TESTS below).

  python tools/transcribe_lines.py      print the table (index, start, section, text, reading)
Author: NikusonP -- vocaloid-style-mv-pipeline, MIT licence.
"""

LINES = [
    # ---- Verse 1 ----
    ("二人歩いた小径 ひとり 歩いています", "ふたりあるいたこみち ひとり あるいています", "verse1", 38.30, 0.95, [], ""),
    ("風に揺れる葉の音 ひとり 歌を 口ずさみます", "かぜにゆれるはのおと ひとり うたを くちずさみます", "verse1", 47.28, 0.90, [], "Whisper heard 波紋と / 人に"),
    # ---- Pre-chorus 1 ----
    ("手鞠花 色あせるように", "てまりばな いろあせるように", "pre1", 57.16, 0.85, ["色褪せぬように"], "official spelling 色あせるやうに (sung よう; kept in analysis/lyrics_mv.lrc); forced scoring split: ばな wins on the stem, はな on centre (both within noise)"),
    ("この想い 消え逝く前に", "このおもい きえゆくまえに", "pre1", 61.30, 0.95, [], ""),
    ("手毬歌 歌う貴女の", "てまりうた うたうあなたの", "pre1", 66.06, 0.95, [], ""),
    ("声をこの胸に 響かせて", "こえをこのむねに ひびかせて", "pre1", 70.86, 0.97, [], ""),
    # ---- Chorus 1 ----
    ("舞い散る落ち葉は ひらひらと", "まいちるおちばは ひらひらと", "chorus1", 75.32, 0.97, [], ""),
    ("緑と紅 つがいの楓", "みどりとくれない つがいのかえで", "chorus1", 80.26, 0.80, ["緑とべに"], "forced scoring: くれない -41.2 vs べに -52.3 (vocal stem), same order on centre"),
    ("木枯らしが 連れ去るひとひら", "こがらしが つれさるひとひら", "chorus1", 84.70, 0.93, [], ""),
    ("見上げた空には 片時雨", "みあげたそらには かたしぐれ", "chorus1", 90.58, 0.90, [], ""),
    # ---- Verse 2 ----
    ("風が木々を揺らして 交わりを歌えば", "かぜがきぎをゆらして まじわりをうたえば", "verse2", 114.12, 0.90, [], ""),
    ("貴女の歌声が 胸の奥に響いてきます", "あなたのうたごえが むねのおくにひびいてきます", "verse2", 123.02, 0.97, [], ""),
    # ---- Pre-chorus 2 ----
    ("言えない恋は その胸に", "いえないこいは そのむねに", "pre2", 132.78, 0.97, [], ""),
    ("癒えない傷を 重ねたね", "いえないきずを かさねたね", "pre2", 136.96, 0.93, [], ""),
    ("消えない愛よ 叶うなら", "きえないあいよ かなうなら", "pre2", 141.30, 0.93, [], ""),
    ("せめてこの歌を 響かせて", "せめてこのうたを ひびかせて", "pre2", 146.04, 0.95, [], ""),
    # ---- Chorus 2 ----
    ("舞い散るひとひら ひらひらと", "まいちるひとひら ひらひらと", "chorus2", 150.60, 0.95, [], ""),
    ("今も口ずさむ 手毬歌", "いまもくちずさむ てまりうた", "chorus2", 155.54, 0.93, [], ""),
    ("詠い 詠え 詠う想いを", "うたい うたえ うたうおもいを", "chorus2", 159.70, 0.90, [], "Whisper hears 歌い 歌え 歌う: 詠 sung うた"),
    ("この歌に隠して 袖時雨", "このうたにかくして そでしぐれ", "chorus2", 164.94, 0.95, [], ""),
    # ---- Bridge ----
    ("泣かないで 顔上げて", "なかないで かおあげて", "bridge", 192.72, 0.85, [], "Whisper heard 泣いた 溶けた"),
    ("この空で あなたを 見ているわ", "このそらで あなたを みているわ", "bridge", 197.06, 0.80, [], "long line with gaps; あなたを 202.05 s, 見ているわ 206.06 s (mora times, each after a breath gap in the vocal stem)"),
    # ---- Final chorus ----
    ("染まり逝く 木々のように赤く", "そまりゆく きぎのようにあかく", "chorus3", 207.30, 0.93, [], ""),
    ("この胸に散る 楓 ひとひら", "このむねにちる かえで ひとひら", "chorus3", 211.84, 0.93, [], ""),
    ("木枯らしに抱かれ 眠りたい", "こがらしにだかれ ねむりたい", "chorus3", 216.60, 0.85, [], "forced scoring tie: だかれ -37.3 / いだかれ -38.9 (stem), -31.6 / -31.7 (centre)"),
    ("胸に散らす 紅時雨", "むねにちらす くれないしぐれ", "chorus3", 221.26, 0.80, [], "Whisper heard 紅いシグネ; forced scoring: くれない -23.5 vs べに -44.2"),
    # ---- Outro ----
    ("風は歌う 秋風恋歌 時雨はいつしか 風花に", "かぜはうたう あきかぜれんか しぐれはいつしか かざはなに", "coda", 226.04, 0.80, [], "forced scoring: あきかぜれんか -19.6 vs しゅうふうれんか -45.8"),
    ("風に吹かれ消える想いは 私を濡らしてゆく 恋しぐれ", "かぜにふかれきえるおもいは わたしをぬらしてゆく こいしぐれ", "coda", 235.42, 0.93, [], "onset verified; mora times after 240.2 s are unreliable (the last MMS window ends at approx start + 6 s = 241.4 s, the line runs to ~245 s). 私を starts ~240.80 (breath gap 240.50-240.75)"),
]

# ---- song metadata for transcribe_reconcile.py (LRC title, lyrics_sections.json notes) ----
SONG = dict(
    title="秋風恋歌",
    language="ja",
    wordless_vocal_regions=[
        dict(start=17.9, end=39.0, desc="vocal stem active under the band intro but no words in the Whisper pass: humming or lead-instrument bleed (unconfirmed)"),
        dict(start=252.0, end=270.0, desc="vocal stem ~-19 dB but no words in the Whisper pass: wordless vocal or lead-instrument bleed (unconfirmed)"),
    ],
    instrumental_breaks=[],   # band drop-outs under a sung line: none found (interludes are in analysis/sections.json)
)

# ---- manual onset fixes for transcribe_reconcile.py (line index -> (start, source) / {mora index: start}) ----
# Lines where MMS_FA's first mora is clearly wrong:
#  7  緑と紅 : first morae score 0.001 / 0.02 at 80.44; vocal stem dips to -34 dB 80.50-80.75 and the line rises at 80.80
START_OVERRIDE = {7: (80.78, "manual")}
MORA_OVERRIDE = {}

# ---- reading tests for transcribe_score.py: (name, clip_start, clip_end, [candidate texts]) ----
SCORE_TESTS = [
    ("temari_bana", 56.7, 61.4, ["てまりばな いろあせるように", "てまりはな いろあせるように", "手鞠花 色あせるように"]),
    ("midori_beni", 79.8, 84.8, ["みどりとくれない つがいのかえで", "みどりとべに つがいのかえで",
                                 "みどりとあか つがいのかえで", "みどりとこう つがいのかえで"]),
    ("dakare", 216.2, 221.4, ["こがらしにだかれ ねむりたい", "こがらしにいだかれ ねむりたい"]),
    ("beni_shigure", 220.8, 226.2, ["むねにちらす くれないしぐれ", "むねにちらす べにしぐれ", "むねにちらす あかしぐれ"]),
    ("title", 225.6, 230.8, ["かぜはうたう あきかぜれんか", "かぜはうたう しゅうふうれんか", "かぜはうたう あきかぜこいうた"]),
]


if __name__ == "__main__":
    import argparse
    import sys
    argparse.ArgumentParser(description="Print the per-song lyric line table (see the module docstring).").parse_args()
    sys.stdout.reconfigure(encoding="utf-8")
    print(f"{SONG.get('title', '?')}: {len(LINES)} lines")
    for i, (text, reading, sec, st, conf, *_rest) in enumerate(LINES):
        print(f"{i:3d} {st:7.2f}  {sec:10s} {conf:.2f}  {text}  ({reading})")
