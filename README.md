# FinSight

> **바쁜 직장인을 위한 AI 포트폴리오**

FinSight는 복잡한 금융 시장 데이터 속에서 길을 잃지 않도록 돕는 인공지능 자산 관리 서비스입니다. 저희는 단순한 수익률 극대화를 넘어, **위험 관리 기반의 안정적인 장기 투자**를 지향합니다. 시계열 데이터(주가, 재무)와 비정형 텍스트 데이터(뉴스)를 통합적으로 분석하여 미래 주가를 예측하고, 이를 바탕으로 최적의 포트폴리오를 구성합니다.

무엇보다 FinSight는 XAI(설명 가능한 인공지능)를 통해 **'왜' 이러한 포트폴리오를 추천하는지** 그 근거를 투명하게 제공함으로써, 투자자가 확신을 가지고 자신의 자산을 운용할 수 있도록 돕는 것을 목표로 합니다.

![FinSight Project Overview](https://github.com/junsu0302/FinSight/blob/main/img/FinSight_Introduce.png?raw=true)

---

## 🏛️ 시스템 아키텍처

FinSight의 전체 시스템 아키텍처는 데이터 수집부터 포트폴리오 추천, 그리고 그 근거를 설명하는 과정까지의 모든 흐름을 보여줍니다.

![FinSight System Architecture](https://github.com/junsu0302/FinSight/blob/main/img/FinSight_Architecture.png?raw=true)

---

## 🛠️ 기술 스택 (Tech Stack)

| 구분                   | 기술                                                                    |
| :--------------------- | :---------------------------------------------------------------------- |
| **언어**               | `Python 3.9+`                                                           |
| **데이터베이스**       | `PostgreSQL`, `MongoDB`, `Elasticsearch`                                |
| **데이터 처리 & 분석** | `Pandas`, `NumPy`, `Tableau`                                            |
| **ML & MLOps**         | `Scikit-learn`, `XGBoost`, `LightGBM`, `PyTorch`, `TensorFlow`, `Keras` |
| **모델 관리**          | `MLflow`, `BentoML`, `Triton`                                           |
| **오케스트레이션**     | `Apache Airflow`, `Docker`, `Docker Compose`                            |
| **CI/CD**              | `Argo CI/CD`                                                            |
| **모니터링**           | `Prometheus`, `Grafana`                                                 |
| **프론트엔드**         | `Streamlit`                                                             |
| **기타**               | `Git`, `GitKraken`, `Notion`                                            |

---

## 🚀 프로젝트 실행 단계 및 토의

FinSight 프로젝트는 총 9개의 핵심 단계로 구성되어 있으며, 각 단계의 완료 후에는 관련 결정 사항과 결과에 대한 토의 내용을 문서로 기록하여 관리합니다.

> 최신 디렉토리 구조는 반영되지 않음

| 단계   | 주요 활동 및 목표                                                                            | Discussion 링크                                                                   |
| :----- | :------------------------------------------------------------------------------------------- | :-------------------------------------------------------------------------------- |
| **P1** | **핵심 인프라 구축**: Docker, Git을 활용한 로컬 개발 환경 설정.                              | [Docker based Architecture](https://github.com/junsu0302/FinSight/discussions/12) |
| **P2** | **데이터 수집 자동화**: Airflow를 이용한 일일 데이터 수집 파이프라인 구축.                   | [ETL Pipeline Docs](https://github.com/junsu0302/FinSight/discussions/22)         |
| **P3** | **피처 엔지니어링**: 기술적 & 기본적 분석 지표를 계산하여 DWH에 저장.                        | _(링크 추가 예정)_                                                                |
| **P4** | **뉴스 이벤트 추출**: LLM을 활용해 뉴스에서 금융 이벤트를 추출하고 Elasticsearch에 저장.     | _(링크 추가 예정)_                                                                |
| **P5** | **통합 피처 스토어 구축**: 모든 정형/비정형 피처를 결합하여 모델 학습용 데이터셋 생성.       | _(링크 추가 예정)_                                                                |
| **P6** | **주가 예측 모델 개발**: MLflow로 회귀 모델 실험을 추적하고 최적 모델 선정.                  | _(링크 추가 예정)_                                                                |
| **P7** | **포트폴리오 전략 개발 및 백테스팅**: 예측 주가를 기반으로 포트폴리오를 구성하고 성과 검증.  | _(링크 추가 예정)_                                                                |
| **P8** | **리밸런싱 파이프라인 자동화**: Airflow를 통해 분기별 포트폴리오 리밸런싱 End-to-End 자동화. | _(링크 추가 예정)_                                                                |
| **P9** | **RAG 기반 Q&A 봇 구축**: Streamlit으로 포트폴리오 결정 이유를 설명하는 데모 웹 개발.        | _(링크 추가 예정)_                                                                |

---

## 📁 디렉토리 구조

```text
.
├── airflow/      # Airflow DAGs, plugins, logs 등 관련 파일
├── img/          # 각종 문서에 사용되는 이미지 파일
├── data/         # 샘플 데이터 및 SQL 스크립트
├── notebooks/    # EDA 및 모델 프로토타이핑을 위한 Jupyter Notebooks
├── src/          # 데이터 처리, 모델링, API 등 핵심 소스 코드
├── tests/        # 단위 테스트 및 통합 테스트 코드
├── .github/      # GitHub Actions 워크플로우
├── docker-compose.yml
└── README.md
```

## ✍️ 코드 기여 가이드

프로젝트의 일관성 유지를 위해 아래 가이드 문서를 반드시 숙지해 주시기 바랍니다.

- [문서 ID 명명 규칙](https://github.com/junsu0302/FinSight/discussions/15)
- [테스트 케이스 명세서 작성 규칙](https://github.com/junsu0302/FinSight/discussions/17)
- [소프트웨어 설계서 작성 규칙](https://github.com/junsu0302/FinSight/discussions/24)

- [데이터 정의서 작성 규칙](https://github.com/junsu0302/FinSight/discussions/25)
- [EDA 보고서 작성 규칙](https://github.com/junsu0302/FinSight/discussions/26)
- [DWH 데이터 요구사항 명세서 작성 규칙](https://github.com/junsu0302/FinSight/discussions/27)
