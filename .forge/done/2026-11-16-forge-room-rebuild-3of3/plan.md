<!-- forge-slug: forge-room-rebuild-3of3 -->
<!-- task: 3 -->
<!-- part: 3/3 -->
<!-- priority: high -->
<!-- tdd: off -->
# [qa] 헤드리스 검사(check:boot/play/layout)와 새 play.mjs

## Goal / Non-goals
- Goal: `.forge/loop.md`의 C1–C3 계약을 그대로 구현한 `task check:boot`, `task check:play`, `task check:layout`(각자 서버 기동·정리)과 새 키보드 시나리오 `play.mjs`. 게임 코드·에셋은 고치지 않음.
- Non-goals: 검사 기준 완화 · index.html/assets 수정 · fal 호출.

## Source of truth
- Glossary terms: none
- Related ADRs: none
- Definition of Done:
  - `task check:boot`: shot.mjs와 같은 GPU 플래그, 6초 로드, error 0 AND fps ≥ 55가 아니면 비0 종료. `probe/models_loaded.txt`에 실제 요청된 `/assets/models/*.glb` basename을 기록(`page.on('request')`).
  - `task check:play`: `play.mjs`를 `?autostart&seed=1`로 끝까지 실행하고 C2 단언(ordersCompleted≥1, gold>goldStart, traveled≥15, interactLog 순서 accept→pickup→heat→strike→deliver, 각 dist≤radius)을 검사해 실패 시 비0 종료.
  - `task check:layout`: C3 단언 구현.
  - `play.mjs`는 `page.evaluate(() => window.__game.state)` 읽기만 사용하고 입력은 키보드/마우스만 — C2의 grep 반-우회 단언 두 개 → 0.
  - 세 task와 `task verify`를 실행한 실제 출력을 보고. 실패 시 재현 쿼리 + 스크린샷(`probe/`)을 첨부해 gameplay/art3d에 귀속.
  - `Taskfile.yml`의 `SKILL` 변수가 실제 경로(`.agents/skills/video-to-game` 또는 `.claude/skills/video-to-game`)를 가리키는지 확인.

## Work slices
- [ ] S1. `task check:boot` + 모델 요청 기록 — completion criterion: 실행 시 판정 JSON과 `probe/models_loaded.txt` 생성
- [ ] S2. 새 `play.mjs`(FPS 경로 주행: 주문→재료→화로→모루→납품) — completion criterion: 반-우회 grep 두 개 → 0
- [ ] S3. `task check:play`, `task check:layout` — completion criterion: 단언 실패 시 비0 종료함을 일부러 틀린 쿼리로 1회 확인(예: 존재하지 않는 zone 키) (depends: S1, S2)
- [ ] S4. 전체 실행 보고(check:boot/play/layout, verify) — completion criterion: 네 명령의 실제 출력과 exit code 기록 (depends: S3)
