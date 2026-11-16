# run — forge-room-fix-shell
executor: Paseo art3d (codex/gpt-5.6-luna, auto-review), agent bab523e1
## Rulings
- task3(qa)가 활성 슬롯에 있는 동안 폴더가 겹치지 않아 병렬 실행(backlog에서 직접 실행·봉인). 단일 활성 슬롯 불변식의 의도적 예외 — 파일 충돌 없음.
## UAT (Measured, 오케스트레이터 Blender 독립 실측 /tmp/forgetax_scan/measure.py)
- room_order_window bbox 2.82×2.05×2.35 m, room_exchange 2.90×0.65×2.35 m → 높이≥2.2·폭≥2.4 충족
- room_shell 내부(벽 0.6 m 안쪽, 바닥 기준 0.2–2.0 m) 정점 0. 주의: 셸 glb 원점이 높이 중앙(z −1.64..1.64) → C6 구현은 바닥(min z) 기준 높이로 재야 함.
- assets 변화 = 새 glb뿐: 0 · fal_log 변경: 0
