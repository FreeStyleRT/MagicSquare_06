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
