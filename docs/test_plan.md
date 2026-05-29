# Magic Square — 테스트 계획서 (Test Plan)

| 항목 | 내용 |
|---|---|
| **문서 ID** | TP-AC-FR01-01-001 |
| **버전** | 1.0 |
| **작성일** | 2026-05-29 |
| **작성 역할** | Senior QA Lead |
| **기준 PRD** | [docs/PRD_MagicSquare.md](docs/PRD_MagicSquare.md) §10 FR-01, §13, §14, §16 |
| **샘플 AC** | **AC-FR01-01** — 4×4가 아니면 실패 코드 반환 |
| **보조 AC** | **AC-FR01-05** — 실패 시 Domain resolver 미호출 |
| **기술 스택** | Python 3.11+, pytest, pydantic, unittest.mock |
| **Dual-Track** | Track A (Boundary Contract) — 본 계획서 범위 |

---

## 1. 목적 및 범위

### 1.1 목적

FR-01 입력 검증 중 **크기(4×4) 불변식(AC-FR01-01)** 을 pytest 단위 테스트로 RED-GREEN-REFACTOR 사이클에 고정한다.  
동시에 **AC-FR01-05** 를 통해 Boundary 검증 실패 시 Domain 해 결정 진입점(resolver)이 호출되지 않음을 mock/spy로 검증한다.

### 1.2 In-Scope

| 레이어 | 컴포넌트(예정) | 테스트 대상 |
|---|---|---|
| Boundary | `BoundaryValidator` | 행렬 크기 4×4 판정, `INVALID_SIZE` 실패 응답 반환 |
| Control | `ResolveUseCase` (또는 동등 오케스트레이터) | 검증 실패 시 Domain resolver **0회** 호출 보장 |
| Contract | Pydantic `FailureResponse` | `{ code, message }` 구조·타입 고정 |

### 1.3 Out-of-Scope (본 계획서)

- AC-FR01-02 ~ AC-FR01-04 (빈칸 개수, 값 범위, 중복) — 별도 TP 문서
- **4×4 정상 입력** — AC-FR01-01 범위 외, **본 계획 경계값·예외 케이스 목록에 포함 금지**
- FR-02 ~ FR-05 Domain 로직 — Track B 별도 계획
- UI, DB, Web/API, 성능(50ms) 벤치마크

### 1.4 PRD 추적성

| Concept | Business Rule | FR | AC | Error Code (구현) | PRD Error Code |
|---|---|---|---|---|---|
| 4×4 입력 | BR-01 | FR-01 | AC-FR01-01 | `INVALID_SIZE` | E001 |
| Domain 미호출 | §13 정책 | FR-01 | AC-FR01-05 | — | — |

> 구현 계약은 본 계획서 기준 **`INVALID_SIZE` / `"Grid must be 4x4."`** 를 사용한다. PRD §13의 `E001` / `"Input matrix must be 4x4."` 와 의미적으로 동일하며, Control 계층에서 코드 매핑 시 추적성을 유지한다.

---

## 2. pytest 기반 단위 테스트 범위 및 우선순위

### 2.1 테스트 디렉터리 구조 (목표)

```
tests/
├── boundary/
│   └── test_fr01_invalid_size.py      # P0 — BoundaryValidator 단위
├── control/
│   └── test_fr01_domain_not_called.py # P0 — resolver 미호출 통합(얕은)
└── conftest.py                        # P1 — 공통 fixture, mock factory
```

### 2.2 우선순위 정의

| 우선순위 | ID | 테스트 범위 | 목표 | 선행 조건 |
|---|---|---|---|---|
| **P0** | RED-BND-VAL-001 | `grid=None` → `INVALID_SIZE` | Track A RED 고정 | 없음 |
| **P0** | RED-BND-VAL-001b | P0 + Domain resolver `call_count == 0` | AC-FR01-05 동시 검증 | Control + mock 주입 가능 |
| **P1** | RED-BND-VAL-001-ext | §4 경계값 전체(빈 리스트, 열 없음, 3×4/4×3/5×5) | 크기 판정 분기 커버 | P0 GREEN |
| **P1** | TP-EX-01 ~ EX-04 | §5 예외·특이 케이스 | 예외 전파 금지, 결정론 | P0 GREEN |
| **P2** | TP-REF-01 | REFACTOR 회귀 | P0·P1 전체 재실행, 커버리지 유지 | P1 GREEN |

