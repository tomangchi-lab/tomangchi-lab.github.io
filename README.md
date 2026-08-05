# tomangchi-lab.github.io

토망치랩(@ai_tomangchi.lab) 키트 페이지. 인스타 댓글 CTA → Manychat DM으로 안내하는 자료 모음.

## 구조

```
/                    인덱스 — 키트 모음 랜딩
/kits/*.html         키트 페이지 (정적 HTML, 각 파일에 CSS 인라인)
/assets/             로고 등 브랜드 에셋
```

빌드 없음. main 브랜치 루트를 GitHub Pages가 그대로 서빙한다.

## 브랜드 토큰

각 페이지 `:root`에 동일하게 선언한다. 값 변경 시 전 페이지를 함께 고칠 것.

| 토큰 | 값 | 용도 |
|---|---|---|
| `--cream` | `#FCF8F0` | 배경 |
| `--ink` | `#1C2028` | 본문·헤더 |
| `--cyan` | `#34DCE6` | 브랜드 액센트 |
| `--cyan-d` | `#1E8C96` | 밝은 배경 위 시안 텍스트 |
| `--coral` | `#D97757` | 경고·균형 문장 |
| `--line` | `#EBE4D7` | 테두리 |
| `--gray` | `#787E88` | 보조 텍스트 |

## 키트 추가하기

1. `kits/` 안의 기존 페이지를 복사해 새 파일 생성 (템플릿은 `canva.html` 기준)
2. `index.html`의 `.grid`에 카드 한 장 추가
3. 커밋 → push → Actions 배포 자동

## 구 주소

이전에는 `ohjaejuno.github.io/kits/*.html`에서 서빙했다. 기존 Manychat DM 링크 보호를 위해
구 경로는 삭제하지 않고 meta refresh 리다이렉트만 심어 뒀다.
