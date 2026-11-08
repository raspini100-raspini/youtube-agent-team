---
description: 새 에피소드(롱폼 1 + 쇼츠 3)를 리서치부터 컴플라이언스 검수까지 진행
argument-hint: <vibepay|moduplay> <주제 또는 백로그 번호>
---
브랜드: $1
주제: $ARGUMENTS

총괄 프로듀서로서 CLAUDE.md 파이프라인을 따라 진행한다.

1. 오늘 날짜와 주제로 에피소드 id(`YYYYMMDD-slug`)를 정하고 `episodes/$1/<id>/` 폴더를 만든다.
2. **trend-researcher** 에이전트 → research.md
3. **content-strategist** 에이전트 → brief.md
4. 여기서 멈추고 사람에게 brief.md 요약 + 제목 후보 3개 + 각도 2개를 보여주고 **승인 ①**을 받는다.
5. 승인되면 **longform-scriptwriter**, 이어서 **shorts-producer**와 **thumbnail-designer**를 병렬로 실행한다.
6. **seo-publisher** → metadata.json, shorts_1~3.json (업로드는 하지 않음)
7. **compliance-reviewer** → review.md. FAIL이면 해당 에이전트에 수정 지시 후 재검수 (최대 2회).
8. 최종 산출물 목록, review 판정, 사람이 할 일(영상 편집, 승인 ②)을 정리해 보고한다.
