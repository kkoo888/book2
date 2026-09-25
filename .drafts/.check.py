import re, sys, os, glob

BAN = ["他心中暗道","此乃","阁下","在下","感到一阵","眼神里有","心里有一种说不出",
       "深吸一口气","一股强大的气势","这就是","故事还在继续","他自言自语","他的使命","他的人生"]
BAN_SOFT = {"眼神里":0, "心里":3, "他摇了摇头":2, "他笑了笑":2, "他叹了口气":1, "嘴角微微上扬":1}
EMOJI = re.compile("[\U0001F000-\U0001FAFF\u2600-\u27BF\u2B00-\u2BFF]")

def count_body(text):
    lines = text.splitlines()
    body = "\n".join(lines[1:])
    return len(re.sub(r"\s", "", body))

rows = []
all_titles = set()
for f in sorted(glob.glob("book2/chapters/*.md")):
    with open(f, encoding="utf-8") as fh:
        t = fh.readline().strip()
    all_titles.add(t)

for n in range(166, 178):
    p = f"book2/.drafts/第{n}章.md"
    if not os.path.exists(p):
        print(f"{n}: MISSING")
        continue
    txt = open(p, encoding="utf-8").read()
    lines = txt.splitlines()
    title = lines[0].strip() if lines else ""
    body = "\n".join(lines[1:])
    wc = count_body(txt)
    bans = {w: body.count(w) for w in BAN if body.count(w)}
    soft = {w: body.count(w) for w, lim in BAN_SOFT.items() if body.count(w) > lim}
    soft_counts = {w: body.count(w) for w in BAN_SOFT}
    excl = body.count("！") + body.count("!")
    emo = EMOJI.findall(body)
    dup = title in all_titles
    # title length (after 第XXX章 )
    m = re.match(r"# (第\d+章) (.+)", title)
    tlen = len(m.group(2)) if m else -1
    para = max((len(l) for l in body.splitlines() if l.strip()), default=0)
    ok = (2250 <= wc <= 2550) and not bans and not soft and excl <= 5 and not emo and not dup and tlen <= 15
    print(f"{n} | 字数={wc} | 标题='{title}' 标题字数={tlen} 重复={dup} | 禁词={bans} | 软限={soft_counts} | 感叹号={excl} | emoji={len(emo)} | 最长段={para}字 | {'OK' if ok else 'FAIL'}")
