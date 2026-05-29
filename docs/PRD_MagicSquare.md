# PRD — Magic Square 4x4 TDD Practice

## 1. Executive Summary
Magic Square 4x4 TDD Practice는 "정답 격자 1개 생성"이 아니라 "불변식 기반으로 검증 가능한 규칙 시스템 구축"을 목표로 한다. 본 프로젝트는 입력/출력 계약 고정, Boundary/Domain 책임 분리, Dual-Track TDD(Track A: Boundary Contract, Track B: Domain Invariant), RED-GREEN-REFACTOR 규율, 그리고 Concept -> Rule -> Use Case -> Contract -> Test -> Component 추적성을 구현 전 단계에서 확정하는 기준 문서다.

## 2. Background
학습자는 마방진 문제를 구현 과제로 시작하는 경우가 많고, 성공 기준을 "동작함"으로만 판단하는 경향이 있다. 그 결과 입력 검증 누락, 계층 책임 혼합, 리팩토링 후 계약 파손, 테스트 약화가 반복된다.
본 PRD는 문제를 "알고리즘 난이도"가 아닌 "불변식과 계약을 지키는 소프트웨어 설계 훈련"으로 재정의한다. 프로젝트의 산출물은 코드 이전에 요구사항/검증기준/추적성이다.

## 3. Problem Statement
본 문제는 "4x4 마방진을 만든다"가 아니다.
본 문제는 다음을 동시에 만족하는 검증 가능한 시스템 기준을 확정하는 것이다.

1. 입력이 도메인 규칙을 만족하는지 명시적으로 판정한다.
2. 빈칸/누락 숫자/마방진 조건을 불변식으로 검증한다.
3. 고정된 시도 순서(small-first, reverse)로 결과를 결정한다.
4. 결과를 고정 출력 계약(`int[6]`, 1-index)으로 반환한다.
5. 실패를 미정 상태로 두지 않고 정의된 실패 정책으로 종료한다.

입력/출력 계약은 요구사항의 실행 가능한 경계이며, TDD의 RED 기준을 고정하는 핵심 자산이다.

## 4. Why Now / Why Chain
- Why 1: 구현을 먼저 시작하면 요구사항이 코드에 종속된다.
- Why 2: 테스트 기준이 불명확하면 RED가 성립하지 않는다.
- Why 3: Boundary와 Domain이 섞이면 결함 원인 추적이 불가능해진다.
- Why 4: 리팩토링 후 외부 계약 파손 여부를 자동 검증하지 못한다.
- Why 5: 학습 목표(불변식 사고, 계약 중심 설계)가 결과물 중심 개발에 의해 소실된다.

현재 해결해야 하는 핵심 불편:
- 구현 선행, 계약 후행
- 성공/실패 기준 불일치
- 계층 경계 붕괴
- 회귀 보호 부재

## 5. Target Users
- TDD 학습자
- 코드 리뷰어
- Clean Architecture/ECB 훈련 개발자

사용 환경:
- 콘솔 실행 또는 테스트 실행 중심
- UI 화면, DB, Web/API, 외부 연동은 범위 밖

## 6. Vision & Epic Goal
**Vision**: 마방진 과제를 통해 불변식 기반 설계/검증 역량을 반복 가능한 방식으로 훈련한다.
**Epic Goal**: **불변식 기반 사고 훈련 시스템 구축**

핵심 성과:
- 규칙이 테스트 가능한 문장으로 고정된다.
- 계약 파손 없이 리팩토링이 가능해진다.
- Boundary/Domain 분리 상태에서 품질 지표를 달성한다.

## 7. Persona
- TDD를 학습 중인 개발자
- Clean Architecture 계층 분리를 이해하려는 학습자
- 알고리즘 정답보다 설계/계약/테스트/리팩토링 흐름을 훈련하려는 사용자

## 8. User Journey Summary
1. **문제 인식**
   - Pain Point: "정답 찾기"와 "검증 가능한 설계"를 동일시함
   - Learning Outcome: 성공 기준을 불변식으로 표현

2. **계약 정의**
   - Pain Point: 입력/출력 형식 모호성
   - Learning Outcome: Input/Output/Error 계약을 수치와 형식으로 고정

3. **도메인 분리**
   - Pain Point: 검증/탐색/판정 책임 혼합
   - Learning Outcome: 컴포넌트 책임 단위 분해

