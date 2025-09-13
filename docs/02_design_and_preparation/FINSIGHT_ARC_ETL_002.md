| 문서 ID       | FINSIGHT-ARC-ETL-002 |
| :------------ | :------------------- |
| **문서 버전** | 1.0                  |
| **프로젝트**  | FinSight             |
| **작성자**    | 김준수               |
| **작성일**    | 2025년 9월 13일      |

## 1. 문서 개요

본 문서는 FinSight 프로젝트 데이터 파이프라인의 **변환(Transform)** 계층을 담당하는 `transformer` 모듈의 소프트웨어 아키텍처를 상세히 기술하는 것을 목적으로 한다. `transformer` 모듈은 `KIS_API_hook`을 통해 추출된 다양한 구조의 원본 데이터를 DB 스키마에 맞는 정형 데이터(DataFrame)로 변환하는 책임을 가진다.

본 설계서는 모듈의 요구사항, 전체 구조, 적용된 디자인 패턴, 핵심 로직을 명세하여 향후 개발 및 유지보수 담당자가 설계 사상을 명확히 이해하고 일관된 개발을 수행할 수 있도록 지원한다.

---

## 2. 요구사항 및 제약사항

### 2.1. 기능 요구사항

- **다중 구조 처리**: KIS API가 제공하는 다양한 응답 구조(단일 `output`, `output1`+`output2` 결합, 다중 `output` 블록 재구성 등)를 모두 처리할 수 있어야 한다. [cite: 1, 3, 4, 5]
- **스키마 정합성**: 변환된 최종 데이터는 `KIS_schemas.py`에 정의된 `dataclass` 스키마와 컬럼 순서 및 타입이 일치해야 한다. [cite: 1, 3, 4, 5]
- **데이터 무결성**: 변환 과정에서 필수 데이터가 누락된 경우, 해당 레코드를 제외하여 데이터의 무결성을 보장해야 한다. [cite: 1, 3, 5]

### 2.2. 비기능 요구사항

- **확장성 (OCP 원칙)**: 신규 데이터 종류가 추가될 때, 기존 변환 로직의 수정을 최소화하고 새로운 변환 로직을 쉽게 추가할 수 있는 구조여야 한다.
- **가독성 및 유지보수성**: 복잡한 변환 로직을 책임과 역할에 따라 명확히 분리하여 코드의 가독성을 높이고 유지보수를 용이하게 해야 한다.
- **테스트 용이성**: 각 데이터별 변환 로직은 다른 로직과 독립적으로 단위 테스트(Unit Test)가 가능해야 한다.

---

## 3. 아키텍처 및 설계

`transformer` 모듈은 높은 확장성과 유지보수성을 확보하기 위해 **Facade, Strategy, Builder** 디자인 패턴을 유기적으로 조합하여 설계되었다.

### 3.1. 전체 구조: Facade + Strategy 패턴

- **`KISTransformer` (Context & Facade)**: `KIS_Collector`는 데이터 변환이 필요할 때 오직 `KISTransformer` 클래스의 `transform()` 메서드만 호출한다. 이 클래스는 모든 변환 전략(`Strategy`)들을 내부적으로 관리하며, `transformer_name`에 따라 적절한 전략을 선택하여 실행하는 **단일화된 창구(Facade)** 역할을 수행한다. [cite: 4]
- **`TransformerStrategy` (Interface)**: 모든 변환 전략 클래스가 반드시 구현해야 하는 `transform()` 메서드를 정의한 인터페이스(추상 클래스)이다. [cite: 2]
- **`*_strategy.py` (Concrete Strategy)**: `TransformerStrategy` 인터페이스를 구현한 구체적인 변환 전략 클래스들이다. 각 클래스는 특정 데이터 종류(예: `asking_price`, `estimate_perform`)에 대한 변환 절차 전체를 책임진다. [cite: 1, 3, 5]

### 3.2. 내부 변환 로직: Builder 패턴

- **`DataFrameBuilder` (Interface)**: 복잡한 DataFrame 객체의 생성 단계를 정의하는 `build()` 메서드를 가진 인터페이스이다. [cite: 2]
- **`*_builder.py` (Concrete Builder)**: `*_strategy.py` 내부에 구현된 빌더 클래스들로, 여러 `output` 블록을 병합하거나 데이터를 재구조화하는 등 복잡한 DataFrame 생성 과정을 캡슐화한다. `Strategy` 클래스는 이 `Builder`를 사용하여 최종 결과물을 단계적으로 생성한다. [cite: 1, 3, 5]

### 3.3. 설계 결정 및 대안 분석

본 설계는 각 계층의 역할을 명확히 분리하고 OCP(개방-폐쇄 원칙)를 준수하기 위해 다음과 같은 설계 결정을 내렸다.

