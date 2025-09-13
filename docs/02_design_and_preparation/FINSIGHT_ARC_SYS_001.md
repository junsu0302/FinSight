# FINSIGNT-ARC-SYS-001: ETL 파이프라인 소프트웨어 설계 기술서

| 문서 ID       | FINSIGNT-ARC-SYS-001 |
| :------------ | :------------------- |
| **문서 버전** | 1.0                  |
| **프로젝트**  | FinSignt             |
| **작성자**    | 김준수               |
| **작성일**    | 2025년 9월 13일      |

---

## 1. 개요 (Overview)

본 문서는 FinSignt 프로젝트의 핵심 구성 요소인 **정형데이터 기반 변동성 예측 모델**의 데이터 기반을 마련하기 위한 ETL(Extract, Transform, Load) 파이프라인의 기술적 설계와 아키텍처를 정의한다. 본 문서의 목적은 시스템의 구조와 컴포넌트 간의 상호작용, 그리고 데이터 흐름을 명확히 기술하여 신규 참여자의 이해를 돕고, 향후 유지보수 및 기능 확장을 용이하게 하는 데 있다.

---

## 2. 시스템 아키텍처 (System Architecture)

본 섹션은 시스템의 전체적인 구조와 구성 요소 간의 관계를 거시적인 관점에서 설명한다. 이는 FinSignt 프로젝트 가치 중 **유지보수성**과 **확장성**을 보장하기 위한 아키텍처 원칙을 보여준다.

### 2.1. 아키텍처 다이어그램 (Component Diagram)

![ETL Component Diagram](./images/finsight_component_diagram.png)

- **설명:**
  - 위 다이어그램은 ETL 파이프라인을 구성하는 4개의 핵심 내부 컴포넌트(`KIS_Collector.py`, `KIS_API_hook.py`, `KIS_Transformer.py`, `DB_Handler.py`)와 외부 시스템(`한국투자증권(KIS) API`, `PostgreSQL DB`) 간의 의존성 및 제어 흐름을 명확히 보여준다.
  - 중앙의 **`KIS_Collector.py`(Orchestrator)** 가 전체 프로세스를 조율하며, 각 컴포넌트는 **단일 책임 원칙(SRP)** 에 따라 데이터 추출(Extractor), 변환(Transformer), 적재(Loader)의 역할을 독립적으로 수행한다. 이러한 모듈식 설계는 각 컴포넌트의 개별적인 테스트와 교체를 용이하게 한다.

---

## 3. 정적 설계 (Static Design)

본 섹션은 각 컴포넌트의 내부 구조와 클래스 설계를 미시적인 관점에서 상세히 기술한다. 코드 레벨에서의 설계 패턴 적용 방식을 통해 시스템의 유연성을 설명한다.

### 3.1. 클래스 다이어그램 (Class Diagram)

![ETL Class Diagram](./images/finsight_class_diagram.png)

- **설명:**
  - 위 다이어그램은 시스템의 주요 클래스와 인터페이스, 그리고 그들 간의 관계(상속, 구현, 연관, 의존)를 상세하게 나타낸다.
  - 특히 **Facade, Strategy, Builder, Wrapper**와 같은 GoF(Gang of Four) 디자인 패턴이 실제 코드에서 어떻게 구현되어 시스템의 **결합도(Coupling)는 낮추고 응집도(Cohesion)는 높이는지** 명확히 확인할 수 있다.

### 3.2. 주요 클래스 명세

#### `KIS_API_hook` (Wrapper Pattern)

- **역할:** KIS Open API와의 모든 통신을 전담하는 게이트웨이(Gateway) 및 래퍼(Wrapper).
- **핵심 메서드:** `get_*(...)`, `_send_request(...)` 등.
- **설계 원칙:** API 토큰 발급, HTTP 요청 헤더 설정, 재시도 로직, 응답 파싱 등 KIS API 통신의 모든 복잡성을 `_send_request()`라는 private 메서드 내에 캡슐화한다. 외부 호출자는 `get_...()` 형태의 단순화된 인터페이스만 호출하면 되므로, API의 복잡성으로부터 다른 컴포넌트를 완벽히 분리한다.

#### `KISTransformer` (Facade Pattern)

