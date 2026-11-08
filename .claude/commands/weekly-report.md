---
description: 이번 주 유튜브 성과 분석 리포트와 백로그 우선순위 제안
argument-hint: [YYYY-WW]
---
**analytics-analyst** 에이전트로 `analytics/$ARGUMENTS/` 의 데이터를 분석해 report.md를 만든다.
데이터 폴더가 비어 있으면 YouTube Studio에서 내보낼 CSV 목록(콘텐츠별 개요, 노출수·CTR, 시청 지속률)을 안내하고 멈춘다.
리포트 요약과 백로그 변경 제안을 보여주고, 승인받은 변경만 `backlog/*.md`에 반영한다.