### 2.3 테스트 작성 규칙

- 패턴: **AAA** (Arrange → Act → Assert)
- 함수명: `test_` 접두사 필수
- Fixture scope: 기본 `function` (상태 공유 금지)
- `@pytest.mark.parametrize` 로 §4 경계값 테이블 일괄 실행
- 실패 응답 검증: Pydantic 모델로 파싱 후 `code` / `message` assert
- 금지: `print()`, bare `except`, 테스트 삭제·완화로 GREEN 유도

### 2.4 P0 대표 시나리오 (샘플 예제)

| 항목 | 값 |
|---|---|
| AC | AC-FR01-01, AC-FR01-05 |
| 입력 | `grid = None` |
| 기대 출력 | `{ "code": "INVALID_SIZE", "message": "Grid must be 4x4." }` |
| Domain resolver | 호출 **0회** |

---

## 3. 경계값 케이스 목록

AC-FR01-01(크기 불일치)만 대상한다. 모든 케이스는 동일 기대 출력을 가진다.

```json
{ "code": "INVALID_SIZE", "message": "Grid must be 4x4." }
```

| ID | 입력 | 설명 | AC | 포함 |
|---|---|---|---|---|
| **BV-01** | `grid = None` | 명시적 None — 최소·선행 실패 | AC-FR01-01 | ✅ |
| **BV-02** | `grid = []` | 빈 리스트 — 행 0개 | AC-FR01-01 | ✅ |
| **BV-03** | `grid = [[]] * 4` | 행 4개 존재, 각 행 열 0개 | AC-FR01-01 | ✅ |
| **BV-04** | `grid = [[1]*4, [2]*4, [3]*4]` | 3×4 — 행 3, 열 4 | AC-FR01-01 | ✅ |
| **BV-05** | `grid = [[1]*3]*4` | 4×3 — 행 4, 열 3 | AC-FR01-01 | ✅ |
| **BV-06** | `grid = [[1]*5]*5` | 5×5 — 행·열 모두 초과 | AC-FR01-01 | ✅ |
| **BV-07** | `grid = [[16,2,3,13],[5,11,10,8],[9,7,0,12],[4,14,15,0]]` | 4×4 유효 형태 | — | ❌ **포함 금지** |

### 3.1 BV-03 주의사항

`[[]] * 4`는 Python에서 동일 빈 리스트 참조 4개를 만든다. 크기 검증 구현은 **행 수·각 행 열 수**를 독립적으로 판정해야 하며, 참조 동일성에 의존한 검증은 금지한다.

### 3.2 BV-04 ~ BV-06 구체 입력

```python
# BV-04: 3×4
grid_3x4 = [[1, 2, 3, 4], [5, 6, 7, 8], [9, 10, 11, 12]]

# BV-05: 4×3
grid_4x3 = [[1, 2, 3], [4, 5, 6], [7, 8, 9], [10, 11, 12]]

# BV-06: 5×5
grid_5x5 = [[1, 2, 3, 4, 5] for _ in range(5)]
```

---

## 4. 예외·특이 케이스 목록

| ID | 케이스 | 입력/조건 | 기대 동작 | 검증 포인트 |
|---|---|---|---|---|
| **EX-01** | 예외 전파 금지 | BV-01 ~ BV-06 각각 | `FailureResponse` 반환, **예외 미발생** | PRD §13 Error Policy |
| **EX-02** | 결정론 (NFR-03) | 동일 invalid grid 2회 연속 호출 | 동일 `code`·`message` | 해시/객체 동등성 |
| **EX-03** | 비-리스트 타입 | `grid = "invalid"`, `grid = 4`, `grid = {}` | `INVALID_SIZE` (또는 동일 크기 실패 정책) | 방어적 입력 처리 |
| **EX-04** | 불균일 행 길이 | `[[1,2,3,4],[1,2],[1,2,3,4],[1,2,3,4]]` | `INVALID_SIZE` — 열 수 불일치 | 행별 열 길이 검사 |
| **EX-05** | `None` 행 원소 | `[[1,2,3,4], None, [1,2,3,4], [1,2,3,4]]` | `INVALID_SIZE` (행 자체가 리스트 아님) | None-safe 순회 |
| **EX-06** | Side effect 없음 (NFR-04) | 유효하지 않지만 mutable grid 전달 | 호출 후 grid 내용·구조 불변 | shallow copy 여부와 무관 |