4. **Dual-Track TDD 진행**
   - Pain Point: Boundary 검증과 Domain 로직을 한 번에 구현
   - Learning Outcome: Track A/Track B 독립 RED-GREEN 진행

5. **회귀 보호**
   - Pain Point: 리팩토링 후 계약 파손
   - Learning Outcome: 계약/불변식 중심 회귀 검증

## 9. Scope

### 9.1 In-Scope
- 빈칸 좌표 탐색
- 누락 숫자 탐색
- 마방진 판정
- 두 조합 시도 후 결과 반환
- Boundary 입력 검증
- 출력 계약 검증
- RED-GREEN-REFACTOR 기반 검증 가능성 확보

### 9.2 Out-of-Scope
- UI 화면 개발
- DB 저장/검색
- Web/API 서버 개발
- N×N 일반화
- 완전한 마방진 생성 알고리즘
- 사용자 인증/권한
- 네트워크 오류 처리
- QR 스캔
- 외부 서비스 연동

## 10. Functional Requirements

### FR-01 Input Verification
- Description: 입력 행렬이 도메인 진입 전 계약을 만족하는지 검증한다.
- Layer: Boundary
- Input: `int[][]`
- Processing Rules:
  - 행렬 크기 4x4
  - `0` 개수 정확히 2
  - 값 범위 `0` 또는 `1~16`
  - `0` 제외 중복 금지
- Output: 성공 시 Domain 호출 허용, 실패 시 정의된 오류 응답 반환
- Acceptance Criteria:
  - AC-FR01-01: 4x4가 아니면 실패 코드 반환
  - AC-FR01-02: 빈칸 개수 2가 아니면 실패 코드 반환
  - AC-FR01-03: 범위 위반 값이 있으면 실패 코드 반환
  - AC-FR01-04: `0` 제외 중복이 있으면 실패 코드 반환
  - AC-FR01-05: 실패 시 Domain resolver를 호출하지 않는다
- Error / Exception Policy: 예외 전파 금지, 표준 실패 응답 반환
- Related Business Rules: BR-01, BR-02, BR-03, BR-04
- Related Test Direction: Boundary 계약 테스트, 미호출 테스트
- Component Candidate: BoundaryValidator

### FR-02 Blank Coordinate Discovery
- Description: row-major 기준 두 빈칸 좌표를 탐색한다.
- Layer: Domain
- Input: 검증 통과 4x4 행렬
- Processing Rules:
  - `0`을 빈칸으로 식별
  - row-major 순서 유지
  - 첫 번째 빈칸 정의를 고정
- Output: 빈칸 좌표 2개(내부 표준 좌표 체계)
- Acceptance Criteria:
  - AC-FR02-01: `0` 위치 2개를 반환한다
  - AC-FR02-02: row-major 순서를 유지한다
  - AC-FR02-03: 첫 번째 빈칸이 스캔 기준 첫 `0`과 일치한다
- Error / Exception Policy: Domain 내부 실패 코드로 처리
- Related Business Rules: BR-05
- Related Test Direction: 순서 보장 테스트
- Component Candidate: BlankFinder

### FR-03 Missing Number Discovery
- Description: `1~16`에서 누락된 숫자 2개를 도출한다.
- Layer: Domain
- Input: 검증 통과 4x4 행렬
- Processing Rules:
  - `0`은 누락 계산에서 제외
  - 누락 숫자 2개 도출
  - 오름차순 정렬
- Output: 누락 숫자 `[small, large]`
- Acceptance Criteria:
  - AC-FR03-01: 누락 숫자 개수는 2개다
  - AC-FR03-02: 누락 숫자는 오름차순이다
  - AC-FR03-03: 숫자 범위는 `1~16`이다
- Error / Exception Policy: Domain 내부 실패 코드로 처리
- Related Business Rules: BR-06, BR-07
- Related Test Direction: 누락/정렬 검증 테스트
- Component Candidate: MissingNumberFinder

### FR-04 Magic Square Validation
- Description: 완성 후보 행렬이 마방진 불변식을 만족하는지 판정한다.
- Layer: Domain
- Input: 완성 후보 4x4 행렬
- Processing Rules:
  - 행 4개 합 = 34
  - 열 4개 합 = 34
  - 대각선 2개 합 = 34
