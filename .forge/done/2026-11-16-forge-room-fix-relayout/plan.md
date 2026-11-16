<!-- forge-slug: forge-room-fix-relayout -->
<!-- task: 5 -->
<!-- priority: high -->
<!-- tdd: off -->
# [gameplay] 수정된 방에 맞춘 재배치·충돌 재설정

## Goal / Non-goals
- Goal: forge-room-fix-shell 산출물에 맞춰 index.html의 배치·충돌·구역 반경을 갱신. 열린 방에서 전 구역 직행 가능. C1–C5 계약 유지.
- Non-goals: 에셋 수정 · 새 메커니즘.

## Source of truth
- Glossary terms: none
- Related ADRs: none
- Definition of Done:
  - zones C3 조건 유지, 상호작용 거리 판정 유지.
  - 대형화된 북쪽 설비가 벽에 붙고 겹침 없음(북쪽 시점 스크린샷 probe/relayout_north.png).
  - shot.mjs '?autostart&seed=1' → errors 0, fps ≥ 55.
  - SPEC.md 구역 서술 갱신(필요 시).

## Work slices
- [ ] S1. 배치·충돌 갱신 — completion criterion: 칸막이 문간 경유 없이 모든 구역 직행 가능(gameplay 자체 키보드 테스트)
- [ ] S2. 북쪽 시점 스크린샷 + shot.mjs 실측 — completion criterion: errors 0, fps ≥55 출력 (depends: S1)
