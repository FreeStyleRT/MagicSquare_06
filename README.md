# 4×4 Magic Square — 문제 정의 프로젝트

[![Repository](https://img.shields.io/badge/GitHub-MagicSquare__16-blue)](https://github.com/FreeStyleRT/MagicSquare_16)

4×4 마방진 프로그램을 만들기 **전에**, 문제를 관찰·분석·정의한 워크숍 산출물 모음입니다.  
현재 단계는 **문제 인식·정의(STEP 1~5)** 이며, 설계·구현·테스트 코드는 포함하지 않습니다.

---

## 빠른 시작

```bash
git clone https://github.com/FreeStyleRT/MagicSquare_16.git
cd MagicSquare_16
```

1. [Report/01.MagicSquare-Problem-Definition-Report.md](Report/01.MagicSquare-Problem-Definition-Report.md) — Executive Summary부터 STEP 5까지 읽기  
2. [Prompting/01.MagicSquare-Problem-Definition-Prompt.md](Prompting/01.MagicSquare-Problem-Definition-Prompt.md) — Cursor에서 워크숍 재현·STEP 6 이어가기  

---

## 프로젝트 목적

표면적으로는 “4×4 격자에 1~16을 채워 행·열·대각선의 합을 맞추는 프로그램”을 목표로 하지만, 본 저장소가 다루는 **진짜 문제**는 다음과 같습니다.

> **고정된 4×4 정수 격자**에 대해, 규칙 준수 여부를 **일관되게 판정**하고, 필요 시 **유효한 배치를 반복적으로 산출**하며, 그 결과를 **동일 기준으로 재현·검사**할 수 있어야 한다.

학습·실무 관점에서는 **제약 명문화, 불변 조건, 검증 우선, 관심사 분리(판정 vs 산출), TDD를 통한 계약 고정**을 훈련하는 것이 핵심입니다.

---

## 현재 진행 상태

| 단계 | 주제 | 상태 |
|------|------|------|
| STEP 1 | Observation (관찰) | 완료 |
| STEP 2 | Why #1 — 왜 “완성”인가 | 완료 |
| STEP 3 | Why #2 — 왜 프로그램인가 | 완료 |
| STEP 4 | Why #3 — 왜 TDD인가 | 완료 |
| STEP 5 | 진짜 문제 정의 | 완료 |
| STEP 6 | 이해관계자, 범위, 성공 기준, 시나리오 | **예정** |
| 이후 | 명세·테스트·구현 | **범위 외** |

---

## 저장소 구조

저장소 루트 = 프로젝트 루트 (`MagicSquare_16` 클론 디렉터리).

```
MagicSquare_16/
├── README.md                                          ← 이 파일
├── .gitignore
├── Report/
│   └── 01.MagicSquare-Problem-Definition-Report.md   ← STEP 1~5 통합 보고서
└── Prompting/
    └── 01.MagicSquare-Problem-Definition-Prompt.md     ← 대화 Export (재현·이어가기)
```

### 문서 안내

| 파일 | 용도 |
|------|------|
| [Report/01.MagicSquare-Problem-Definition-Report.md](Report/01.MagicSquare-Problem-Definition-Report.md) | Executive Summary, STEP별 요약, Invariant, 표면 vs 개선 대조 |
| [Prompting/01.MagicSquare-Problem-Definition-Prompt.md](Prompting/01.MagicSquare-Problem-Definition-Prompt.md) | Cursor Export **대화형 transcript** — 동일 워크숍 재실행·STEP 6 참고 |

---

## 핵심 결론 (요약)

### 표면 정의 (피해야 할 표현)

> 4×4에 1~16을 채워 마방진을 **완성하는 프로그램**을 만든다.

→ 16칸 채움 ≠ 규칙 만족. 생성·검증·품질 기준이 한 덩어리로 묶이기 쉽습니다.

### 개선된 정의

- **판정:** 1~16 각 1회, 정의된 행·열·대각선의 합이 모두 동일한가  
- **산출(선택):** 위 규칙을 만족하는 배치를 반복적으로 생성  
- **신뢰:** 동일 입력·규칙 → 동일 판정; 산출물은 판정을 통과해야 함  

### 핵심 Invariant (발췌)

| 구분 | 내용 |
|------|------|
| 데이터 | 값 집합 1~16, 검사 선의 합 동일, 4×4 정상 시 합 = 34 |
| 시스템 | 판정 일관·충실, 산출-판정 정합 |
| 프로세스 | “유효” 의미를 예시·반례로 먼저 고정, 판정 vs 산출 분리 |

자세한 목록은 보고서 **§5.3**을 참고하세요.

---

## 워크숍 진행 방법

1. **처음 읽을 때:** `Report/01.MagicSquare-Problem-Definition-Report.md`의 Executive Summary → STEP 5 순으로 읽습니다.  
2. **대화를 이어갈 때:** `Prompting/01.MagicSquare-Problem-Definition-Prompt.md`를 새 Cursor 채팅에 붙이거나, 보고서를 컨텍스트로 첨부합니다.  
3. **STEP 6 시작 예시** (구현·코드 없이):

   ```text
   STEP 1~5 문제 정의가 완료되었습니다.
   첨부: Report/01.MagicSquare-Problem-Definition-Report.md

   STEP 6 — 다음을 작성하십시오:
   - 이해관계자
   - 범위 In / Out
   - 성공 기준 및 비기능 요구
   - 사용자 시나리오 (2~3개)

   제약: 구현 설계·코드·알고리즘 절차 설명 금지.
   STEP 5의 개선된 정의·Invariant와 모순되지 않을 것.
   ```

---

## 워크숍 원칙

- **관찰 우선:** “만든다”보다 “어떤 상황·제약인가”부터 서술  
- **Why 연쇄:** 완성 → 프로그램 → TDD 순으로 동기를 밝힘  
- **검증 우선:** 산출보다 “무엇이 옳은 상태인가”를 먼저 고정  
- **단계 분리:** 문제 정의 단계에서는 설계·구현·알고리즘을 다루지 않음  

---

## 로컬 작업 경로

| 환경 | 권장 경로 |
|------|-----------|
| Windows (예시) | `c:\DEV\MagicSquare_16` |
| 클론 후 | 저장소 루트 디렉터리 |

Git 작업은 **이 폴더를 루트**로 합니다 (`README.md`가 있는 위치).

---

## 메타 정보

| 항목 | 값 |
|------|-----|
| 저장소 | [FreeStyleRT/MagicSquare_16](https://github.com/FreeStyleRT/MagicSquare_16) |
| 작성일 | 2026-05-28 |
| 문제 정의 범위 | STEP 1 ~ STEP 5 |
| 도메인 | 4×4 Magic Square (1~16, 행·열·대각선 합 동일) |

---

## 라이선스·기여

개인 학습·워크숍용 산출물입니다. STEP 6 이후 문서가 추가되면 본 README의 **진행 상태** 표를 갱신하는 것을 권장합니다.