- Output: 유효/무효 판정
- Acceptance Criteria:
  - AC-FR04-01: 행 합이 모두 34면 행 조건 통과
  - AC-FR04-02: 열 합이 모두 34면 열 조건 통과
  - AC-FR04-03: 대각선 합 2개가 34면 대각 조건 통과
  - AC-FR04-04: 세 조건 모두 통과한 경우만 유효
- Error / Exception Policy: 판정 실패는 무효로 반환
- Related Business Rules: BR-08, BR-09
- Related Test Direction: 정상/부분 실패/완전 실패 테스트
- Component Candidate: MagicSquareValidator

### FR-05 Two-Combination Solver and Result Formatting
- Description: small-first 후 reverse 시도로 해를 결정하고 결과를 포맷한다.
- Layer: Domain + Boundary(Output formatting)
- Input: 검증 통과 행렬, 빈칸 좌표, 누락 숫자
- Processing Rules:
  - Attempt 1: small→첫 빈칸, large→둘째 빈칸
  - Attempt 2: Attempt 1 실패 시 reverse
  - 성공 시 `[r1,c1,n1,r2,c2,n2]` 1-index 반환
- Output: 성공 시 `int[6]`, 실패 시 표준 실패 응답
- Acceptance Criteria:
  - AC-FR05-01: Attempt 1 성공 시 해당 순서 반환
  - AC-FR05-02: Attempt 1 실패 시 Attempt 2를 실행
  - AC-FR05-03: Attempt 2 성공 시 reverse 순서 반환
  - AC-FR05-04: 성공 결과 길이는 6이다
  - AC-FR05-05: 반환 좌표는 1-index다
  - AC-FR05-06: 두 조합 모두 실패 시 정의된 실패 코드 반환
- Error / Exception Policy: **실패 응답 반환 정책 확정** (예외 외부 전파 금지)
- Related Business Rules: BR-10, BR-11
- Related Test Direction: small-first 성공/실패 후 reverse 성공/양측 실패 테스트
- Component Candidate: Solver, ResultFormatter

## 11. Business Rules / Domain Rules
- BR-01: 입력은 4x4 정수 행렬이어야 한다.
- BR-02: 입력에서 `0`은 정확히 2개여야 한다.
- BR-03: 모든 값은 `0` 또는 `1~16`이어야 한다.
- BR-04: `0`을 제외한 숫자는 중복될 수 없다.
- BR-05: 첫 번째 빈칸은 row-major 스캔에서 처음 발견된 `0`이다.
- BR-06: 누락 숫자 개수는 정확히 2개여야 한다.
- BR-07: 누락 숫자 반환 순서는 오름차순이어야 한다.
- BR-08: 마방진 상수는 `34`여야 한다.
- BR-09: 모든 행/열/두 대각선의 합은 각각 `34`여야 한다.
- BR-10: 성공 결과 좌표는 1-index여야 한다.
- BR-11: 성공 결과 형식은 `int[6]`이어야 한다.

## 12. Input / Output Contract

### 12.1 Input Contract

| Field / Item | Type | Rule | Valid Example | Invalid Example | Related Error Code / Failure Policy |
|---|---|---|---|---|---|
| Matrix | `int[][]` | 크기 4x4 고정 | `[[16,2,3,13],[5,11,10,8],[9,7,0,12],[4,14,15,0]]` | `[[1,2],[3,4]]` | E001 |
| Blank Cells | count of `0` | 정확히 2개 | `0`이 2개 포함 | `0`이 1개 또는 3개 | E002 |
| Value Range | int | `0` 또는 `1~16` | `16`, `0` | `17`, `-1` | E003 |
| Uniqueness | set rule | `0` 제외 중복 금지 | `1..16` 중 중복 없음 | `5`가 2회 등장 | E004 |
| First Blank | position rule | row-major 첫 `0` 고정 | `(3,3)`이 첫 빈칸 | 스캔 순서 무시 | E005(내부 검증 실패) |

### 12.2 Output Contract

| Field / Item | Type | Rule | Valid Example | Invalid Example | Related Error Code / Failure Policy |
|---|---|---|---|---|---|
| Success Result | `int[6]` | `[r1,c1,n1,r2,c2,n2]` | `[3,3,6,4,4,1]` | 길이 5/7 배열 | E007 |
| Coordinate Index | int | `r1,c1,r2,c2`는 1-index | `1<=r,c<=4` | `0`, `5` | E008 |
| Number Pair | int | `n1,n2`는 누락 숫자 2개 | `1,6` | 범위 밖 숫자 | E003 |
| Failure Response | structured error | 성공 대신 표준 실패 응답 | `{code:"E006", message:"..."}` | 실패 상태에서 success 형식 반환 | E006 |