> **EX-03 ~ EX-06**은 P1/P2에서 추가한다. P0는 **BV-01 + resolver 미호출**만 RED로 고정한다.

---

## 5. Domain 해 결정 진입점 호출 횟수 검증 전략

### 5.1 검증 대상

| 이름 | 레이어 | 역할 |
|---|---|---|
| `DomainResolver.resolve` (또는 `Solver.solve`) | Domain/Control 경계 | 검증 통과 후에만 호출되는 해 결정 진입점 |
| `BoundaryValidator.validate` | Boundary | 크기·계약 선행 검증 |
| `ResolveUseCase.execute` | Control | validate → (pass) resolve 순서 오케스트레이션 |

### 5.2 Mock / Spy 패턴

**전략 A — Control 계층 통합 테스트 (권장, P0)**

1. `unittest.mock.create_autospec(DomainResolver, spec_set=True)` 로 fake resolver 생성
2. `ResolveUseCase(domain_resolver=mock_resolver)` 주입
3. Act: `use_case.execute(grid=None)`
4. Assert:
   - `mock_resolver.resolve.assert_not_called()`
   - `mock_resolver.resolve.call_count == 0`
   - 반환값이 Pydantic `FailureResponse(code="INVALID_SIZE", ...)` 와 일치

**전략 B — Boundary 단독 테스트 (P1 보조)**

- `BoundaryValidator` 단위 테스트에서는 resolver mock **불필요**
- 반환 타입이 `ValidationResult.failure(...)` 인지만 검증
- resolver 미호출은 Control 테스트에서만 assert (레이어 책임 분리)

**전략 C — Spy (호출 이력 기록, P2)**

- `wraps=real_resolver` 로 spy 생성 후, invalid 입력에서는 `call_count == 0` 확인
- valid 4×4 입력 시나리오는 **본 계획 범위 외** — Track B/후속 TP에서 `call_count == 1` 검증

### 5.3 Mock 검증 체크리스트

| # | Assert | AC |
|---|---|---|
| 1 | `resolve.assert_not_called()` | AC-FR01-05 |
| 2 | `resolve.call_count == 0` | AC-FR01-05 |
| 3 | `validate` 또는 `execute` 1회 호출로 실패 종료 | FR-01 Processing Rules 순서 |
| 4 | 예외(`TypeError`, `AttributeError` 등) 미발생 | §13 예외 전파 금지 |
| 5 | mock이 autospec이면 잘못된 시그니처 조기 탐지 | 유지보수성 |

### 5.4 ECB 의존성 준수

- Boundary 테스트 → Entity/Domain **직접 import 금지**
- Domain resolver mock은 **Control 테스트**에서만 주입
- Entity 계층은 본 AC 범위에서 **호출 0회**가 정상 (커버리지 측정 시 Domain 95% 목표는 Track B 테스트와 합산)

---

## 6. 커버리지 목표

PRD §14 NFR-01, NFR-02 기준:

| 레이어 | 패키지(목표) | 목표 커버리지 | 본 TP 기여 |
|---|---|---|---|
| **Domain (Entity + Domain logic)** | `src/entity/` (+ 향후 solver) | **≥ 95%** | 직접 기여 낮음 (미호출 경로) |
| **Boundary** | `src/boundary/` | **≥ 85%** | **주요 기여** — `BoundaryValidator` 크기 분기 |
| **Control** | `src/control/` | Boundary와 합산 또는 별도 gate | resolver 분기 100% |

### 6.1 본 TP만으로의 기대 커버리지

| 모듈 | 기대 |
|---|---|
| `boundary/validator.py` (크기 검증 함수) | 분기 85%+ 달성 가능 |
| `control/use_case.py` (early return 경로) | failure 분기 line cover |
| Domain solver | 0% 호출 — Track B 테스트 필수 |

