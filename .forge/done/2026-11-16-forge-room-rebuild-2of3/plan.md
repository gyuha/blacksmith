<!-- forge-slug: forge-room-rebuild-2of3 -->
<!-- task: 2 -->
<!-- part: 2/3 -->
<!-- priority: high -->
<!-- tdd: off -->
# [gameplay] FPS 이동·주문·집기·제작 루프로 index.html 재작성

## Goal / Non-goals
- Goal: 새 방(`refs/room_layout.md`, art3d 산출)을 로드하고, FPS 이동으로 주문 창구에서 주문 받기 → 재료 집기 → 화로 가열 → 모루 타격(기존 강화 판정 유지) → 주문 창구 납품까지 한 바퀴가 되는 게임. `SPEC.md` 갱신.
- Non-goals: fal 호출 · 구 대장간 모델(anvil, bench, bucket, cabinet, hearth, hearth_fire, lamp, stool, toolrack) 로드 · 새 사운드 생성(기존 `assets/sfx`, `assets/music` 재사용만) · FORGE TAX 이름·무기명·UI 복제.

## Source of truth
- Glossary terms: none
- Related ADRs: none
- 계약(.forge/loop.md C1–C5): `?autostart`, `?seed=N` 유지, `window.__game.state` 유지·확장.
- Definition of Done:
  - 조작: WASD 이동, 마우스(포인터락) **및 방향키 ←→↑↓**로 시점(헤드리스 키보드 플레이 가능), `E` 집기/상호작용, `Space` 타격, `R` 재시작.
  - `__game.state`에 노출: `fps, phase, gold, goldStart, ordersCompleted, player:{x,z,yaw,traveled}, held, zones:{order,exchange,craft,forge,display,gate,rack → {x,z,radius,model}}, interactLog:[{action,zone,dist,t}]`.
  - 상호작용은 엔진이 `dist ≤ zones[zone].radius`일 때만 수행하고 그때만 `interactLog`에 기록.
  - 구역 좌표가 C3 사분면 조건을 만족(order/exchange 북, craft/forge 동, display 남, gate/rack 서).
  - 로드되는 glb: `blade.glb`, `hammer.glb` + `room_*.glb` 7종 이상, 구 모델 0.
  - 옵션 교환(exchange): 골드로 다음 타격 성공률 보정 등 1종 이상 동작, 진열장(display): 완성품 배치·판매.
  - `SPEC.md`가 새 루프·조작·구역을 서술.

## Work slices
- [ ] S1. 방 로딩 + 구역 정의 + 조명/포스트(기존 룩 유지) — completion criterion: `__game.state.zones` 7개가 C3 조건 만족
- [ ] S2. FPS 컨트롤러(충돌: 벽·가구 AABB, 이동 누적 `traveled`) — completion criterion: 키보드만으로 방 안 모든 구역에 도달 가능 (depends: S1)
- [ ] S3. 집기/들기(E) + 주문 시스템(주문 창구에서 수락·납품, 골드 지급) + 재료원 — completion criterion: `interactLog`에 accept/pickup/deliver 기록 (depends: S2)
- [ ] S4. 화로 가열 → 모루 타격(기존 판정 재사용) → 완성품, 옵션 교환·진열장 — completion criterion: heat/strike 기록, `ordersCompleted` 증가 (depends: S3)
- [ ] S5. `SPEC.md` 갱신 — completion criterion: 조작·구역·루프가 문서에 반영 (depends: S4)