## 13. Error / Failure Policy
정책 원칙:
- Boundary 검증 실패 시 Domain resolver 호출 금지
- 외부 호출자에게는 표준 실패 응답 반환
- 예외는 내부 변환 후 코드/메시지로 표준화

| Error Code | Message | Layer | Domain resolver 호출 여부 | Related Acceptance Criteria |
|---|---|---|---|---|
| E001 | Input matrix must be 4x4. | Boundary | No | AC-FR01-01 |
| E002 | Exactly two blank cells (`0`) are required. | Boundary | No | AC-FR01-02 |
| E003 | Values must be `0` or `1..16`. | Boundary | No | AC-FR01-03 |
| E004 | Duplicate non-zero values are not allowed. | Boundary | No | AC-FR01-04 |
| E006 | No valid magic square result for both attempts. | Domain/Control | Yes | AC-FR05-06 |
| E007 | Output format must be `int[6]`. | Boundary | Yes | AC-FR05-04 |
| E008 | Output coordinates must be 1-index. | Boundary | Yes | AC-FR05-05 |

## 14. Non-Functional Requirements
- NFR-01 Coverage: Domain Logic 테스트 커버리지는 95% 이상이어야 한다.
- NFR-02 Coverage: Boundary Validation 테스트 커버리지는 85% 이상이어야 한다.
- NFR-03 Determinism: 동일 입력은 항상 동일 출력 또는 동일 실패 코드를 반환해야 한다.
- NFR-04 Side Effect Policy: 입력 행렬은 외부 관점에서 변경되지 않아야 한다.
- NFR-05 Performance: 4x4 단일 실행은 50ms 이내를 만족해야 한다.
- NFR-06 Maintainability: Boundary와 Domain 책임은 분리되어야 한다.
- NFR-07 Maintainability: 설명 없는 매직 넘버 사용을 금지한다.
- NFR-08 Maintainability: 도메인 상수는 명명된 상수로 관리해야 한다.
- NFR-09 Reliability: 실패 정책은 E001~E008 규격과 일치해야 한다.

## 15. Dual-Track TDD Strategy

### 15.1 Track A — Boundary / UI Contract TDD
- 입력 검증 실패 조건을 RED로 먼저 고정한다.
- 성공 경로 출력 형식/좌표 규칙을 RED로 고정한다.
- 실패 응답 코드/메시지를 계약 테스트로 고정한다.
- 입력 검증 실패 시 Domain 미호출 조건을 고정한다.

### 15.2 Track B — Domain / Logic TDD
- 빈칸 탐색, 누락 숫자 탐색, 마방진 판정을 독립 RED로 고정한다.
- small-first 성공/실패 후 reverse 성공/양측 실패를 RED로 고정한다.
- 불변식(BR-05~BR-11) 중심으로 GREEN 최소 구현을 진행한다.

### 15.3 Parallel Progression Rules
- UI RED와 Logic RED를 분리한다.
- UI GREEN과 Logic GREEN을 각각 최소 변경으로 진행한다.
- 구조 개선은 REFACTOR 단계에서만 수행한다.
- Domain 전체 선구현 후 Boundary 부착 방식은 금지한다.
- 테스트 삭제/완화/우회로 통과시키는 방식은 금지한다.

## 16. Test Plan / QA

### 16.1 Normal Scenarios
- TS-N-01: small-first 성공
- TS-N-02: small-first 실패 후 reverse 성공

### 16.2 Exception Scenarios
- TS-E-01: 4x4 아님
- TS-E-02: 빈칸 개수 오류
- TS-E-03: 값 범위 오류
- TS-E-04: 중복 숫자 오류
- TS-E-05: 두 조합 모두 실패

### 16.3 Boundary Scenarios
- TS-B-01: 최소값 `1` 처리
- TS-B-02: 최대값 `16` 처리
- TS-B-03: `0`을 빈칸으로만 처리
- TS-B-04: 출력 좌표 1-index
- TS-B-05: 반환 배열 길이 6