> **Gate 정책**: CI에서는 레이어별 `--cov-fail-under` 를 분리 적용한다. Boundary-only PR은 Boundary 85%를, Domain PR은 Domain 95%를 각각 만족해야 merge 가능.

---

## 7. pytest-cov 측정 전략

### 7.1 설치

```bash
pip install pytest pytest-cov pydantic
```

### 7.2 기본 실행 (요청 명령)

```bash
pytest --cov=src --cov-report=term-missing
```

### 7.3 저장소 실제 패키지 매핑

현재 프로젝트 루트 패키지는 `src/` 이다. 아래 명령을 **로컬 표준**으로 사용한다.

```bash
# Boundary (Track A — 본 TP)
pytest tests/boundary/ tests/control/ \
  --cov=src.boundary \
  --cov=src.control \
  --cov-report=term-missing \
  --cov-fail-under=85

# Domain (Track B — 전체 gate, 본 TP와 합산)
pytest tests/ \
  --cov=src.entity \
  --cov-report=term-missing \
  --cov-fail-under=95
```

### 7.4 측정 범위 분리

| 실행 프로파일 | `--cov` 대상 | `--cov-fail-under` | 용도 |
|---|---|---|---|
| `boundary-gate` | `src.boundary`, `src.control` | 85 | FR-01 Track A PR |
| `domain-gate` | `src.entity` (+ 향후 domain) | 95 | FR-02~05 Track B |
| `full-gate` | `src` | Boundary 85 + Domain 95 (리포트 분리) | 릴리즈 전 |

### 7.5 term-missing 해석 가이드

- `Missing` 열에 **크기 검증 분기 line**이 없으면 BV-02 ~ BV-06 parametrize 추가
- Control `execute` early-return line 미커버 → resolver mock 테스트(P0) 누락
- Domain 모듈이 전부 Missing → 정상 (본 TP 범위); Track B 테스트 추가 필요

### 7.6 CI 권장 (향후)

```bash
pytest tests/boundary/ tests/control/ \
  --cov=src.boundary \
  --cov=src.control \
  --cov-report=xml:coverage-boundary.xml \
  --cov-fail-under=85
```

---

## 8. 테스트 케이스 매트릭스 (요약)

| TC ID | 우선순위 | 입력 | 기대 code | resolver 호출 | AC |
|---|---|---|---|---|---|
| TC-01 | P0 | `None` | `INVALID_SIZE` | 0 | AC-FR01-01, 05 |
| TC-02 | P1 | `[]` | `INVALID_SIZE` | 0 | AC-FR01-01, 05 |
| TC-03 | P1 | `[[]]*4` | `INVALID_SIZE` | 0 | AC-FR01-01, 05 |
| TC-04 | P1 | 3×4 | `INVALID_SIZE` | 0 | AC-FR01-01, 05 |
| TC-05 | P1 | 4×3 | `INVALID_SIZE` | 0 | AC-FR01-01, 05 |
| TC-06 | P1 | 5×5 | `INVALID_SIZE` | 0 | AC-FR01-01, 05 |
| TC-07 | — | 4×4 유효 | — | — | **범위 외 — 미작성** |

---

## 9. 완료 기준 (Exit Criteria)

- [ ] P0: TC-01 RED → GREEN → REFACTOR, pytest 전체 통과
- [ ] P0: TC-01에서 `DomainResolver.resolve` **call_count == 0** 검증
- [ ] P1: TC-02 ~ TC-06 parametrize 통과
- [ ] EX-01: invalid 입력에서 예외 미발생
- [ ] Boundary `--cov-fail-under=85` 충족 (`src.boundary` + `control` failure path)
- [ ] PRD 추적성: AC-FR01-01, AC-FR01-05, BR-01, TS-E-01, RED-BND-VAL-001 매핑 문서화

---

## 10. 참고

- PRD: [docs/PRD_MagicSquare.md](docs/PRD_MagicSquare.md)
- 아키텍처: ECB — Boundary → Control → Entity
- Dual-Track: 본 문서 = **Track A (Boundary Contract TDD)**
- 후속 TP: AC-FR01-02 (E002/빈칸 개수), AC-FR01-03 (E003/범위), AC-FR01-04 (E004/중복)
