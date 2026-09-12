# -*- coding: utf-8 -*-
"""킷 목록을 `kits/*.html` 에서 **생성한다** — 손으로 적지 않는다.

🔴 **왜 만들었나 (2026-09-13).** `index.html` 의 카드가 손으로 쓴 HTML 이라 킷을 새로
   올릴 때 아무도 같이 안 고쳤다. 실측: 디스크에 킷 **35개**인데 목록에 링크된 것이
   **10개**였고, `index.html` 마지막 수정이 **2026-08-20**(24일 전)이었다.
   그 사이 만든 킷 25개가 프로필 링크에서 **아예 닿지 않았다** — 인스타 바이오가
   「DM 못 받았다면 킷 모음 ↓」이라고 가리키는 바로 그 대체 경로다.

   정관 §0 4층 ①: 검사로 「목록에 빠진 킷 있나」를 재는 것이 아니라, **목록이 파일에서
   나오게** 해서 빠질 수가 없게 만든다. 파일이 있으면 목록에 있다.

**무엇을 어디서 읽나 (실물이 정본이다 · §0)**
- 아이콘·제목: 킷 페이지의 `<title>` (`🧰 내 AI 하네스 점검표 — 토망치랩` 꼴)
- 설명: `<meta name="description">` → 없으면 `og:description` → 없으면 `FALLBACK_DESC`
- 순서: **그 파일이 처음 커밋된 날**(`git log --diff-filter=A`) 기준 최신순

🔴 **꾸미기가 없다고 킷이 빠지지는 않는다.** 설명이 비어도 카드는 나온다 — 빠지는 쪽으로
   틀리면 이 파일을 만든 이유가 사라진다.
"""
import glob
import html
import io
import os
import re
import subprocess
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
INDEX = os.path.join(ROOT, "index.html")
BEGIN, END = "<!-- KITS:BEGIN -->", "<!-- KITS:END -->"
DEFAULT_ICO = "🔨"

#: description 이 아예 없는 옛 킷 7개. 🔴 **여기 없다고 목록에서 빠지지 않는다** —
#: 설명만 비고 카드는 그대로 난다(빠지는 쪽으로 틀리지 않게).
FALLBACK_DESC = {
    "ai-opportunities.html": "지금 신청할 수 있는 AI 크레딧·체험판·공모를 한 장에. 계속 갱신합니다.",
    "canva.html": "캔바 AI 기능을 무료로 어디까지 쓰는지, 어떤 작업에 쓸 만한지 정리본.",
    "claude-skills-start.html": "Claude 스킬을 처음 만들 때 필요한 최소 구성과 예시 파일.",
    "cyber-eval.html": "AI 보안 평가 항목을 우리 기준으로 옮긴 표. 무엇을 재고 무엇을 못 재는지까지.",
    "gpt100.html": "조건 체크리스트 + X 포스트 템플릿 3종 + 제출 방법.",
    "orca.html": "Orca 브라우저를 AI 작업용으로 세팅하는 순서와 손에 익는 단축키.",
    "qwen38max.html": "Qwen3.8-Max 를 무료로 써보는 경로와 한국에서 막히는 자리.",
}


def meta(path):
    """킷 페이지 한 장에서 (아이콘, 제목, 설명)."""
    t = io.open(path, encoding="utf-8").read(4000)

    def grab(pat):
        m = re.search(pat, t, re.S)
        return html.unescape(m.group(1).strip()) if m else ""

    title = grab(r"<title>(.*?)</title>")
    #: 꼬리표 «— 토망치랩» · «| 토망치랩» 를 뗀다 — 카드에서는 되풀이다.
    title = re.sub(r"\s*[—|·]\s*토망치랩\s*$", "", title).strip()
    #: 앞머리 이모지를 아이콘으로 뗀다. 없으면 기본값.
    m = re.match(r"^([^\w\s\d]+(?:️)?)\s+(.*)$", title)
    ico, title = (m.group(1), m.group(2).strip()) if m else (DEFAULT_ICO, title)

    desc = (grab(r'<meta name="description" content="(.*?)"')
            or grab(r'<meta property="og:description" content="(.*?)"')
            or FALLBACK_DESC.get(os.path.basename(path), ""))
    return ico, title, desc


def added(path):
    """그 파일이 **처음 커밋된** ISO 날짜. 못 읽으면 빈 문자열(맨 뒤로 간다)."""
    out = subprocess.run(
        ["git", "-C", ROOT, "log", "--diff-filter=A", "--format=%ad", "--date=short",
         "--", os.path.relpath(path, ROOT).replace("\\", "/")],
        capture_output=True, text=True).stdout.strip().splitlines()
    return out[-1] if out else ""