- **역할:** 복잡한 데이터 변환 서브시스템으로의 단일화된 진입점을 제공하는 퍼사드(Facade).
- **핵심 메서드:** `transform(transformer_name, raw_df)`
- **설계 원칙:** `KIS_Collector`는 데이터 변환이 필요할 때 오직 `KISTransformer`의 `transform()` 메서드만 호출한다. `transformer_name`에 따라 내부적으로 어떤 `Strategy`와 `Builder`가 동작하는지에 대한 구체적인 내용은 알 필요가 없다. 이는 변환 로직의 복잡성을 은닉하고 컴포넌트 간의 결합을 최소화한다.

#### `*_strategy.py` & `*_builder.py` (Strategy & Builder Pattern)

- **역할:** 실제 데이터 변환 알고리즘(`Strategy`)과 복잡한 DataFrame 객체의 생성(`Builder`)을 담당한다.
- **설계 원칙:**
  - **Strategy:** KIS API로부터 수신되는 다양한 형태의 JSON 데이터를 DB 스키마에 맞게 변환하는 로직을 `TransformerStrategy` 인터페이스의 구현체로 캡슐화한다. 새로운 API 응답 형태가 추가되더라도, 기존 코드 수정 없이 새로운 Strategy 클래스를 추가하는 것만으로 유연하게 확장할 수 있다 (OCP 원칙).
  - **Builder:** `estimate_perform_strategy`와 같이 여러 `output` 블록을 조합하여 복잡한 DataFrame을 생성해야 할 때, 생성 단계를 캡슐화하고 분리하여 동일한 생성 절차에서 서로 다른 표현 결과를 만들 수 있도록 한다.

#### `db_handler.py` (Repository Pattern)

- **역할:** PostgreSQL 데이터베이스와의 모든 상호작용(DDL 실행, DML 실행)을 책임지는 리포지토리(Repository).
- **핵심 메서드:** `create_table()`, `insert_data()`, `get_latest_date()`
- **설계 원칙:** 데이터 영속성에 관한 모든 로직(Connection, Cursor, Commit, Rollback 등)을 이 클래스에 위임함으로써, 다른 비즈니스 로직 코드로부터 데이터베이스 관련 코드를 분리한다. 이를 통해 DB 교체나 SQL 최적화 작업이 다른 컴포넌트에 미치는 영향을 최소화할 수 있다.

---

## 4. 동적 행위 (Dynamic Behavior)

본 섹션은 특정 시나리오가 주어졌을 때, 시스템의 컴포넌트들이 시간의 흐름에 따라 어떻게 메시지를 주고받으며 동작하는지를 설명한다.

### 4.1. 시나리오: 해외 주식 일별 시세 수집

![ETL Sequence Diagram](./images/finsight_sequence_diagram.png)

- **설명:**
  - 위 다이어그램은 Airflow와 같은 스케줄러에 의해 `KIS_Collector`가 실행되었을 때 발생하는 일련의 상호작용을 시간 순서대로 보여준다.
  - **[1단계: 시작일 결정]** `Collector`는 `DB_Handler`를 호출하여 DB에 저장된 데이터의 최신 날짜를 조회하고, 증분 수집(Incremental Loading)을 위한 시작일을 결정한다.
  - **[2단계: 데이터 추출]** `Collector`는 각 종목(ticker)에 대해 `KIS_API_hook`의 `get_us_stock_daily_price()` 메서드를 호출한다. `Hook`은 내부적으로 `_send_request()`를 통해 KIS API 서버와 통신하여 원본 JSON 데이터를 수신한다.
  - **[3단계: 데이터 변환]** `Collector`는 수신한 원본 데이터를 `KISTransformer`의 `transform()` 메서드로 전달한다. `Transformer`는 `transformer_name`('us_stock_daily_price')에 맞는 `UsStockDailyPriceStrategy`를 찾아 변환 작업을 위임하고, 최종적으로 정제된 DataFrame을 반환받는다.
  - **[4단계: 데이터 적재]** `Collector`는 변환된 DataFrame을 `DB_Handler`의 `insert_data()` 메서드에 전달하여 `PostgreSQL DB`에 최종 저장(INSERT)한다.
  - 이러한 흐름을 통해 데이터가 **Extract → Transform → Load** 단계를 거치며 어떻게 각 전문 컴포넌트에 의해 처리되는지를 명확하게 추적할 수 있다.
