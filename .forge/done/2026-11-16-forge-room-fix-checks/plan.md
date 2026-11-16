<!-- forge-slug: forge-room-fix-checks -->
<!-- task: 6 -->
<!-- priority: high -->
<!-- tdd: off -->
# [qa] check:open · check:fixtures 구현과 전체 재검증

## Goal / Non-goals
- Goal: loop.md C6·C7을 Taskfile에 그대로 구현하고, play.mjs 경로를 열린 방에 맞게 갱신, C1–C7 전체 실행 보고.
- Non-goals: 게임 코드·에셋 수정, 계약 완화.

## Source of truth
- Glossary terms: none
- Related ADRs: none
- Definition of Done:
  - `task check:open`, `task check:fixtures`가 Blender 헤드리스(`blender -b --python-expr` 또는 Taskfile 인라인)로 glb를 직접 실측해 판정.
  - 음성 확인 기록: 수정 전 값(칸막이 존재 / 1.60·1.44 m)에서 실패했던 출력 — 이 task 시작 시점에 이미 수정됐다면 임계값을 일시적으로 뒤집어 비0 종료 1회 확인 후 원복.
  - check:boot / play / layout / open / fixtures / verify 실제 출력과 exit code 보고.

## Work slices
- [ ] S1. check:open, check:fixtures 구현 + 음성 확인 — completion criterion: 두 task가 실측값 출력
- [ ] S2. play.mjs 경로 갱신(칸막이 문간 경유 제거 가능) — completion criterion: 반-우회 grep 두 개 → 0
- [ ] S3. C1–C7 전체 실행 보고 — completion criterion: 7개 명령 출력·exit code 기록 (depends: S1, S2)