### 16.4 Representative Test Data
- D-01 small-first 성공 행렬: `[[0,2,3,13],[5,11,10,8],[9,7,6,12],[4,14,15,0]]` 기대 결과 `[1,1,1,4,4,16]`
- D-02 reverse 성공 행렬: `[[16,2,3,13],[5,11,10,8],[9,7,0,12],[4,14,15,0]]` 기대 결과 `[3,3,6,4,4,1]`
- D-03 invalid size: `2x2` 행렬
- D-04 invalid blank count: `0` 개수 1 또는 3
- D-05 duplicate value: `0` 제외 중복 값 존재
- D-06 invalid range: `17` 또는 `-1` 포함

## 17. Architecture Overview, High-Level
- **Boundary Layer**
  - 입력 검증
  - 오류 응답 표준화
  - 출력 포맷/인덱스 계약 보장
- **Domain Layer**
  - 빈칸/누락 숫자/마방진 판정/조합 시도
  - 불변식 검증
- **Control / Application Layer**
  - Boundary <-> Domain 흐름 조정
  - 실패 코드 매핑 일관성 유지

의존 방향:
- Boundary -> Control -> Domain
- Domain은 Boundary를 참조하지 않는다.
- Domain은 UI/DB/Web/파일 시스템에 의존하지 않는다.

## 18. Component Candidates

| Component | Responsibility | Layer | Input | Output | Related FR | Related Test |
|---|---|---|---|---|---|---|
| BoundaryValidator | 입력 계약 검증 및 실패 코드 반환 | Boundary | `int[][]` | pass/failure | FR-01 | TS-E-01~04 |
| BlankFinder | row-major 빈칸 2개 탐색 | Domain | validated matrix | blank coordinates | FR-02 | TS-B-03 |
| MissingNumberFinder | 누락 숫자 2개 도출/정렬 | Domain | validated matrix | `[small,large]` | FR-03 | TS-B-01, TS-B-02 |
| MagicSquareValidator | 행/열/대각 합 34 판정 | Domain | candidate matrix | valid/invalid | FR-04 | TS-N-01, TS-N-02 |
| Solver | 두 조합 시도 및 성공/실패 결정 | Domain | matrix + blanks + missing nums | success/failure | FR-05 | TS-N-01, TS-N-02, TS-E-05 |
| ResultFormatter | 성공 결과 `int[6]`/1-index 보장 | Boundary/Control | solved positions/numbers | `int[6]` | FR-05 | TS-B-04, TS-B-05 |

## 19. Risks & Ambiguities

| Risk | Impact | Decision / Mitigation |
|---|---|---|
| 1-index / 0-index 혼동 | 결과 포맷 불일치 | 출력 계약에 1-index 고정, TS-B-04로 검증 |
| row-major 첫 빈칸 정의 누락 | Solver 비결정성 | BR-05로 고정, FR-02 AC로 검증 |
| small-first/reverse 데이터 혼동 | 오탐/미탐 발생 | D-01, D-02 분리 유지, AC-FR05-01~03로 검증 |
| 입력 행렬 변경 여부 불명확 | 부작용 회귀 | NFR-04로 "외부 관점 불변" 고정 |
| 양측 실패 정책 누락 | 런타임 처리 불일치 | E006 실패 응답 반환으로 확정 |
| 상수 34 하드코딩 남용 | 유지보수 저하 | BR-08 + NFR-07/08로 통제 |
| Boundary/Domain 책임 혼합 | 테스트/리뷰 복잡도 증가 | 아키텍처 의존성 규칙 강제 |

## 20. Engineering Principles
- EP-01: Python 3.10+ 기준을 준수한다.
- EP-02: PEP8 및 최대 라인 길이 기준을 준수한다.
- EP-03: 모든 public 계약은 타입힌트를 명시한다.
- EP-04: 테스트 프레임워크는 `pytest`, 패턴은 AAA를 사용한다.
- EP-05: 커버리지 목표(도메인 95%+, Boundary 85%+)를 유지한다.
- EP-06: ECB 계층 분리를 준수한다.
- EP-07: RED-GREEN-REFACTOR 단계를 강제한다.
- EP-08: `print()` 디버깅을 금지한다.
- EP-09: bare `except`를 금지한다.
- EP-10: 테스트 약화/삭제를 금지한다.
- EP-11: 설명 없는 매직 넘버 사용을 금지한다.
- EP-12: 하드코딩 상수 대신 명명된 상수를 사용한다.

