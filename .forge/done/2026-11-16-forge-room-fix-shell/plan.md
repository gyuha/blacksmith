<!-- forge-slug: forge-room-fix-shell -->
<!-- task: 4 -->
<!-- priority: high -->
<!-- tdd: off -->
# [art3d] 방 셸 칸막이 제거 · 북쪽 벽 설비 대형화 · 벽돌 텍스처 비율 교정

## Goal / Non-goals
- Goal: room_shell의 중앙 칸막이 제거(하나의 열린 방), room_order_window·room_exchange를 영상처럼 북쪽 벽을 채우는 대형 설비(높이 ≥2.2 m, 폭 ≥2.4 m)로, 벽돌 UV 스케일을 실제 벽돌 크기(약 0.25×0.065 m 단위가 읽히도록)로 교정.
- Non-goals: fal · 다른 소품 재설계 · 게임 코드.

## Source of truth
- Glossary terms: none
- Related ADRs: none
- 근거: done/2026-11-16-forge-room-rebuild-2of3/run.md "관찰된 결함", 사용자 결정(loop.md 범위 확장).
- Definition of Done:
  - 기존 room_*.glb는 git에 미추적(새 파일)이므로 같은 이름 재생성 허용. 단 구(舊) 추적 에셋은 여전히 수정 금지 — `git status --porcelain -uall assets | grep -vE '^\?\? assets/models/[A-Za-z0-9_]+\.glb$' | wc -l` → 0
  - fal_log 변경 0.
  - Blender 실측 bbox: order_window·exchange 높이 ≥2.2, 폭 ≥2.4 (C7 계약과 동일).
  - room_shell 내부(벽 0.6 m 안쪽, 높이 0.2–2.0 m) 정점 0 (C6 계약과 동일).
  - refs/room_layout.md 갱신(새 치수·앵커).

## Work slices
- [ ] S1. 셸 칸막이 제거 + 벽돌 UV 교정 — completion criterion: 내부 정점 0 실측 출력
- [ ] S2. 주문 창구·옵션 교환 대형화(영상의 조명 캐비닛 벽 참고, 독자 디자인) — completion criterion: bbox 실측 출력이 기준 충족
- [ ] S3. room_layout.md 갱신 + Blender 미리보기 렌더 refs/room_preview_north.png — completion criterion: 파일 존재 (depends: S1, S2)
