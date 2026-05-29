# Magic Square — 결함 목록 (Defect List)

| 항목 | 내용 |
|---|---|
| **문서 ID** | DL-AC-FR01-01-001 |
| **기준** | [docs/test_plan.md](docs/test_plan.md), AC-FR01-01 / AC-FR01-05 |
| **최종 갱신** | 2026-05-29 |
| **상태 요약** | 등록 3건 — **수정 완료 3건**, 미해결 0건 |

---

## 결함 테이블

| ID | Severity | AC ID | 재현 절차 | 기대값 | 실제값 | 근본 원인 | 수정 요약 |
|---|---|---|---|---|---|---|---|
| DEF-001 | Critical | AC-FR01-01 | 프로젝트 루트에서 `python -m pytest tests/boundary/ -v` 실행 | `BoundaryValidator.validate(grid=None)` → `code="INVALID_SIZE"`, `message="Grid must be 4x4."` | `ModuleNotFoundError: No module named 'magic_square.boundary'` (수집 단계 ERROR) | `magic_square.boundary` 패키지·`BoundaryValidator` 미구현 | `magic_square/boundary/` 추가: `validator.py`에 `grid is None` 및 4×4 크기 분기, `contracts.py`에 `INVALID_SIZE` 계약 |
| DEF-002 | Critical | AC-FR01-05 | `python -m pytest tests/control/ -v` 실행 | `grid=None` 시 `DomainResolver.resolve()` **0회**, 동일 실패 계약 반환 | `ModuleNotFoundError: No module named 'magic_square.control'` (수집 단계 ERROR) | `magic_square.control` 패키지·오케스트레이션 미구현 | `magic_square/control/resolve_use_case.py` 추가: `is_size_invalid` 시 validator만 호출, `resolve()` 미호출 |
| DEF-003 | Minor | AC-FR01-01 | `tests/boundary/` 실행, `TestInvalidSizeResponseType::test_none_grid_returns_failure_response_model` | `FailureResponse.model_validate(result)` 성공 | `ValidationError`: 서로 다른 모듈의 `FailureResponse` 인스턴스 (`tests.helpers` vs `magic_square.boundary.contracts`) | 실패 응답 Pydantic 모델 이중 정의 | `tests/helpers/fr01_contract.py`가 `magic_square.boundary.contracts`를 re-export하도록 정렬 |

---

## 재현 로그 요약

### DEF-001 / DEF-002 (수집 ERROR)

```
ERROR collecting tests/boundary/test_fr01_invalid_size.py
tests\boundary\test_fr01_invalid_size.py:9: in <module>
    from magic_square.boundary.validator import BoundaryValidator
E   ModuleNotFoundError: No module named 'magic_square.boundary'

ERROR collecting tests/control/test_fr01_domain_not_called.py
tests\control\test_fr01_domain_not_called.py:9: in <module>
    from magic_square.control.domain_resolver import DomainResolver
E   ModuleNotFoundError: No module named 'magic_square.control'
```

### DEF-003 (Assertion / Validation)

```
FAILED test_none_grid_returns_failure_response_model
FailureResponse.model_validate(result)
E   ValidationError: Input should be a valid dictionary or instance of FailureResponse
    input_type=FailureResponse  # boundary.contracts.FailureResponse
```

---

## 회귀 검증

| 명령 | 결과 (수정 후) |
|---|---|
| `python -m pytest tests/boundary/ -v` | **8 passed** |
| `python -m pytest tests/control/ -v` | **4 passed** |
| `python -m pytest tests/boundary/ tests/control/ -v` | **12 passed** |

```powershell
cd c:\DEV\MagicSquare_06
.\.venv\Scripts\python.exe -m pytest tests/boundary/ tests/control/ -v
```

---

## 범위 외 (본 목록에 미등록)

다음은 AC-FR01-01 RED/GREEN 범위 밖이며, 별도 TP·결함 목록에서 다룬다.

- AC-FR01-02 ~ AC-FR01-04 (빈칸 개수, 값 범위, 중복)
- FR-02 ~ FR-05 (Domain solver, blank/missing/validation)
- 4×4 **유효** 입력에 대한 `resolve()` 성공 경로

---

## 변경 파일 (수정 요약 참고)

| 레이어 | 파일 |
|---|---|
| Boundary | `magic_square/boundary/constants.py`, `contracts.py`, `validator.py` |
| Control | `magic_square/control/domain_resolver.py`, `resolve_use_case.py` |
| Test | `tests/helpers/fr01_contract.py` (계약 re-export) |