## 21. Traceability Matrix

| Concept / Invariant | Business Rule | Feature ID | Acceptance Criteria | Test Case Candidate | Component |
|---|---|---|---|---|---|
| 4x4 입력 | BR-01 | FR-01 | AC-FR01-01 | TS-E-01 | BoundaryValidator |
| 빈칸 2개 | BR-02 | FR-01 | AC-FR01-02 | TS-E-02 | BoundaryValidator |
| 값 범위 0 또는 1~16 | BR-03 | FR-01 | AC-FR01-03 | TS-E-03 | BoundaryValidator |
| 중복 금지 | BR-04 | FR-01 | AC-FR01-04 | TS-E-04 | BoundaryValidator |
| row-major 첫 번째 빈칸 | BR-05 | FR-02 | AC-FR02-02, AC-FR02-03 | TS-B-03 | BlankFinder |
| 누락 숫자 2개 | BR-06 | FR-03 | AC-FR03-01 | TS-B-01/02 | MissingNumberFinder |
| 누락 숫자 오름차순 | BR-07 | FR-03 | AC-FR03-02 | TS-B-01/02 | MissingNumberFinder |
| 마방진 상수 34 | BR-08 | FR-04 | AC-FR04-01~03 | TS-N-01/02 | MagicSquareValidator |
| 행/열/대각선 합 | BR-09 | FR-04 | AC-FR04-04 | TS-N-01/02 | MagicSquareValidator |
| small-first 시도 | BR-10/11 | FR-05 | AC-FR05-01 | TS-N-01 | Solver |
| reverse 시도 | BR-10/11 | FR-05 | AC-FR05-02, AC-FR05-03 | TS-N-02 | Solver |
| int[6] 반환 | BR-11 | FR-05 | AC-FR05-04 | TS-B-05 | ResultFormatter |
| 1-index 좌표 | BR-10 | FR-05 | AC-FR05-05 | TS-B-04 | ResultFormatter |
| 양측 실패 정책 | BR-10/11 | FR-05 | AC-FR05-06 | TS-E-05 | Solver/Control |

## 22. Open Questions / Decision Needed
- Decision Needed-01: Control/Application Layer를 최소 오케스트레이션으로 항상 포함할지, Boundary->Domain 직접 호출을 허용할지 최종 확정 필요.
- Decision Needed-02: 실패 응답 메시지의 언어 정책(영문 고정/국문 고정/다국어)을 릴리즈 정책으로 확정 필요.
- Decision Needed-03: 성능 기준 50ms 측정 환경(로컬 단일 실행 기준, CI 기준)을 운영 표준으로 확정 필요.

## 23. Appendix

### 23.1 참고 문서 목록
- `Report/1.ProblemDefinition_Report.md`
- `Report/4.UserJourney_Epic_to_TechnicalScenario_Report.md`
- `Report/2.CleanArchitecture_DualTrack_TDD_Design_Report.md`
- `Report/3.DevelopmentEnvironment_CursorRules_ECB_UserEntity_Report.md`
- `.cursorrules`
- `.cursor/rules/*.mdc`

### 23.2 Cursor Rules 요약
- ECB 계층 의존 방향 강제
- TDD RED-GREEN-REFACTOR 단계 강제
- pytest/AAA/coverage 기준 유지
- 금지 패턴(`print`, bare except, 테스트 약화, 설명 없는 매직 넘버) 차단

### 23.3 대표 Gherkin Scenario 요약
- GS-01: small-first 성공 시 성공 결과 반환
- GS-02: small-first 실패 후 reverse 성공 시 reverse 결과 반환
- GS-03: 입력 검증 실패 시 Domain 미호출 및 실패 코드 반환

### 23.4 향후 RED Test ID 후보
- RED-BND-VAL-001: invalid size
- RED-BND-VAL-002: invalid blank count
- RED-BND-VAL-003: invalid range
- RED-BND-VAL-004: duplicate non-zero
- RED-DOM-BLK-001: row-major blank order
- RED-DOM-MIS-001: missing numbers asc order
- RED-DOM-MAG-001: row/col/diag sum validation
- RED-DOM-SOL-001: small-first success
- RED-DOM-SOL-002: reverse success after first fail
- RED-DOM-SOL-003: both attempts fail -> E006
