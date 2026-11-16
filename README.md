# THE TEMPER

`forgetax.mp4`를 보고 다시 만든 브라우저 게임입니다. Three.js 단일 파일(`index.html`)이고 빌드 단계가 없습니다.
대장간 안을 FPS로 걸어 다니며 **주문을 받고 → 재료를 집어 → 화로에서 달구고 → 모루에서 두드려 → 납품**합니다.

## 원본과 참고 범위

`forgetax.mp4`는 출시된 게임 *FORGE TAX*를 녹화한 91.8분짜리 영상(1280×720, 30 fps)입니다.
`gameplay.txt`는 저장소에 없어서 영상 분석(`study/`, `refs/`)과 `SPEC.md`를 기준으로 삼았습니다.

영상에서는 **공간의 기능 배치**만 참고했습니다. 이름, 무기명, 손님 캐릭터, UI 플라크는 가져오지 않았고,
방 구성과 소품은 독자적으로 만든 오마주입니다. 영상 컨택트 시트는 `refs/scan_sheet_01.jpg`, `refs/scan_sheet_02.jpg`입니다.

## 방 구성

방은 10 × 8 m이고 중심이 원점, `+x`가 동쪽, `+z`가 남쪽입니다.

```
              북
   ┌──────────────┬──────────────┐
   │  주문 창구    │  옵션 교환    │
 서 │ (order)      │ (exchange)   │  동
   │              │              │
   │ 철창 문·무기   │              │  모루 작업대(craft)
   │ 거치대        │              │  화로(forge)
   │ (gate, rack) │              │
   └──────────────┴──────────────┘
              진열장(display)
                 남
```

| 구역 | 위치 | 하는 일 |
|---|---|---|
| `order` | 북쪽 벽 서쪽 | 주문 받기, 완성품 납품 |
| `exchange` | 북쪽 벽 동쪽 | 골드로 다음 타격 보정(tonic) 구입 |
| `craft` | 동쪽 | 재료 상자에서 철 막대 집기, 모루에서 타격 |
| `forge` | 동쪽 | 화로에서 가열 |
| `display` | 남쪽 | 완성품 진열·판매 |
| `gate`, `rack` | 서쪽 | 철창 문(장식), 무기 거치대(완성품 걸기) |

## 조작

| 입력 | 동작 |
|---|---|
| `W` `A` `S` `D` | 이동 |
| 마우스 (클릭 후 포인터락) / `←` `→` `↑` `↓` | 시점 |
| `E` | 상호작용 (집기·가열·주문 수락·납품 등) |
| `Space` 길게 → 떼기 | 모루 앞에서 타격. 게이지의 밴드 안에서 떼면 성공 쪽으로 보정 |
| `R` | 재시작 (같은 시드면 같은 주문과 판정) |

상호작용은 엔진이 플레이어와 구역 중심의 거리가 구역 `radius` 이내일 때만 처리합니다.

## 게임 루프

```
order(E 수락) → craft(E 재료) → forge(E 가열) → craft(Space 타격) → order(E 납품) → 골드
                                      ↑ 등급 부족하면 다시 타격·재가열 ┘
```

- 시작 골드는 500입니다. 납품 보상은 `pay + 90 × (달성 등급 − 요구 등급)`입니다.
- 타격 결과는 `shatter`(파괴) / `damage`(−1) / `hold` / `rise`(+1) / `surge`(+2~+3, 프리즘 광채)입니다. 타격 1회에 12 g이 듭니다.
- 등급은 글로우로 표현합니다: 없음 → 얇은 흰 선 → 따뜻한 금색 → 백열 → 프리즘.

URL 파라미터: `?autostart`(타이틀 건너뛰기), `?seed=N`(주문·판정 고정), `?cam=x,y,z,yaw,pitch`(디버그 카메라).
세부 규칙과 `window.__game.state` 계약은 [`SPEC.md`](SPEC.md)에 있습니다.

## 실행

```bash
task play     # 0.0.0.0:8123 으로 서버를 띄우고 브라우저를 엽니다
task serve    # 서버만 (같은 네트워크의 다른 PC에서도 접속 가능)
```

`task serve`와 `task play`는 `0.0.0.0`에 바인드하므로 **같은 네트워크의 누구나 이 폴더 전체를 읽을 수 있습니다.**
공용 네트워크에서는 쓰지 마세요. 시작할 때 접속 주소와 경고가 출력됩니다.

정적 서버라면 무엇이든 됩니다: `python3 -m http.server 8123` 후 `http://127.0.0.1:8123/index.html`.

## 검증

각 검사는 스스로 서버를 띄우고 끝나면 정리합니다(`probe/with_server.sh`, `127.0.0.1` 바인드).

