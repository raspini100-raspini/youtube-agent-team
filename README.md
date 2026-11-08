# 유튜브 콘텐츠 에이전트팀 (바이브페이 · 모두플레이)

Claude Code에서 이 폴더를 열면 메인 세션이 **총괄 프로듀서**(CLAUDE.md)가 되어 8명의 전문 에이전트를 지휘합니다.

## 팀 구성
| 에이전트 | 역할 | 산출물 |
|---|---|---|
| trend-researcher | 고충·검색수요·경쟁영상 조사 | research.md |
| content-strategist | 기획안·백로그·캘린더 | brief.md |
| longform-scriptwriter | 8~12분 롱폼 대본 | script.md |
| shorts-producer | 쇼츠 3편 (팁/상황극/BA) | shorts.md |
| thumbnail-designer | 썸네일 3안 + PNG 시안 | thumbnail.md, thumbnail_*.png |
| seo-publisher | 제목·설명·태그·업로드 | metadata.json |
| compliance-reviewer | 사실·광고·세무·저작권 검수 | review.md |
| analytics-analyst | 주간 성과 분석 | analytics/<주>/report.md |

## 시작하기
1. `brands/vibepay.md`, `brands/moduplay.md`의 **[확인 필요]** 사실표 채우기 (수수료, 비사업자 조건, 컬러 등)
2. Claude Code에서: `/new-episode vibepay V2` 또는 `/new-episode moduplay M1`
3. 승인 ①(주제) → 승인 ②(대본·썸네일) → 영상 편집(templates/production-guide.md) → 예약 업로드 → `/weekly-report`

## 업로드 설정 (1회)
```
pip install google-api-python-client google-auth-oauthlib
```
Google Cloud에서 YouTube Data API v3 + OAuth 데스크톱 클라이언트 → `client_secret.json`을 루트에 저장.
`python3 scripts/upload_youtube.py <metadata.json> --dry-run` 으로 먼저 확인.
