#!/usr/bin/env python3
"""metadata.json 기반 유튜브 업로드 (YouTube Data API v3).

준비:
  pip install google-api-python-client google-auth-oauthlib
  Google Cloud 콘솔 → YouTube Data API v3 사용 설정 → OAuth 클라이언트(데스크톱 앱) 생성
  → client_secret.json 을 프로젝트 루트에 저장 (git에 올리지 말 것)

사용:
  python3 scripts/upload_youtube.py episodes/<brand>/<id>/metadata.json [--dry-run]

안전장치:
  - privacyStatus 가 public 이면 --confirm-public 플래그 없이는 거부
  - publishAt 이 있으면 자동으로 private 로 업로드되어 예약 공개
  - 결과(videoId, url)를 metadata.json 의 result 필드에 기록
참고: 미인증(감사 전) API 프로젝트로 업로드한 영상은 비공개로 잠길 수 있습니다.
      정식 운영 전 Google의 API 감사(audit)를 신청하세요.
"""
import argparse
import json
import os
import sys
from datetime import datetime, timezone

SCOPES = ["https://www.googleapis.com/auth/youtube.upload", "https://www.googleapis.com/auth/youtube.force-ssl"]
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def get_service():
    from google.auth.transport.requests import Request
    from google.oauth2.credentials import Credentials
    from google_auth_oauthlib.flow import InstalledAppFlow
    from googleapiclient.discovery import build

    token_path = os.path.join(ROOT, "token.json")
    secret_path = os.path.join(ROOT, "client_secret.json")
    creds = Credentials.from_authorized_user_file(token_path, SCOPES) if os.path.exists(token_path) else None
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            if not os.path.exists(secret_path):
                sys.exit(f"{secret_path} 가 없습니다. 모듈 docstring의 준비 단계를 확인하세요.")
            creds = InstalledAppFlow.from_client_secrets_file(secret_path, SCOPES).run_local_server(port=0)
        with open(token_path, "w") as f:
            f.write(creds.to_json())
    return build("youtube", "v3", credentials=creds)


def build_body(m):
    status = {
        "privacyStatus": m.get("privacyStatus", "private"),
        "selfDeclaredMadeForKids": bool(m.get("madeForKids", False)),
        "containsSyntheticMedia": bool(m.get("containsSyntheticMedia", False)),
    }
    if m.get("publishAt"):
        status["privacyStatus"] = "private"
        status["publishAt"] = datetime.fromisoformat(m["publishAt"]).astimezone(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    return {
        "snippet": {
            "title": m["title"][:100],
            "description": m.get("description", "")[:5000],
            "tags": m.get("tags", []),
            "categoryId": str(m.get("categoryId", "22")),
            "defaultLanguage": m.get("defaultLanguage", "ko"),
            "defaultAudioLanguage": m.get("defaultAudioLanguage", "ko"),
        },
        "status": status,
    }


def resolve(p):
    return p if os.path.isabs(p) else os.path.join(ROOT, p)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("metadata")
    ap.add_argument("--dry-run", action="store_true")
    ap.add_argument("--confirm-public", action="store_true")
    a = ap.parse_args()

    with open(a.metadata, encoding="utf-8") as f:
        m = json.load(f)
    body = build_body(m)

    if body["status"]["privacyStatus"] == "public" and not a.confirm_public:
        sys.exit("public 업로드는 사람 승인 후 --confirm-public 을 붙여 실행하세요.")
    if len(" ".join(m.get("tags", []))) > 500:
        sys.exit("태그 총 길이가 500자를 넘습니다.")
    video = resolve(m["video_file"])
    if not os.path.exists(video) and not a.dry_run:
        sys.exit(f"영상 파일 없음: {video}")

    if a.dry_run:
        print(json.dumps(body, ensure_ascii=False, indent=2))
        print("dry-run: 업로드하지 않았습니다.")
        return

    from googleapiclient.http import MediaFileUpload

    yt = get_service()
    req = yt.videos().insert(part="snippet,status", body=body,
                             media_body=MediaFileUpload(video, chunksize=8 * 1024 * 1024, resumable=True))
    resp = None
    while resp is None:
        st, resp = req.next_chunk()
        if st:
            print(f"업로드 {int(st.progress() * 100)}%")
    vid = resp["id"]
    print(f"완료: https://youtu.be/{vid}")

    if m.get("thumbnail_file") and os.path.exists(resolve(m["thumbnail_file"])):
        yt.thumbnails().set(videoId=vid, media_body=MediaFileUpload(resolve(m["thumbnail_file"]))).execute()
        print("썸네일 설정 완료")
    if m.get("playlist_id"):
        yt.playlistItems().insert(part="snippet", body={"snippet": {
            "playlistId": m["playlist_id"], "resourceId": {"kind": "youtube#video", "videoId": vid}}}).execute()
        print("재생목록 추가 완료")
    if m.get("pinned_comment"):
        yt.commentThreads().insert(part="snippet", body={"snippet": {
            "videoId": vid, "topLevelComment": {"snippet": {"textOriginal": m["pinned_comment"]}}}}).execute()
        print("댓글 작성 완료 — 고정(pin)은 YouTube Studio에서 직접 하세요 (API 미지원)")

    m["result"] = {"videoId": vid, "url": f"https://youtu.be/{vid}",
                   "uploadedAt": datetime.now(timezone.utc).isoformat(), "status": body["status"]}
    with open(a.metadata, "w", encoding="utf-8") as f:
        json.dump(m, f, ensure_ascii=False, indent=2)


if __name__ == "__main__":
    main()