| 구분          | **채택: Facade + Strategy + Builder**                                                                                                                                                                                                                       | **대안: 단일 클래스 내 분기문 처리**                                                                                                                                                                                                                                                                          |
| :------------ | :---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | :------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| **핵심 목적** | **기능의 분리 및 확장**                                                                                                                                                                                                                                     | 로직의 중앙 집중화                                                                                                                                                                                                                                                                                            |
| **평가**      | **(최적합)** `KISTransformer`는 전략 선택, `Strategy`는 변환 절차, `Builder`는 객체 생성을 각각 책임지므로 역할이 명확하다. 신규 데이터 추가 시 새로운 `Strategy`와 `Builder`만 추가하면 되므로 **OCP를 만족**하며, 각 클래스는 독립적으로 테스트 가능하다. | (부적합) `KISTransformer` 클래스 하나의 `transform` 메서드 내부에 `if/elif` 분기문으로 모든 변환 로직을 구현하는 방식이다. 이 경우, 새로운 데이터가 추가될 때마다 메서드 내부를 **직접 수정**해야 하므로 **OCP에 위배**된다. 또한, 클래스가 비대해지고 가독성이 저하되어 유지보수와 테스트가 매우 어려워진다. |

---

## 4. 핵심 로직 상세

### 4.1. 전략 선택 및 실행 (in `KISTransformer.py`)

`KISTransformer`는 생성자(`__init__`)에서 모든 전략 클래스들을 `_strategies` 딕셔너리에 등록합니다. `transform` 메서드는 이 딕셔너리를 통해 `transformer_name`에 해당하는 전략 객체를 찾아 `transform` 메서드를 호출하는 방식으로 동작합니다.

```python
# KISTransformer.py
class KISTransformer:
  def __init__(self):
    self._strategies: Dict[str, TransformerStrategy] = {
      "estimate_perform": EstimatePerformStrategy(),
      "asking_price": AskingPriceStrategy(),
      "daily_itemchartprice": DailyItemchartPriceStrategy(),
    }

  def transform(self, transformer_name: str, raw_df: pd.DataFrame) -> pd.DataFrame:
    strategy = self._strategies.get(transformer_name)
    if not strategy:
      raise ValueError(f"Unsupported transformer_name: '{transformer_name}'")

    return strategy.transform(raw_df)
```

### 4.2. 변환 로직 상세 (Strategy & Builder)

각 `Strategy`는 `Builder`를 사용하여 실제 변환 작업을 수행합니다. 데이터 구조의 복잡도에 따라 `Builder`의 역할이 달라집니다.

#### 4.2.1. 단순 결합 예시: `AskingPriceStrategy`

- **요구사항**: `output1`과 `output2`에 나뉘어 있는 '주식호가' 정보를 하나의 행으로 결합해야 합니다.
- **Builder 역할 (`AskingPriceBuilder.build`)**:
  1.  `data_source`를 기준으로 데이터를 `output1_df`와 `output2_df`로 분리합니다.
  2.  두 데이터가 모두 존재하는지 검증합니다.
  3.  `pd.concat`을 사용하여 두 데이터를 컬럼 기준으로 병합하고, `ticker` 정보를 추가하여 최종 DataFrame 조각을 생성합니다.
- **Strategy 역할 (`AskingPriceStrategy.transform`)**:
  1.  원본 DataFrame을 `ticker`별로 그룹화합니다.
  2.  각 그룹을 `Builder`에게 전달하여 변환된 DataFrame 조각들을 리스트에 수집합니다.
  3.  모든 조각을 `pd.concat`으로 합치고, 최종적으로 `KrStockAskingPrice` 스키마에 맞게 컬럼을 정렬하여 반환합니다.

#### 4.2.2. 복합 재구성 예시: `EstimatePerformStrategy`

- **요구사항**: `output1`(메타데이터), `output2`, `output3`(지표 데이터), `output4`(기간 정보)로 흩어져 있는 '종목추정실적' 정보를 기간별 재무제표 형태의 테이블로 재구성해야 합니다.
- **Builder 역할 (`EstimatePerformBuilder.build`)**:
  1.  원본 그룹을 `output1`~`output4` 딕셔너리/리스트로 재분리합니다.
  2.  `output4`의 `dt` 값을 최종 테이블의 **컬럼명**으로 사용합니다.
  3.  `output2`와 `output3`의 데이터를 합쳐 테이블의 **데이터 행**을 구성합니다.
  4.  DataFrame을 생성한 뒤, 행/열을 전환(`.transpose()`)하여 기간이 행이 되도록 구조를 변경합니다.
  5.  `output1`의 메타데이터(애널리스트, 투자의견 등)를 모든 행에 공통으로 추가합니다.
- **Strategy 역할 (`EstimatePerformStrategy.transform`)**:
  1.  `ticker`별로 그룹화하여 `Builder`를 호출하고 결과를 취합합니다.
  2.  최종적으로 `KrStockEstimatePerform` 스키마에 맞게 컬럼을 정렬하여 반환합니다.
