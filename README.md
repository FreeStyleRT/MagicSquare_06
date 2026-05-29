# Magic Square 4x4 — TDD Practice

[![Repository](https://img.shields.io/badge/GitHub-MagicSquare__06-blue)](https://github.com/FreeStyleRT/MagicSquare_06)

4×4 마방진 문제를 **불변식 기반 설계·검증 훈련**에 활용하는 프로젝트입니다.  
ECB 아키텍처, Dual-Track UI + Logic TDD, 입력/출력 계약 고정, Concept-to-Code Traceability를 목표로 합니다.

---

## 빠른 시작

```bash
git clone https://github.com/FreeStyleRT/MagicSquare_06.git
cd MagicSquare_06
```

1. [docs/PRD_MagicSquare.md](docs/PRD_MagicSquare.md) — 구현 전 기준 PRD  
2. [Report/01.MagicSquare-Problem-Definition-Report.md](Report/01.MagicSquare-Problem-Definition-Report.md) — 문제 정의(STEP 1~5)  
3. [Prompt/06.MagicSquare-Level1-to-Level5-Transcript.md](Prompt/06.MagicSquare-Level1-to-Level5-Transcript.md) — Epic → Journey → Story → Scenario 기획  

---

## 프로젝트 목적

표면적으로는 “4×4 격자에 1~16을 채워 행·열·대각선의 합을 맞추는 프로그램”을 목표로 하지만, 본 저장소가 다루는 **진짜 문제**는 다음과 같습니다.

> **고정된 4×4 정수 격자**에 대해, 규칙 준수 여부를 **일관되게 판정**하고, 필요 시 **유효한 배치를 반복적으로 산출**하며, 그 결과를 **동일 기준으로 재현·검사**할 수 있어야 한다.

학습·실무 관점에서는 **제약 명문화, 불변 조건, 검증 우선, 관심사 분리(판정 vs 산출), TDD를 통한 계약 고정**을 훈련하는 것이 핵심입니다.

---

## 현재 진행 상태

| 단계 | 주제 | 상태 |
|------|------|------|
| STEP 1~5 | 문제 정의 | 완료 |
| PRD | 구현 전 기준 문서 | 완료 |
| Level 1~5 | Epic / Journey / Story / Scenario | 완료 |
| Cursor Rules / Agents | 개발 규칙·에이전트 | 완료 |
| User Entity baseline | ECB 샘플 엔티티 + 테스트 | 완료 |
| Magic Square 구현 | FR-01~FR-05 | **예정** |

---

## RED 단계 To-Do 리스트

> 이 체크리스트는 [docs/test_plan.md](docs/test_plan.md) 기반으로 생성되었습니다.
> 각 항목은 RED(실패 테스트 작성) 완료 시 체크합니다.

### Track A — UI / Boundary 테스트
- [ ] TC-A-01: grid=None 입력 → 실패 결과 반환 (Happy Path of Failure)
- [ ] TC-A-02: code가 정확히 "INVALID_SIZE" 문자열인지 검증
- [ ] TC-A-03: message가 "Grid must be 4x4." 와 문자 단위 동일한지 검증
- [ ] TC-A-04: grid=None 시 Domain 진입점 0회 호출 (mock/spy 검증)
- [ ] TC-A-05: grid=[] 빈 리스트 → 실패 결과 반환
- [ ] TC-A-06: grid=3×4 크기 불일치 → 실패 결과 반환
- [ ] TC-A-07: 반환 객체 타입이 지정 실패 결과 구조체인지 검증

### Track B — Domain / Logic 테스트
- [ ] TC-B-01: resolve()가 None grid를 직접 받지 않음을 격리 검증
- [ ] TC-B-02: Boundary가 None 분기를 처리 후 resolve() 미호출 확인
- [ ] TC-B-03: resolve() mock이 호출됐을 경우 테스트 실패 처리
- [ ] TC-B-04: AC-FR-01-02~05 범위의 케이스는 이 커밋에 포함하지 않음 확인

### 커버리지 목표
- [ ] Domain Logic: 95%+ (pip install pytest-cov)
- [ ] Boundary Layer: 85%+
- [ ] 전체 TOTAL: 90%+

### 결함 목록 연결
- [x] [defect_list.md](docs/defect_list.md) 생성 및 발견 결함 기록
- [x] 모든 결함 수정 후 회귀 테스트 통과 확인

---

## GREEN 단계 To-Do 리스트

> [docs/test_plan.md](docs/test_plan.md) 기준 **P0 → P1 → P2** 오름차순으로 최소 구현을 진행합니다.  
> 각 항목은 대응 RED 테스트가 통과(GREEN)되면 체크합니다.  
> RED 커밋은 Wave 단위로 묶고, GREEN 커밋은 동일 Wave 번호로 맞춥니다.

### 정렬 기준

| 축 | 규칙 |
|---|---|
| 1차 | 우선순위 `P0` → `P1` → `P2` |
| 2차 | `TC-01` → `TC-06` (test_plan §8) |
| 3차 | 동일 입력 — Boundary 계약 → Control 격리 |
| 4차 | README `TC-A-*` / `TC-B-*` 번호 |

### Wave 1 — P0: `grid=None` + Domain 미호출

- [x] **G-01** (TC-01 / BV-01): `BoundaryValidator.validate(None)` → `INVALID_SIZE` 반환
- [x] **G-02** (TC-A-02): `code == "INVALID_SIZE"` 계약 (`contracts.py`)
- [x] **G-03** (TC-A-03): `message == "Grid must be 4x4."` 문자 단위 일치
- [x] **G-04** (TC-A-07): Pydantic `FailureResponse` 단일 정의 및 파싱 통과
- [x] **G-05** (TC-A-04 / AC-FR01-05): `ResolveUseCase` — `grid=None` 시 `resolve()` 0회
- [x] **G-06** (TC-B-02): Boundary 선행 검증 후 Domain에 `None` 미전달
- [x] **G-07** (TC-B-03): `resolve()` mock `side_effect` — 호출 시 테스트 즉시 실패

**Wave 1 검증**

```powershell
pytest tests/ -k "none" -v
```

### Wave 2 — P1: 경계값 확장 (BV-02 ~ BV-06)

- [x] **G-08** (TC-02 / BV-02 / TC-A-05): `grid=[]` — `len(grid) != 4` 분기
- [x] **G-09** (TC-03 / BV-03): `grid=[[]]*4` — 행별 `len(row) != 4` 분기
- [x] **G-10** (TC-04 / BV-04 / TC-A-06): 3×4 — 행 수 ≠ 4 분기
- [x] **G-11** (TC-05 / BV-05): 4×3 — RED 테스트 추가 후 `INVALID_SIZE` GREEN
- [x] **G-12** (TC-06 / BV-06): 5×5 — RED 테스트 추가 후 행·열 초과 분기 GREEN

**Wave 2 검증**

```powershell
pytest tests/boundary/test_fr01_invalid_size.py::TestInvalidSizeBoundaryValues -v
```

### Wave 3 — P1: 예외·특이 케이스 (EX-01 ~ EX-06)

- [x] **G-13** (EX-01): BV-01~06 각각 — 예외 미발생, `FailureResponse` 반환
- [x] **G-14** (EX-02): 동일 invalid grid 2회 연속 — 동일 `code`·`message` (결정론)
- [x] **G-15** (EX-03): 비-리스트 타입 (`"invalid"`, `4`, `{}`) — 방어적 `INVALID_SIZE`
- [x] **G-16** (EX-04): 불균일 행 길이 — 행별 열 길이 검사
- [x] **G-17** (EX-05): 행 원소 `None` — `isinstance(row, list)` 검사
- [x] **G-18** (EX-06): mutable grid 전달 후 — 입력 grid 구조·내용 불변

### Wave 4 — P2: 범위 가드 + REFACTOR

- [x] **G-19**: `test_scope_excludes_valid_4x4_and_downstream_domain_cases` — AC-FR01-01 범위 고정 확인
- [x] **G-20** (TC-B-04): `test_scope_commit_excludes_fr01_02_through_fr05_cases` — FR-02~05 미포함 확인
- [ ] **G-21** (TP-REF-01): P0·P1 전체 회귀 + Boundary/Control `--cov-fail-under=85` 충족

**전체 gate 검증**

```powershell
pytest tests/boundary/ tests/control/ -v `
  --cov=magic_square.boundary `
  --cov=magic_square.control `
  --cov-fail-under=85
```

### GREEN 커밋 묶음 (RED Wave 대응)

- [x] **GREEN-Commit-1** (Wave 1): None + resolver 미호출 — Control 3건 (`G-05`~`G-07`)
- [x] **GREEN-Commit-2** (Wave 1+): None 계약 강화 — code / message / type (`G-02`~`G-04`)
- [x] **GREEN-Commit-3** (Wave 2): BV-02~04 parametrize (`G-08`~`G-10`)
- [x] **GREEN-Commit-4** (Wave 2): BV-05, BV-06 추가 (`G-11`~`G-12`)
- [x] **GREEN-Commit-5** (Wave 3): EX-01~06 (`G-13`~`G-18`)
- [ ] **GREEN-Commit-6** (Wave 4): REFACTOR + 커버리지 gate (`G-21`)

### 구현 의존 관계

```
G-01 (grid is None)
  → G-02~G-04 (FailureResponse 계약)
    → G-05~G-07 (ResolveUseCase early return)
      → G-08~G-12 (len(grid) / len(row) 분기)
        → G-13~G-18 (비-list / 불균일 행 / side effect)
          → G-21 (REFACTOR + cov 85%)
```

---

## 저장소 구조

저장소 루트 = 프로젝트 루트 (`MagicSquare_06` 클론 디렉터리).

```
MagicSquare_06/
├── README.md
├── .cursorrules
├── .cursor/
│   ├── agents/
│   └── rules/
├── docs/
│   └── PRD_MagicSquare.md
├── magic_square/
│   ├── boundary/
│   ├── control/
│   └── entity/
├── tests/
├── Report/
└── Prompt/
```

---

## 로컬 작업 경로

| 환경 | 권장 경로 |
|------|-----------|
| Windows (예시) | `c:\DEV\MagicSquare_06` |
| 클론 후 | 저장소 루트 디렉터리 |

Git 작업은 **이 폴더를 루트**로 합니다 (`README.md`가 있는 위치).

---

## 메타 정보

| 항목 | 값 |
|------|-----|
| 저장소 | [FreeStyleRT/MagicSquare_06](https://github.com/FreeStyleRT/MagicSquare_06) |
| 작성일 | 2026-05-28 |
| 도메인 | 4×4 Magic Square (1~16, 행·열·대각선 합 동일) |
| 개발 방식 | ECB + Dual-Track TDD |

---

## 라이선스·기여

개인 학습·워크숍용 산출물입니다. 문서가 추가되면 본 README의 **진행 상태** 표를 갱신하는 것을 권장합니다.
