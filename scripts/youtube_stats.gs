/**
 * 유튜브 영상 저장소 시트 → 조회수/좋아요/댓글 자동 갱신 (+ 선택: CTR·시청 지속률·구독 증가)
 *
 * 설치:
 *  1. 시트에서 확장 프로그램 > Apps Script 열기 → 이 코드 전체 붙여넣기 → 저장
 *  2. 왼쪽 "서비스(+)" → "YouTube Data API v3" 추가 (식별자 YouTube)
 *     (선택) "YouTube Analytics API" 추가 (식별자 YouTubeAnalytics) — CTR·지속률까지 채울 때
 *  3. 함수 선택 updateStats → 실행 → 채널 소유 구글 계정으로 권한 승인
 *  4. 왼쪽 "트리거(시계)" → 트리거 추가 → updateStats, 시간 기반, 일 단위(예: 오전 6~7시)
 *
 * 시트 '영상' 탭의 머리글 이름으로 열을 찾으므로 열 순서를 바꿔도 되지만, 머리글 이름은 바꾸지 마세요.
 */
const SHEET_NAME = '영상';

function videoIdFromUrl_(url) {
  if (!url) return '';
  const m = String(url).match(/(?:youtu\.be\/|v=|shorts\/|embed\/)([A-Za-z0-9_-]{11})/);
  return m ? m[1] : '';
}

function updateStats() {
  const sh = SpreadsheetApp.getActive().getSheetByName(SHEET_NAME);
  const data = sh.getDataRange().getValues();
  const head = data[0];
  const col = (name) => {
    const i = head.indexOf(name);
    if (i < 0) throw new Error('머리글을 찾을 수 없습니다: ' + name);
    return i;
  };
  const C = {
    url: col('유튜브 URL'), status: col('상태'), published: col('게시일'),
    views: col('조회수'), likes: col('좋아요'), comments: col('댓글'), updated: col('지표 갱신일'),
    ctr: col('CTR(%)'), ret: col('시청 지속률(%)'), subs: col('구독 증가'), impressions: col('노출수'),
  };

  const rows = [];
  for (let r = 1; r < data.length; r++) {
    const id = videoIdFromUrl_(data[r][C.url]);
    if (id) rows.push({ r, id });
  }
  if (!rows.length) return;

  const today = Utilities.formatDate(new Date(), Session.getScriptTimeZone(), 'yyyy-MM-dd');
  for (let i = 0; i < rows.length; i += 50) {
    const batch = rows.slice(i, i + 50);
    const res = YouTube.Videos.list('statistics,snippet,status', { id: batch.map((b) => b.id).join(',') });
    const byId = {};
    (res.items || []).forEach((it) => { byId[it.id] = it; });
    batch.forEach((b) => {
      const it = byId[b.id];
      if (!it) return;
      const s = it.statistics || {};
      sh.getRange(b.r + 1, C.views + 1).setValue(Number(s.viewCount || 0));
      sh.getRange(b.r + 1, C.likes + 1).setValue(Number(s.likeCount || 0));
      sh.getRange(b.r + 1, C.comments + 1).setValue(Number(s.commentCount || 0));
      sh.getRange(b.r + 1, C.updated + 1).setValue(today);
      if (it.status && it.status.privacyStatus === 'public') {
        sh.getRange(b.r + 1, C.status + 1).setValue('게시됨');
        if (!data[b.r][C.published] && it.snippet) {
          sh.getRange(b.r + 1, C.published + 1).setValue(it.snippet.publishedAt.slice(0, 10));
        }
      }
    });
  }

  // 선택: YouTube Analytics 서비스를 추가했으면 지속률·구독 증가도 채움
  if (typeof YouTubeAnalytics !== 'undefined') {
    rows.forEach((b) => {
      try {
        const rep = YouTubeAnalytics.Reports.query({
          ids: 'channel==MINE', startDate: '2020-01-01', endDate: today,
          metrics: 'averageViewPercentage,subscribersGained', filters: 'video==' + b.id,
        });
        const v = (rep.rows || [])[0];
        if (v) {
          sh.getRange(b.r + 1, C.ret + 1).setValue(Math.round(v[0] * 10) / 10);
          sh.getRange(b.r + 1, C.subs + 1).setValue(v[1]);
        }
      } catch (e) {
        console.log('Analytics 조회 실패 ' + b.id + ': ' + e.message);
      }
    });
  }
  // 노출수와 노출 클릭률(CTR)은 공개 API로 제공되지 않습니다. YouTube Studio > 분석 > 도달범위에서 옮겨 적으세요.
}
