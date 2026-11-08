# 썸네일: PG 심사 반려 사유 TOP 7 (V2)
- 에피소드 id: 20261108-pg-reject-top7 / 브랜드: vibepay
- 확정 제목: PG 심사 반려 사유 TOP 7, AI로 만든 사이트는 이것부터 고치세요
- 각도: AI로 만든 사이트의 빈틈을 AI 프롬프트로 고친다

> **주의: 현재 PNG 3장은 단색 그라데이션 시안입니다.** 브랜드 임시 컬러(딥네이비 #111827 → 일렉트릭 퍼플 #7C3AED, 강조 옐로 #FACC15, brands/vibepay.md §7)로 문구·배치만 검증한 것이며, **실사 배경(화면 캡처·인물)은 사람이 나중에 교체**합니다. 교체 시 아래 프롬프트로 배경을 만든 뒤 `--bg 배경.png` 옵션으로 다시 렌더하세요.
> 브랜드 컬러는 §7에서 아직 `[확인 필요]`(임시값)입니다. 확정되면 다시 렌더해야 합니다.

## 문구 설계 원칙 (제목과 겹치지 않게)
제목이 이미 "반려 사유 TOP 7"과 "AI로 만든 사이트"를 말하므로, 썸네일은 제목에 **없는** 정보를 하나씩 맡습니다.
- A: 원인이 코드가 아니라는 반전 (핵심 메시지 1)
- B: 고치는 데 드는 수단과 시간 (핵심 메시지 3)
- C: 반려 사유의 구성, 7개 중 4개는 "없는 페이지" (핵심 메시지 2, 구성표 사유 1~4)

---

## A안: 공포/문제 (반려)
| 항목 | 내용 |
|---|---|
| 파일 | `thumbnail_A.png` |
| 문구 | 1줄 **또 반려?** (흰색) / 2줄 **맨 아래부터** (옐로) |
| 배지 | PG 심사 결과 메일 |
| 구도 | 좌측 55%: 텍스트. 우측 45%: 노트북 화면에 흐릿한 "심사 결과: 반려" 메일 UI와 빨간 반려 도장, 그 앞에 인물 상반신 |
| 인물 표정 | 이마를 짚고 화면을 보며 당황, 입이 살짝 벌어진 "또?" 표정 |
| 핵심 오브젝트 | 빨간 "반려" 도장이 찍힌 이메일 화면 |

배경 이미지 프롬프트 (영문):
```
A frustrated young Korean indie developer in a hoodie, hand on forehead, staring at a laptop in a dim room at night, laptop screen shows a generic email UI with a large red rejection stamp, no readable text, no logos, cool navy and purple ambient light, subject placed on the right third, empty dark space on the left for text, cinematic, shallow depth of field, photorealistic, 16:9, 1280x720
```

## B안: 결과/해결
| 항목 | 내용 |
|---|---|
| 파일 | `thumbnail_B.png` |
| 문구 | 1줄 **AI 프롬프트로** (흰색) / 2줄 **바로 수정** (옐로) |
| 배지 | 프롬프트 7줄 공개 |
| 구도 | 좌측: 텍스트. 우측: AI 코딩 도구 채팅창에 프롬프트 한 줄 → 옆에 완성된 "환불정책" 페이지가 생성되는 Before/After 화면 분할. 인물은 우하단에 작게 |
| 인물 표정 | 안도의 미소, 화면을 가리키며 "됐다" 하는 밝은 표정 |
| 핵심 오브젝트 | 프롬프트 입력창 + 자동 생성된 약관/환불정책 페이지 |

배경 이미지 프롬프트 (영문):
```
Split-screen laptop display: left side a minimal AI chat interface with a single short prompt line, right side a freshly generated clean website policy page with a footer section, no readable text, no brand logos, a relieved smiling young Korean developer pointing at the screen in the lower right, bright purple and electric violet lighting, empty dark navy area on the left third for text, photorealistic, 16:9, 1280x720
```

## C안: 호기심/숫자
| 항목 | 내용 |
|---|---|
| 파일 | `thumbnail_C.png` |
| 문구 | 1줄 **7개 중 4개** (흰색) / 2줄 **빈 페이지** (옐로) |
| 배지 | 심사원 시점 체크 |
| 구도 | 좌측: 텍스트. 우측: 웹사이트 하단(푸터)을 확대한 화면에 빈 칸 4개가 점선/물음표로 표시, 돋보기가 그 위를 비춤. 인물 없이 오브젝트 중심도 가능 |
| 인물 표정 | (사용 시) 돋보기를 든 심사원 역할 인물, 눈을 가늘게 뜬 의심하는 표정 |
| 핵심 오브젝트 | 빈칸이 뚫린 사이트 푸터 + 돋보기 |

배경 이미지 프롬프트 (영문):
```
Close-up of a website footer on a large monitor with four empty placeholder blocks outlined in dashed yellow lines and question marks, a magnifying glass hovering over them, no readable text, no logos, dark navy background with purple glow, objects placed on the right half, empty space on the left for large text, clean flat lighting, photorealistic, 16:9, 1280x720
```
- 사실 근거: brief.md 핵심 메시지 2 및 구성표 사유 1~4(하단 정보, 약관·개인정보처리방침, 환불정책, 상품·가격 페이지). "4개"는 이 영상의 7개 분류 기준이라는 점을 대본 사유 1~4 구간에서 함께 보여줄 것.

---

## 렌더 확인 결과
- 3장 모두 1280×720 PNG, 72~81KB (2MB 이하). 글자 잘림 없음, 검정 외곽선 덕분에 그라데이션 양끝 모두 대비 충분 → 재렌더 불필요.
- 렌더 폰트가 시스템 대체 폰트(wqy-zenhei)라 획이 얇은 편. 최종본은 `--font Pretendard-ExtraBold.otf` 같은 굵은 고딕으로 다시 렌더할 것을 권장합니다.
- 현재 시안은 문구가 가로로 꽉 차 있습니다(A 2줄이 약 1,100px). 실사 배경에 인물·오브젝트를 우측에 넣을 때는 텍스트가 좌측 55% 안에 들어가야 하므로, 스크립트의 최대 폭(현재 W×0.86)을 줄이거나 글자 크기를 낮춰 다시 렌더하세요.

## 추천안: A안 ("또 반려?|맨 아래부터")
- 이미 반려를 겪은 핵심 타깃(초기 1인 창업자, 비사업자)을 겨냥. "맨 아래부터"는 제목에 없는 정보이고 영상 훅("손님처럼 들어가서 맨 아래까지")과 사유 1(하단 정보)로 바로 이어짐
- B안(결과형)은 아직 심사를 넣지 않은 바이브코더에게 강함. 결과 보장 표현 없음
- **이미 반려를 겪은 핵심 타깃(C. 초기 1인 창업자, B. 비사업자 크리에이터)이 바로 자기 일로 받아들이는 문구**입니다. "또"가 반복 반려를 겪은 시청자를 정확히 겨냥합니다.
- 제목은 해결("이것부터 고치세요"), 썸네일은 문제를 맡아 서로 역할이 겹치지 않습니다.

## A/B 테스트 계획 (YouTube Studio "테스트 및 비교")
| 항목 | 설정 |
|---|---|
| 테스트 대상 | 썸네일 2안 A / B 테스트, C 제외 (제목은 고정해서 썸네일 효과만 측정) |
| 시작 시점 | 실사 배경으로 교체한 최종본 업로드와 동시에 등록 (예약 공개 시점부터 노출 분배) |
| 판정 지표 | Studio 기본 기준인 시청 시간 점유율(watch time share). 노출 클릭률(목표 5%)은 보조 지표로 함께 기록 |
| 기간 | Studio가 결과를 확정할 때까지(보통 최대 2주). 결과가 "결론 없음"이면 추천안 A를 유지 |
| 기록 | 결과 화면 캡처와 승리안을 analytics-analyst 주간 리포트에 넘겨 「심사 통과 클리닉」 다음 화 썸네일 유형(공포형 vs 해결형) 결정에 반영 |
| 주의 | 테스트 중에는 썸네일·제목을 수동으로 바꾸지 않음. 쇼츠 썸네일은 별도로 운영 |

## 컴플라이언스 체크
- [x] "100% 통과", "무조건", 통과 보장 뉘앙스 없음 (B "바로 수정"은 수정 작업을 말하며 심사 결과가 아님)
- [x] 타사(PG사·AI 도구) 로고 없음. 프롬프트에 "no logos, no readable text" 명시
- [x] 실존 인물 없음. AI로 인물을 생성하면 업로드 시 `containsSyntheticMedia: true` 설정 필요 (CLAUDE.md 절대 규칙 4)
- [x] 1280×720, 2MB 이하
- [x] 수수료 수치 미사용 (승인 ①: 영상 내 수수료 언급 금지)

## 검수 반영 (2026-11-08)
- A안 2줄 "코드 문제 아님" → "맨 아래부터": 출처 없는 단정을 피하고, 영상 훅("손님처럼 들어가서 맨 아래까지")과 사유 1(하단 정보)에 직접 연결
- B안 "AI 한 줄로 / 10분 수정" → "AI 프롬프트로 / 바로 수정", 배지 "프롬프트 7줄 공개": 영상에 없는 시간 약속 제거, 실제 프롬프트 7줄과 일치
- C안 "7개 중 4개 | 빈 페이지"는 대본에 이를 직접 말하는 장면이 없어 A/B 테스트 후보에서 제외 (필요 시 대본 7:50 체크리스트에 "7개 중 4개는 페이지 하나 만들면 끝" 한 줄 추가 후 사용)
