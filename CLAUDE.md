# tomangchi-lab.github.io — 토망치랩 통합 작업장

이 레포는 **배포물과 제작 영역이 한 폴더에 공존**한다. 둘의 취급이 다르다.

| 영역 | 경로 | git |
|---|---|---|
| 배포물 (공개) | `index.html`, `kits/`, `assets/`, `.nojekyll`, `README.md` | **추적·공개** — GitHub Pages가 그대로 서빙 |
| 제작 영역 (로컬 전용) | `workshop/` | **`.gitignore`로 무시** — 절대 공개되지 않음 |

`workshop/`은 2026-08-06에 `C:\토망치`에서 통째로 이전한 제작 폴더다
(브랜드에셋·발행완료·제작중·소재큐·키트 원문·인사이트·A콘텐츠 출력·렌더 스크립트).
구조와 세부 규칙은 `workshop/README.md`, 콘텐츠 제작 규칙은 스킬 정본
`~/.claude/skills/tomangchi/SKILL.md`를 따른다.

## 금지 사항

- **`.gitignore`에서 `workshop/`을 제거하지 말 것.** 원본 소재·녹화·미발행 자산이 전부 공개 저장소로 올라간다.
- **`kits/` 안의 파일을 삭제하거나 이름을 바꾸지 말 것.** 구 주소 `ohjaejuno.github.io/kits/*`의
  리다이렉트와 기존 Manychat DM 링크가 이 파일명을 직접 참조한다. 내용 수정은 자유, 경로 변경은 링크 파손.
- 브랜드 토큰(`:root` CSS 변수)은 전 페이지 동일 값 유지 — 한 곳만 고치지 말 것 (`README.md` 표 참조).

## 워크플로우

- **`main` 직접 푸시가 정상 워크플로우.** Pages 배포 브랜치이며 빌드 단계가 없다. PR·피처 브랜치 불필요.
- 키트 추가: `kits/`에 새 HTML → `index.html`의 `.grid`에 카드 추가 → 커밋 → push.
- 제작 산출물은 `workshop/` 안에서만 생성한다. 배포할 것만 레포 루트로 올린다.
- 폰 업로드용 `OneDrive\토망치_전달함` 워크플로우는 이번 이전과 무관 — 그대로 유지.

## 커밋

conventional prefix는 영어, 본문은 한국어.

```
feat: cyber-eval 키트 한국어 요약 추가
fix: 키트 인덱스 카드 링크 수정
chore: workshop 제작 영역 git 제외
```

## 프로젝트 정리

Orca의 기존 "토망치" 프로젝트는 **이 레포 프로젝트로 대체됨**. 토망치랩 관련 작업은 전부 여기서 한다.