| task | 검사 내용 |
|---|---|
| `task check:boot` | 헤드리스로 6초 로드, 콘솔 에러 0, fps ≥ 55. 실제로 요청된 GLB 목록을 `probe/models_loaded.txt`에 기록 |
| `task check:play` | `play.mjs`(키보드 입력만, 게임 상태는 읽기만)로 한 바퀴를 끝까지 플레이. 주문 완료·골드 증가·이동 거리·상호작용 순서와 거리를 단언 |
| `task check:layout` | 구역 7개의 좌표 관계와 각 모델이 실제로 로드됐는지 |
| `task check:open` | Blender로 `room_shell.glb`를 직접 읽어 방 안을 가르는 벽이 없는지 |
| `task check:fixtures` | Blender로 주문 창구·옵션 교환의 크기(높이 ≥ 2.2 m, 폭 ≥ 2.4 m) 실측 |
| `task verify` | 헤드리스 로드, 콘솔 에러 있으면 실패 |

마지막 전체 실행 결과: 모두 exit 0, fps 60, 에러 0, `check:play`는 주문 1건 완료(골드 500 → 798).

## 에셋

**새로 만든 것 (이번 작업, fal 호출 없음):** Blender 스크립트 `build_props.py`로 만든 GLB 10종입니다.
`room_shell`, `room_order_window`, `room_exchange`, `room_anvil_bench`, `room_furnace`, `room_display`,
`room_gate`, `room_weapon_rack`, `room_material_crate`, `fire`. 모델을 다시 만들려면 `task props`
(= `blender --background --python build_props.py`)를 실행합니다.

**재활용한 것:**
- `assets/textures/*` — 벽돌, 작업대 나무, 바닥 판자, 달력 종이
- `assets/models/blade.glb`, `hammer.glb` — 기본 검과 망치
- `assets/sfx/*`, `assets/music/forge_theme.mp3` — 효과음과 음악

재활용한 텍스처·검·망치·사운드는 이전 빌드에서 fal로 생성한 것이고, 생성 기록은 `assets/*/fal_log.json`에 남아 있습니다.
이번 재구성에서는 fal을 호출하지 않았고 `fal_log.json`도 바꾸지 않았습니다.

사용되지 않는 이전 빌드 모델(`anvil`, `bench`, `bucket`, `cabinet`, `hearth`, `hearth_fire`, `lamp`, `stool`, `toolrack`)은 파일만 남아 있고
게임에서 로드하지 않습니다(`probe/models_loaded.txt`에 기록된 로드 목록에 없음).

## 룩

ACES Filmic 톤매핑, 올리브 그래파이트 팔레트(`#0e0e0d`~`#555946`), 따뜻한 앰버 키 라이트와 화로 불빛, 지수 안개를 씁니다.
후처리(블룸, 비네트, 그레인, 색수차)는 약하게 줄여 둔 상태입니다: 블룸 0.20, 비네트 0.30, 그레인 0.004.
자세한 값은 `SPEC.md`의 Look 절을 보세요.

## 영상과 다른 점 / 알려진 문제

- **화로**가 평평한 상자처럼 보이고 불빛이 화로와 벽 사이로 샙니다. 아치 입구 방향이 벽 쪽을 향한 것으로 보입니다.
- **벽돌**이 영상보다 큽니다.
- **방이 휑합니다.** 영상에 있는 벽 메모지, 도구 선반, 램프 같은 소품이 없습니다.
- 한 바퀴 이동 거리가 13.65 m라서 `check:play`의 15 m 기준을 채우려고 `play.mjs`가 서쪽을 한 번 돌아갑니다.
- 입력은 키보드와 마우스뿐입니다. 휴대폰·태블릿에서는 화면은 열리지만 조작할 수 없습니다.
- `takes/`, `pairs/`, `study/`는 **이전 빌드(고정 벤치 시점)** 기준 산출물입니다. 현재 게임과 맞지 않으니 비교용으로 쓰지 마세요.
  `*.mp4`는 `.gitignore` 대상이라 녹화본은 추적되지 않습니다. `probe/`도 무시되므로 검사 스크립트는 로컬에만 있습니다.

## 파일

```
index.html           게임 전체 (Three.js, import map, 빌드 없음)
SPEC.md              규칙·구역·상태 계약·룩 명세
build_props.py       Blender 소품·방 생성 스크립트    shrink.py   메시 축소
play.mjs             키보드 전용 플레이 시나리오       shot.mjs    스크린샷 도우미
Taskfile.yml         task 러너 (serve, play, check:*, verify, props, ...)
assets/models/       GLB (새 room_*·fire + 재활용 blade·hammer)
assets/textures/     재활용 텍스처       assets/sfx/, assets/music/   재활용 사운드
refs/                영상 스틸, 컨택트 시트, room_layout.md(소품 치수·앵커), 미리보기
probe/               검사 스크립트와 산출물 (gitignore)
study/ takes/ pairs/ 이전 빌드 기준 영상 분석·녹화·비교
```