def cards(paths):
    out = []
    for i, p in enumerate(paths):
        ico, title, desc = meta(p)
        rel = "kits/" + os.path.basename(p)
        pill = '<span class="pill live">NEW</span>' if i < 3 else ""
        out.append(
            '  <a class="kit" href="%s">\n'
            '    <div class="row"><span class="ico">%s</span><div>\n'
            '      <div class="tt">%s</div>\n'
            '      <div class="ds">%s</div>\n'
            '    </div></div>\n'
            '    <div class="meta">%s<span class="go">열어보기 →</span></div>\n'
            '  </a>\n'
            % (rel, ico, html.escape(title), html.escape(desc), pill))
    return "\n".join(out)


def kit_files():
    return sorted(glob.glob(os.path.join(ROOT, "kits", "*.html")))


def ordered():
    """최신순. 같은 날이면 이름순으로 **결정적**이게 — 안 그러면 빌드마다 diff 가 난다."""
    return sorted(kit_files(), key=lambda p: (added(p), os.path.basename(p)), reverse=True)


def render(text, body, n):
    i, j = text.index(BEGIN), text.index(END)
    #: 리드의 개수도 **센 값**이다 — 손으로 적으면 목록과 갈린다(발행로그 누적 표와 같은 꼴).
    head, cnt = re.subn(r"킷 \d+개", "킷 %d개" % n, text[:i])
    if cnt != 1:
        raise SystemExit("리드에서 «킷 N개» 를 %d 번 찾았다 — 1 이어야 한다" % cnt)
    return head + BEGIN + "\n\n" + body + "\n" + text[j:]


def self_test():
    """🔴 재는 것은 «모든 킷 파일이 목록에 정확히 한 번 나오는가» 하나다."""
    ok = True

    def chk(name, cond, note=""):
        nonlocal ok
        ok = ok and bool(cond)
        print("  %s %s%s" % ("OK  " if cond else "FAIL", name, ("  " + note) if note else ""))

    files = [os.path.basename(p) for p in kit_files()]
    body = cards(ordered())
    miss = [f for f in files if ('href="kits/%s"' % f) not in body]
    dup = [f for f in files if body.count('href="kits/%s"' % f) > 1]
    chk("킷 파일 전부가 목록에 있다", not miss, "%d개 · 누락 %s" % (len(files), miss or 0))
    chk("중복 0", not dup, str(dup or 0))

    # 역검증 — 한 장을 빼면 «누락»으로 잡히는가. 잡지 못하면 위 축이 헛돈다.
    part = cards(ordered()[1:])
    gone = [f for f in files if ('href="kits/%s"' % f) not in part]
    chk("한 장을 빼면 누락으로 잡힌다 (검사가 헛돌지 않는다)", len(gone) == 1, str(gone))

    # 역검증 — 제목·설명이 비어도 **카드는 난다**(빠지는 쪽으로 틀리지 않는다).
    chk("설명이 비어도 카드는 난다", body.count('class="kit"') == len(files),
        "카드 %d / 파일 %d" % (body.count('class="kit"'), len(files)))

    # 순서가 결정적인가 — 두 번 돌려 같아야 한다(빌드마다 diff 가 나면 못 쓴다).
    chk("두 번 돌려 같다 (결정적)", cards(ordered()) == body)

    empty = [os.path.basename(p) for p in kit_files() if not meta(p)[2]]
    chk("설명 없는 킷 0 (없어도 FAIL 아님 — 보고만)", True, "설명 빈 킷: %s" % (empty or 0))
    return ok


def main():
    if "--self-test" in sys.argv:
        raise SystemExit(0 if self_test() else 1)
    if not self_test():                 # 🔴 쓰기 전에 검사한다 (정관 §0)
        raise SystemExit("자체 검사 실패 — index.html 을 쓰지 않았다")
    paths = ordered()
    text = io.open(INDEX, encoding="utf-8").read()
    if BEGIN not in text or END not in text:
        raise SystemExit("index.html 에 %s / %s 표식이 없다" % (BEGIN, END))
    io.open(INDEX, "w", encoding="utf-8").write(render(text, cards(paths), len(paths)))
    print("\nindex.html 갱신 — 킷 %d개 (최신 %s)"
          % (len(paths), os.path.basename(paths[0])))


if __name__ == "__main__":
    main()
