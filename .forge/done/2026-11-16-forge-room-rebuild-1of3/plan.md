<!-- forge-slug: forge-room-rebuild-1of3 -->
<!-- task: 1 -->
<!-- part: 1/3 -->
<!-- priority: high -->
<!-- tdd: off -->
# [art3d] 대장간 방과 소품을 Blender로 새로 구성

## Goal / Non-goals
- Goal: 영상의 대장간 기능 배치를 참고해 방 셸과 구역별 소품을 Blender 스크립트(`build_props.py`)로 새 `.glb`로 생성. 재활용: `assets/textures/*`, `blade.glb`, `hammer.glb`.
- Non-goals: fal 호출(전면 금지) · 기존 파일 덮어쓰기(새 파일명 `room_*`만) · 게임 코드 수정 · FORGE TAX의 고유 디자인(두건 손님, 플라크 UI, 무기명) 복제.

## Source of truth
- Glossary terms: none
- Related ADRs: none
- 참고: `refs/scan_sheet_01.jpg`, `refs/scan_sheet_02.jpg`(45초 간격 컨택트 시트), `refs/*.jpg`, `study/*.jpg`, `SPEC.md` 팔레트(올리브 그래파이트, 앰버 키 라이트, 글로우 등급).
- Definition of Done:
  - `blender -b -P build_props.py` 가 에러 없이 끝나고 아래 7종 이상의 새 glb를 `assets/models/room_*.glb`로 만든다.
  - `git status --porcelain -uall assets | grep -vE '^\?\? assets/models/[A-Za-z0-9_]+\.glb$' | wc -l` → 0 (C4d)
  - `git status --porcelain -- 'assets/**/fal_log.json' | wc -l` → 0 (C4a)
  - 각 새 glb 파일명이 `build_props.py`에 문자열로 존재 (C4c 사전조건).
  - 게임 측 인수인계 메모(`refs/room_layout.md`): 각 glb의 원점·치수(m)·권장 배치 좌표(방 중심 원점, +x=동, +z=남), 상호작용 앵커 위치.

## Work slices
- [ ] S1. 방 셸 `room_shell.glb`: 약 10×8 m, 높이 3.2 m, 벽돌 텍스처 벽·나무 판자 바닥·천장 들보, 서쪽 벽 철창 출입문 개구부 — completion criterion: glb 생성, 바닥 y=0, 방 중심 원점
- [ ] S2. 북쪽 벽 `room_order_window.glb`(철창 주문 창구+카운터)와 `room_exchange.glb`(3칸 조명 진열 슬롯+숫자 카운터+다이얼, 독자 디자인) — completion criterion: 두 glb 생성, 북쪽 벽에 붙는 원점 (depends: S1)
- [ ] S3. 동쪽 `room_anvil_bench.glb`(작업대+모루), `room_furnace.glb`(아치형 벽돌 화로, 불 영역은 별도 emissive 메시 이름 `fire`) — completion criterion: 두 glb 생성 (depends: S1)
- [ ] S4. 남쪽 `room_display.glb`(완성품 진열장, 3–5칸), 서쪽 `room_gate.glb`(철창 문), `room_weapon_rack.glb`(벽 무기 거치대), 재료원 `room_material_crate.glb`(주괴/광석 상자) — completion criterion: 4종 glb 생성 (depends: S1)
- [ ] S5. `refs/room_layout.md` 인수인계 메모 작성 + DoD 명령 실행 결과 기록 — completion criterion: 메모에 모든 glb 항목·좌표가 있고 DoD 명령 출력이 0 (depends: S2, S3, S4)
