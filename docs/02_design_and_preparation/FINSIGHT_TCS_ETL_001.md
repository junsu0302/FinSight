| 문서 ID       | FINSIGHT-TCS-ETL-001 |
| :------------ | :------------------- |
| **문서 버전** | 1.0                  |
| **프로젝트**  | FinSignt             |
| **작성자**    | 김준수               |
| **작성일**    | 2025년 8월 14일      |

---

## 1. 문서 개요

### 1.1. 목적

본 문서는 FinSignt 프로젝트의 KIS(한국투자증권) API 연동 모듈(`src/hooks/KIS_API_hook.py`)의 기능적 정확성, 안정성, 오류 처리 능력 등 모든 측면을 검증하기 위한 **전체 테스트 케이스**를 명세하는 것을 목표로 한다.

### 1.2. 적용 범위

본 문서는 `src/hooks/KIS_API_hook.py` 모듈의 모든 공개 및 비공개 메서드에 대한 21개 단위 테스트 케이스의 설계, 실행, 결과 기준을 정의한다.

해당 메서드들은 KIS API의 `[국내주식] 종목 정보`에 대한 정보를 수집한다.

### 1.3. 테스트 요약 표

| Test Case ID       | 테스트 유형 | 대상(모듈/함수)                    | 테스트 목표(요약)                                                     |
| :----------------- | :---------- | :--------------------------------- | :-------------------------------------------------------------------- |
| **UT-KIS-INI-001** | Unit        | `KISAPIHook.__init__`              | 환경 변수 정상 설정 시, 초기화 성공 검증                              |
| **UT-KIS-INI-002** | Unit        | `KISAPIHook.__init__`              | 환경 변수 누락 시, `KISAPIError` 예외 발생 검증                       |
| **UT-KIS-TKN-001** | Unit        | `KISAPIHook._get_new_access_token` | 신규 토큰 발급 성공 및 토큰 파일 생성/저장 검증                       |
| **UT-KIS-TKN-002** | Unit        | `KISAPIHook._get_new_access_token` | 네트워크 오류 시, `KISAuthenticationError` 예외 발생 검증             |
| **UT-KIS-TKN-003** | Unit        | `KISAPIHook.get_access_token`      | 유효한 파일 캐시로부터 토큰 조회 및 신규 발급 억제 검증               |
| **UT-KIS-REQ-001** | Unit        | `KISAPIHook._send_request`         | API 성공 응답(다중 output)에 대한 동적 파싱 기능 검증                 |
| **UT-KIS-REQ-002** | Unit        | `KISAPIHook._send_request`         | API 비즈니스 오류(`rt_cd` != '0') 발생 시 `KISDataError` 처리 검증    |
| **UT-KIS-REQ-003** | Unit        | `KISAPIHook._send_request`         | 네트워크 오류 발생 시, 3회 재시도 후 `KISDataError` 발생 검증         |
| **UT-KIS-WRP-001** | Unit        | `get_kr_stock_basic_info`          | `_send_request` 호출 시 파라미터(`path`, `tr_id` 등) 정확성 검증      |
| **UT-KIS-WRP-002** | Unit        | `get_kr_stock_balance_sheet`       | `_send_request` 호출 시 파라미터(`path`, `tr_id` 등) 정확성 검증      |
| **UT-KIS-WRP-003** | Unit        | `get_kr_stock_income_statement`    | `_send_request` 호출 시 파라미터(`path`, `tr_id` 등) 정확성 검증      |
| **UT-KIS-WRP-004** | Unit        | `get_kr_stock_financial_ratio`     | `_send_request` 호출 시 파라미터(`path`, `tr_id` 등) 정확성 검증      |
| **UT-KIS-WRP-005** | Unit        | `get_kr_stock_profit_ratio`        | `_send_request` 호출 시 파라미터(`path`, `tr_id` 등) 정확성 검증      |
| **UT-KIS-WRP-006** | Unit        | `get_kr_stock_other_major_ratio`   | `_send_request` 호출 시 파라미터(`path`, `tr_id` 등) 정확성 검증      |
| **UT-KIS-WRP-007** | Unit        | `get_kr_stock_stability_ratio`     | `_send_request` 호출 시 파라미터(`path`, `tr_id` 등) 정확성 검증      |
| **UT-KIS-WRP-008** | Unit        | `get_kr_stock_growth_ratio`        | `_send_request` 호출 시 파라미터(`path`, `tr_id` 등) 정확성 검증      |
| **UT-KIS-WRP-009** | Unit        | `get_kr_stock_inquire_price_basic` | 알려진 버그(잘못된 파라미터 전달)가 수정되지 않았음을 명시적으로 확인 |
| **UT-KIS-WRP-010** | Unit        | `get_kr_stock_dividend`            | `_send_request` 호출 시 파라미터(`path`, `tr_id` 등) 정확성 검증      |
| **UT-KIS-WRP-011** | Unit        | `get_kr_stock_estimate_perform`    | `_send_request` 호출 시 파라미터(`path`, `tr_id` 등) 정확성 검증      |
| **UT-KIS-WRP-012** | Unit        | `get_kr_stock_invest_opinion`      | `_send_request` 호출 시 파라미터(`path`, `tr_id` 등) 정확성 검증      |
| **UT-KIS-WRP-013** | Unit        | `get_kr_stock_invest_opbysec`      | `_send_request` 호출 시 파라미터(`path`, `tr_id` 등) 정확성 검증      |

## 2. 세부 테스트 케이스

### 초기화 (Initialization)

| 항목 (Field)         | 설명                                                                                                                                                                                                                                         |
| :------------------- | :------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **Test Case ID**     | `UT-KIS-INI-001`                                                                                                                                                                                                                             |
| **문서 ID**          | `FINSIGHT-TCS-ETL-001`                                                                                                                                                                                                                       |
| **테스트 유형**      | 단위 테스트 (Unit Test)                                                                                                                                                                                                                      |
| **테스트 대상**      | `KISAPIHook.__init__`                                                                                                                                                                                                                        |
| **테스트 목표**      | `KIS_APP_KEY`, `KIS_APP_SECRET` 환경 변수가 정상적으로 설정되었을 때, `KISAPIHook` 클래스의 인스턴스가 성공적으로 생성되고 속성에 키 값이 올바르게 할당되는지 검증한다.                                                                      |
| **사전 조건**        | • `pytest`의 `monkeypatch` fixture를 통해 `KIS_APP_KEY`와 `KIS_APP_SECRET` 환경 변수가 임시로 설정된 상태.                                                                                                                                   |
| **테스트 절차**      | 1. `KISAPIHook()`를 호출하여 클래스 인스턴스를 생성한다.<br>2. 생성된 인스턴스의 `app_key` 속성이 설정된 `KIS_APP_KEY`와 일치하는지 `assert`로 확인한다.<br>3. `app_secret` 속성이 설정된 `KIS_APP_SECRET`와 일치하는지 `assert`로 확인한다. |
| **테스트 데이터**    | • `KIS_APP_KEY`: "test_app_key"<br>• `KIS_APP_SECRET`: "test_app_secret"                                                                                                                                                                     |
| **예상 결과**        | • 예외 발생 없이 인스턴스 생성이 성공해야 한다.<br>• `hook.app_key`와 `hook.app_secret` 속성에 각각의 테스트 키 값이 정확히 할당되어야 한다.                                                                                                 |
| **판정 (PASS/FAIL)** | PASS                                                                                                                                                                                                                                         |

---

| 항목 (Field)         | 설명                                                                                                                                                                            |
| :------------------- | :------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| **Test Case ID**     | `UT-KIS-INI-002`                                                                                                                                                                |
| **문서 ID**          | `FINSIGHT-TCS-ETL-001`                                                                                                                                                          |
| **테스트 유형**      | 단위 테스트 (Unit Test)                                                                                                                                                         |
| **테스트 대상**      | `KISAPIHook.__init__`                                                                                                                                                           |
| **테스트 목표**      | 필수 환경 변수(`KIS_APP_KEY`, `KIS_APP_SECRET`)가 하나라도 설정되지 않았을 때, 시스템이 즉시 문제를 인지하고 `KISAPIError` 예외를 발생시키는지 검증한다.                        |
| **사전 조건**        | • `KIS_APP_KEY`와 `KIS_APP_SECRET` 환경 변수가 설정되지 않거나 `None`인 상태.                                                                                                   |
| **테스트 절차**      | 1. `pytest.raises(KISAPIError)` 컨텍스트 관리자를 사용하여 `KISAPIError` 예외 발생을 예상하도록 설정한다.<br>2. 컨텍스트 내에서 `KISAPIHook()` 클래스 인스턴스 생성을 시도한다. |
| **테스트 데이터**    | 해당 없음                                                                                                                                                                       |
| **예상 결과**        | `KISAPIError` 예외가 반드시 발생해야 한다.                                                                                                                                      |
| **판정 (PASS/FAIL)** | PASS                                                                                                                                                                            |

### 접근 토큰 관리 (Access Token Management)

| 항목 (Field)         | 설명                                                                                                                                                                                                                                                                                        |
| :------------------- | :------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| **Test Case ID**     | `UT-KIS-TKN-001`                                                                                                                                                                                                                                                                            |
| **문서 ID**          | `FINSIGHT-TCS-ETL-001`                                                                                                                                                                                                                                                                      |
| **테스트 유형**      | 단위 테스트 (Unit Test)                                                                                                                                                                                                                                                                     |
| **테스트 대상**      | `KISAPIHook._get_new_access_token`                                                                                                                                                                                                                                                          |
| **테스트 목표**      | KIS API 서버로부터 새로운 접근 토큰을 성공적으로 발급받고, 해당 토큰 정보를 지정된 파일 경로(`token_filepath`)에 올바르게 저장하는지 검증한다.                                                                                                                                              |
| **사전 조건**        | • `requests.post`가 상태 코드 200과 유효한 토큰 JSON 응답을 반환하도록 Mocking된 상태.                                                                                                                                                                                                      |
| **테스트 절차**      | 1. `requests.post`의 Mock 객체가 성공 응답을 반환하도록 설정한다.<br>2. `api_hook._get_new_access_token()` 메서드를 호출한다.<br>3. 반환된 토큰이 "Bearer " 접두사를 포함한 올바른 형식인지 확인한다.<br>4. `api_hook.token_filepath`에 해당하는 파일이 생성되었는지 `exists()`로 확인한다. |
| **테스트 데이터**    | • Mock 응답 JSON: `{"access_token": "new_dummy_token", "access_token_token_expired": "..."}`                                                                                                                                                                                                |
| **예상 결과**        | • 반환 값은 "Bearer new_dummy_token"이어야 한다.<br>• `token_filepath`에 해당하는 파일이 존재해야 한다.                                                                                                                                                                                     |
| **판정 (PASS/FAIL)** | PASS                                                                                                                                                                                                                                                                                        |

---

| 항목 (Field)         | 설명                                                                                                                                               |
| :------------------- | :------------------------------------------------------------------------------------------------------------------------------------------------- |
| **Test Case ID**     | `UT-KIS-TKN-002`                                                                                                                                   |
| **문서 ID**          | `FINSIGHT-TCS-ETL-001`                                                                                                                             |
| **테스트 유형**      | 단위 테스트 (Unit Test)                                                                                                                            |
| **테스트 대상**      | `KISAPIHook._get_new_access_token`                                                                                                                 |
| **테스트 목표**      | 네트워크 문제 등으로 KIS API 서버 접속에 실패했을 때, `KISAuthenticationError` 예외가 정상적으로 발생하는지 검증한다.                              |
| **사전 조건**        | • `requests.post`가 `requests.exceptions.RequestException` 예외를 발생시키도록 Mocking된 상태.                                                     |
| **테스트 절차**      | 1. `pytest.raises(KISAuthenticationError)` 컨텍스트 관리자를 설정한다.<br>2. 컨텍스트 내에서 `api_hook._get_new_access_token()` 메서드를 호출한다. |
| **테스트 데이터**    | 해당 없음                                                                                                                                          |
| **예상 결과**        | `KISAuthenticationError` 예외가 반드시 발생해야 한다.                                                                                              |
| **판정 (PASS/FAIL)** | PASS                                                                                                                                               |

---

| 항목 (Field)         | 설명                                                                                                                                                                                                                                                                                                             |
| :------------------- | :--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **Test Case ID**     | `UT-KIS-TKN-003`                                                                                                                                                                                                                                                                                                 |
| **문서 ID**          | `FINSIGHT-TCS-ETL-001`                                                                                                                                                                                                                                                                                           |
| **테스트 유형**      | 단위 테스트 (Unit Test)                                                                                                                                                                                                                                                                                          |
| **테스트 대상**      | `KISAPIHook.get_access_token`                                                                                                                                                                                                                                                                                    |
| **테스트 목표**      | 유효 기간이 남은 토큰 정보가 파일에 캐시되어 있을 경우, 불필요한 API 호출 없이 파일에서 토큰을 읽어오는지 검증한다.                                                                                                                                                                                              |
| **사전 조건**        | • `api_hook.token_filepath`에 만료되지 않은 유효한 토큰 정보가 저장되어 있는 상태.<br>• `_get_new_access_token` 메서드는 Mocking 처리된 상태.                                                                                                                                                                    |
| **테스트 절차**      | 1. 테스트용 임시 토큰 파일을 생성하고 유효한 토큰 정보를 JSON 형식으로 저장한다.<br>2. `api_hook.get_access_token()` 메서드를 호출한다.<br>3. 반환된 토큰 값이 파일에 저장된 토큰 값과 일치하는지 확인한다.<br>4. Mocking된 `_get_new_access_token` 메서드가 호출되지 않았음을 `assert_not_called()`로 검증한다. |
| **테스트 데이터**    | • 파일 캐시 내용: `{"access_token": "Bearer file_cached_token", "expired_at": "..."}`                                                                                                                                                                                                                            |
| **예상 결과**        | • 파일에 저장된 토큰 값("Bearer file_cached_token")이 정확히 반환되어야 한다.<br>• `_get_new_access_token` 메서드는 호출되지 않아야 한다.                                                                                                                                                                        |
| **판정 (PASS/FAIL)** | PASS                                                                                                                                                                                                                                                                                                             |

### 요청 및 응답 처리 (Request & Response)

| 항목 (Field)         | 설명                                                                                                                                                                                                                                        |
| :------------------- | :------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| **Test Case ID**     | `UT-KIS-REQ-001`                                                                                                                                                                                                                            |
| **문서 ID**          | `FINSIGHT-TCS-ETL-001`                                                                                                                                                                                                                      |
| **테스트 유형**      | 단위 테스트 (Unit Test)                                                                                                                                                                                                                     |
| **테스트 대상**      | `KISAPIHook._send_request`                                                                                                                                                                                                                  |
| **테스트 목표**      | API가 성공적으로 `output1`, `output2` 등 여러 블록의 데이터를 반환했을 때, 이를 하나의 리스트로 올바르게 병합하고 각 항목에 `data_source` 키를 추가하는지 검증한다.                                                                         |
| **사전 조건**        | • `requests.get`이 `rt_cd: '0'`과 함께 여러 `output` 블록을 포함한 JSON을 반환하도록 Mocking된 상태.<br>• `api_hook._access_token`에 임시 토큰 값이 할당된 상태.                                                                            |
| **테스트 절차**      | 1. `api_hook._send_request()` 메서드를 호출한다.<br>2. 반환된 리스트의 길이가 모든 `output` 블록의 항목 수를 합한 것과 같은지 확인한다.<br>3. 리스트의 각 항목에 `data_source` 키가 원본 `output` 키 이름으로 정확히 추가되었는지 확인한다. |
| **테스트 데이터**    | • Mock 응답 JSON: `{'rt_cd': '0', 'output1': [{}], 'output2': [{}]}`                                                                                                                                                                        |
| **예상 결과**        | • 모든 `output` 데이터가 병합된 리스트가 반환되어야 한다. (예: 길이 2)<br>• 각 딕셔너리 항목에 `data_source` 키가 존재해야 한다.                                                                                                            |
| **판정 (PASS/FAIL)** | PASS                                                                                                                                                                                                                                        |

---

| 항목 (Field)         | 설명                                                                                                                                                                                         |
| :------------------- | :------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **Test Case ID**     | `UT-KIS-REQ-002`                                                                                                                                                                             |
| **문서 ID**          | `FINSIGHT-TCS-ETL-001`                                                                                                                                                                       |
| **테스트 유형**      | 단위 테스트 (Unit Test)                                                                                                                                                                      |
| **테스트 대상**      | `KISAPIHook._send_request`                                                                                                                                                                   |
| **테스트 목표**      | API 응답의 `rt_cd`가 '0'이 아닌 비즈니스 오류일 경우, `KISDataError` 예외를 발생시키고 응답의 `msg1` 내용을 예외 메시지에 포함하는지 검증한다.                                               |
| **사전 조건**        | • `requests.get`이 `rt_cd: '1'`과 오류 메시지를 포함한 JSON을 반환하도록 Mocking된 상태.<br>• `api_hook._access_token`에 임시 토큰 값이 할당된 상태.                                         |
| **테스트 절차**      | 1. `pytest.raises(KISDataError)` 컨텍스트 관리자를 설정하고, `match` 인자를 사용해 기대하는 오류 메시지 패턴을 지정한다.<br>2. 컨텍스트 내에서 `api_hook._send_request()` 메서드를 호출한다. |
| **테스트 데이터**    | • Mock 응답 JSON: `{'rt_cd': '1', 'msg1': 'Error Message'}`                                                                                                                                  |
| **예상 결과**        | `KISDataError` 예외가 발생해야 하며, 예외 메시지에 `error_prefix`와 `msg1`의 내용이 포함되어야 한다. (예: "prefix 실패: Error Message")                                                      |
| **판정 (PASS/FAIL)** | PASS                                                                                                                                                                                         |

---

| 항목 (Field)         | 설명                                                                                                                                                                                                                                                                                                                     |
| :------------------- | :----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **Test Case ID**     | `UT-KIS-REQ-003`                                                                                                                                                                                                                                                                                                         |
| **문서 ID**          | `FINSIGHT-TCS-ETL-001`                                                                                                                                                                                                                                                                                                   |
| **테스트 유형**      | 단위 테스트 (Unit Test)                                                                                                                                                                                                                                                                                                  |
| **테스트 대상**      | `KISAPIHook._send_request`                                                                                                                                                                                                                                                                                               |
| **테스트 목표**      | 네트워크 오류가 계속 발생할 경우, 지정된 횟수(3회)만큼 재시도한 후 최종적으로 `KISDataError` 예외를 발생시키는지 검증한다.                                                                                                                                                                                               |
| **사전 조건**        | • `requests.get`이 `requests.exceptions.RequestException` 예외를 발생시키도록 Mocking된 상태.<br>• `time.sleep`은 테스트 속도를 위해 Mocking 처리된 상태.<br>• `api_hook._access_token`에 임시 토큰 값이 할당된 상태.                                                                                                    |
| **테스트 절차**      | 1. `pytest.raises(KISDataError)` 컨텍스트 관리자를 설정하고, `match` 인자를 사용해 기대하는 오류 메시지 패턴("API 서버 접속 실패")을 지정한다.<br>2. 컨텍스트 내에서 `api_hook._send_request()` 메서드를 호출한다.<br>3. 컨텍스트 종료 후, `requests.get`의 Mock 객체가 정확히 3번 호출되었는지 `call_count`로 검증한다. |
| **테스트 데이터**    | 해당 없음                                                                                                                                                                                                                                                                                                                |
| **예상 결과**        | • `KISDataError` 예외가 발생해야 한다.<br>• `requests.get`은 총 3회 호출되어야 한다.                                                                                                                                                                                                                                     |
| **판정 (PASS/FAIL)** | PASS                                                                                                                                                                                                                                                                                                                     |

### API 래퍼 (API Wrappers)

| 항목 (Field)         | 설명                                                                                                                                                                       |
| :------------------- | :------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **Test Case ID**     | `UT-KIS-WRP-001`                                                                                                                                                           |
| **문서 ID**          | `FINSIGHT-TCS-ETL-001`                                                                                                                                                     |
| **테스트 유형**      | 단위 테스트 (Unit Test)                                                                                                                                                    |
| **테스트 대상**      | `KISAPIHook.get_kr_stock_basic_info`                                                                                                                                       |
| **테스트 목표**      | `get_kr_stock_basic_info` 함수가 내부의 `_send_request`를 호출할 때, API 명세에 맞는 정확한 파라미터를 전달하는지 검증한다.                                                |
| **사전 조건**        | • `src.hooks.KIS_API_hook.KISAPIHook._send_request` 메서드가 `MagicMock` 객체로 Mocking된 상태.                                                                            |
| **테스트 절차**      | 1. `api_hook.get_kr_stock_basic_info("005930")`를 호출한다.<br>2. Mocking된 `_send_request`가 `assert_called_once_with()`를 통해, 정확한 인자로 1회 호출되었는지 검증한다. |
| **테스트 데이터**    | • `stock_code`: "005930"                                                                                                                                                   |
| **예상 결과**        | `_send_request`는 `path="/uapi/domestic-stock/v1/quotations/search-stock-info"`, `tr_id="CTPF1002R"` 등 고유 인자들로 1회 호출되어야 한다.                                 |
| **판정 (PASS/FAIL)** | PASS                                                                                                                                                                       |

---

| 항목 (Field)         | 설명                                                                                                                                                                          |
| :------------------- | :---------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **Test Case ID**     | `UT-KIS-WRP-002`                                                                                                                                                              |
| **문서 ID**          | `FINSIGHT-TCS-ETL-001`                                                                                                                                                        |
| **테스트 유형**      | 단위 테스트 (Unit Test)                                                                                                                                                       |
| **테스트 대상**      | `KISAPIHook.get_kr_stock_balance_sheet`                                                                                                                                       |
| **테스트 목표**      | `get_kr_stock_balance_sheet` 함수가 내부의 `_send_request`를 호출할 때, API 명세에 맞는 정확한 파라미터를 전달하는지 검증한다.                                                |
| **사전 조건**        | • `src.hooks.KIS_API_hook.KISAPIHook._send_request` 메서드가 `MagicMock` 객체로 Mocking된 상태.                                                                               |
| **테스트 절차**      | 1. `api_hook.get_kr_stock_balance_sheet("005930")`를 호출한다.<br>2. Mocking된 `_send_request`가 `assert_called_once_with()`를 통해, 정확한 인자로 1회 호출되었는지 검증한다. |
| **테스트 데이터**    | • `stock_code`: "005930"                                                                                                                                                      |
| **예상 결과**        | `_send_request`는 `path="/uapi/domestic-stock/v1/finance/balance-sheet"`, `tr_id="FHKST66430100"` 등 고유 인자들로 1회 호출되어야 한다.                                       |
| **판정 (PASS/FAIL)** | PASS                                                                                                                                                                          |

---

| 항목 (Field)         | 설명                                                                                                                                                                             |
| :------------------- | :------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **Test Case ID**     | `UT-KIS-WRP-003`                                                                                                                                                                 |
| **문서 ID**          | `FINSIGHT-TCS-ETL-001`                                                                                                                                                           |
| **테스트 유형**      | 단위 테스트 (Unit Test)                                                                                                                                                          |
| **테스트 대상**      | `KISAPIHook.get_kr_stock_income_statement`                                                                                                                                       |
| **테스트 목표**      | `get_kr_stock_income_statement` 함수가 내부의 `_send_request`를 호출할 때, API 명세에 맞는 정확한 파라미터를 전달하는지 검증한다.                                                |
| **사전 조건**        | • `src.hooks.KIS_API_hook.KISAPIHook._send_request` 메서드가 `MagicMock` 객체로 Mocking된 상태.                                                                                  |
| **테스트 절차**      | 1. `api_hook.get_kr_stock_income_statement("005930")`를 호출한다.<br>2. Mocking된 `_send_request`가 `assert_called_once_with()`를 통해, 정확한 인자로 1회 호출되었는지 검증한다. |
| **테스트 데이터**    | • `stock_code`: "005930"                                                                                                                                                         |
| **예상 결과**        | `_send_request`는 `path="/uapi/domestic-stock/v1/finance/income-statement"`, `tr_id="FHKST66430200"` 등 고유 인자들로 1회 호출되어야 한다.                                       |
| **판정 (PASS/FAIL)** | PASS                                                                                                                                                                             |

---

| 항목 (Field)         | 설명                                                                                                                                                                            |
| :------------------- | :------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| **Test Case ID**     | `UT-KIS-WRP-004`                                                                                                                                                                |
| **문서 ID**          | `FINSIGHT-TCS-ETL-001`                                                                                                                                                          |
| **테스트 유형**      | 단위 테스트 (Unit Test)                                                                                                                                                         |
| **테스트 대상**      | `KISAPIHook.get_kr_stock_financial_ratio`                                                                                                                                       |
| **테스트 목표**      | `get_kr_stock_financial_ratio` 함수가 내부의 `_send_request`를 호출할 때, API 명세에 맞는 정확한 파라미터를 전달하는지 검증한다.                                                |
| **사전 조건**        | • `src.hooks.KIS_API_hook.KISAPIHook._send_request` 메서드가 `MagicMock` 객체로 Mocking된 상태.                                                                                 |
| **테스트 절차**      | 1. `api_hook.get_kr_stock_financial_ratio("005930")`를 호출한다.<br>2. Mocking된 `_send_request`가 `assert_called_once_with()`를 통해, 정확한 인자로 1회 호출되었는지 검증한다. |
| **테스트 데이터**    | • `stock_code`: "005930"                                                                                                                                                        |
| **예상 결과**        | `_send_request`는 `path="/uapi/domestic-stock/v1/finance/financial-ratio"`, `tr_id="FHKST66430300"` 등 고유 인자들로 1회 호출되어야 한다.                                       |
| **판정 (PASS/FAIL)** | PASS                                                                                                                                                                            |

---

| 항목 (Field)         | 설명                                                                                                                                                                         |
| :------------------- | :--------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **Test Case ID**     | `UT-KIS-WRP-005`                                                                                                                                                             |
| **문서 ID**          | `FINSIGHT-TCS-ETL-001`                                                                                                                                                       |
| **테스트 유형**      | 단위 테스트 (Unit Test)                                                                                                                                                      |
| **테스트 대상**      | `KISAPIHook.get_kr_stock_profit_ratio`                                                                                                                                       |
| **테스트 목표**      | `get_kr_stock_profit_ratio` 함수가 내부의 `_send_request`를 호출할 때, API 명세에 맞는 정확한 파라미터를 전달하는지 검증한다.                                                |
| **사전 조건**        | • `src.hooks.KIS_API_hook.KISAPIHook._send_request` 메서드가 `MagicMock` 객체로 Mocking된 상태.                                                                              |
| **테스트 절차**      | 1. `api_hook.get_kr_stock_profit_ratio("005930")`를 호출한다.<br>2. Mocking된 `_send_request`가 `assert_called_once_with()`를 통해, 정확한 인자로 1회 호출되었는지 검증한다. |
| **테스트 데이터**    | • `stock_code`: "005930"                                                                                                                                                     |
| **예상 결과**        | `_send_request`는 `path="/uapi/domestic-stock/v1/finance/profit-ratio"`, `tr_id="FHKST66430400"` 등 고유 인자들로 1회 호출되어야 한다.                                       |
| **판정 (PASS/FAIL)** | PASS                                                                                                                                                                         |

---

| 항목 (Field)         | 설명                                                                                                                                                                              |
| :------------------- | :-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **Test Case ID**     | `UT-KIS-WRP-006`                                                                                                                                                                  |
| **문서 ID**          | `FINSIGHT-TCS-ETL-001`                                                                                                                                                            |
| **테스트 유형**      | 단위 테스트 (Unit Test)                                                                                                                                                           |
| **테스트 대상**      | `KISAPIHook.get_kr_stock_other_major_ratio`                                                                                                                                       |
| **테스트 목표**      | `get_kr_stock_other_major_ratio` 함수가 내부의 `_send_request`를 호출할 때, API 명세에 맞는 정확한 파라미터를 전달하는지 검증한다.                                                |
| **사전 조건**        | • `src.hooks.KIS_API_hook.KISAPIHook._send_request` 메서드가 `MagicMock` 객체로 Mocking된 상태.                                                                                   |
| **테스트 절차**      | 1. `api_hook.get_kr_stock_other_major_ratio("005930")`를 호출한다.<br>2. Mocking된 `_send_request`가 `assert_called_once_with()`를 통해, 정확한 인자로 1회 호출되었는지 검증한다. |
| **테스트 데이터**    | • `stock_code`: "005930"                                                                                                                                                          |
| **예상 결과**        | `_send_request`는 `path="/uapi/domestic-stock/v1/finance/other-major-ratios"`, `tr_id="FHKST66430500"` 등 고유 인자들로 1회 호출되어야 한다.                                      |
| **판정 (PASS/FAIL)** | PASS                                                                                                                                                                              |

---

| 항목 (Field)         | 설명                                                                                                                                                                            |
| :------------------- | :------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| **Test Case ID**     | `UT-KIS-WRP-007`                                                                                                                                                                |
| **문서 ID**          | `FINSIGHT-TCS-ETL-001`                                                                                                                                                          |
| **테스트 유형**      | 단위 테스트 (Unit Test)                                                                                                                                                         |
| **테스트 대상**      | `KISAPIHook.get_kr_stock_stability_ratio`                                                                                                                                       |
| **테스트 목표**      | `get_kr_stock_stability_ratio` 함수가 내부의 `_send_request`를 호출할 때, API 명세에 맞는 정확한 파라미터를 전달하는지 검증한다.                                                |
| **사전 조건**        | • `src.hooks.KIS_API_hook.KISAPIHook._send_request` 메서드가 `MagicMock` 객체로 Mocking된 상태.                                                                                 |
| **테스트 절차**      | 1. `api_hook.get_kr_stock_stability_ratio("005930")`를 호출한다.<br>2. Mocking된 `_send_request`가 `assert_called_once_with()`를 통해, 정확한 인자로 1회 호출되었는지 검증한다. |
| **테스트 데이터**    | • `stock_code`: "005930"                                                                                                                                                        |
| **예상 결과**        | `_send_request`는 `path="/uapi/domestic-stock/v1/finance/stability-ratio"`, `tr_id="FHKST66430600"` 등 고유 인자들로 1회 호출되어야 한다.                                       |
| **판정 (PASS/FAIL)** | PASS                                                                                                                                                                            |

---

| 항목 (Field)         | 설명                                                                                                                                                                         |
| :------------------- | :--------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **Test Case ID**     | `UT-KIS-WRP-008`                                                                                                                                                             |
| **문서 ID**          | `FINSIGHT-TCS-ETL-001`                                                                                                                                                       |
| **테스트 유형**      | 단위 테스트 (Unit Test)                                                                                                                                                      |
| **테스트 대상**      | `KISAPIHook.get_kr_stock_growth_ratio`                                                                                                                                       |
| **테스트 목표**      | `get_kr_stock_growth_ratio` 함수가 내부의 `_send_request`를 호출할 때, API 명세에 맞는 정확한 파라미터를 전달하는지 검증한다.                                                |
| **사전 조건**        | • `src.hooks.KIS_API_hook.KISAPIHook._send_request` 메서드가 `MagicMock` 객체로 Mocking된 상태.                                                                              |
| **테스트 절차**      | 1. `api_hook.get_kr_stock_growth_ratio("005930")`를 호출한다.<br>2. Mocking된 `_send_request`가 `assert_called_once_with()`를 통해, 정확한 인자로 1회 호출되었는지 검증한다. |
| **테스트 데이터**    | • `stock_code`: "005930"                                                                                                                                                     |
| **예상 결과**        | `_send_request`는 `path="/uapi/domestic-stock/v1/finance/growth-ratio"`, `tr_id="FHKST66430800"` 등 고유 인자들로 1회 호출되어야 한다.                                       |
| **판정 (PASS/FAIL)** | PASS                                                                                                                                                                         |

---

| 항목 (Field)         | 설명                                                                                                                                                                                                                                                                                   |
| :------------------- | :------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **Test Case ID**     | `UT-KIS-WRP-009`                                                                                                                                                                                                                                                                       |
| **문서 ID**          | `FINSIGHT-TCS-ETL-001`                                                                                                                                                                                                                                                                 |
| **테스트 유형**      | 단위 테스트 (Unit Test)                                                                                                                                                                                                                                                                |
| **테스트 대상**      | `KISAPIHook.get_kr_stock_inquire_price_basic`                                                                                                                                                                                                                                          |
| **테스트 목표**      | 해당 함수에 존재하는 **알려진 버그**(현재가 조회가 아닌 성장성비율 조회 API를 호출하는 문제)가 수정되지 않은 현재 상태를 명시적으로 검증한다. 이 테스트는 향후 해당 버그가 올바르게 수정될 경우 **실패**하게 되며, 이를 통해 수정이 올바르게 이루어졌음을 역으로 보장하는 역할을 한다. |
| **사전 조건**        | • `src.hooks.KIS_API_hook.KISAPIHook._send_request` 메서드가 `MagicMock` 객체로 Mocking된 상태.                                                                                                                                                                                        |
| **테스트 절차**      | 1. `api_hook.get_kr_stock_inquire_price_basic("005930")`를 호출한다.<br>2. Mocking된 `_send_request`가 `assert_called_once_with()`를 통해, 현재 코드에 **잘못 구현된** `path`와 `tr_id`로 호출되었는지 검증한다.                                                                       |
| **테스트 데이터**    | • `stock_code`: "005930"                                                                                                                                                                                                                                                               |
| **예상 결과**        | `_send_request`는 현재 코드의 버그 상태와 동일하게, '성장성비율 조회'에 해당하는 `path`와 `tr_id` 인자를 가지고 1회 호출되어야 한다.                                                                                                                                                   |
| **판정 (PASS/FAIL)** | PASS                                                                                                                                                                                                                                                                                   |

---

| 항목 (Field)         | 설명                                                                                                                                                                                             |
| :------------------- | :----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **Test Case ID**     | `UT-KIS-WRP-010`                                                                                                                                                                                 |
| **문서 ID**          | `FINSIGHT-TCS-ETL-001`                                                                                                                                                                           |
| **테스트 유형**      | 단위 테스트 (Unit Test)                                                                                                                                                                          |
| **테스트 대상**      | `KISAPIHook.get_kr_stock_dividend`                                                                                                                                                               |
| **테스트 목표**      | `get_kr_stock_dividend` 함수가 내부의 `_send_request`를 호출할 때, API 명세에 맞는 정확한 파라미터를 전달하는지 검증한다.                                                                        |
| **사전 조건**        | • `src.hooks.KIS_API_hook.KISAPIHook._send_request` 메서드가 `MagicMock` 객체로 Mocking된 상태.                                                                                                  |
| **테스트 절차**      | 1. `api_hook.get_kr_stock_dividend("005930", "20240101", "20241231")`를 호출한다.<br>2. Mocking된 `_send_request`가 `assert_called_once_with()`를 통해, 정확한 인자로 1회 호출되었는지 검증한다. |
| **테스트 데이터**    | • `stock_code`: "005930"<br>• `start_date`: "20240101"<br>• `end_date`: "20241231"                                                                                                               |
| **예상 결과**        | `_send_request`는 `path="/uapi/domestic-stock/v1/ksdinfo/dividend"`, `tr_id="HHKDB669102C0"` 등 고유 인자들로 1회 호출되어야 한다.                                                               |
| **판정 (PASS/FAIL)** | PASS                                                                                                                                                                                             |

---

| 항목 (Field)         | 설명                                                                                                                                                                             |
| :------------------- | :------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **Test Case ID**     | `UT-KIS-WRP-011`                                                                                                                                                                 |
| **문서 ID**          | `FINSIGHT-TCS-ETL-001`                                                                                                                                                           |
| **테스트 유형**      | 단위 테스트 (Unit Test)                                                                                                                                                          |
| **테스트 대상**      | `KISAPIHook.get_kr_stock_estimate_perform`                                                                                                                                       |
| **테스트 목표**      | `get_kr_stock_estimate_perform` 함수가 내부의 `_send_request`를 호출할 때, API 명세에 맞는 정확한 파라미터를 전달하는지 검증한다.                                                |
| **사전 조건**        | • `src.hooks.KIS_API_hook.KISAPIHook._send_request` 메서드가 `MagicMock` 객체로 Mocking된 상태.                                                                                  |
| **테스트 절차**      | 1. `api_hook.get_kr_stock_estimate_perform("005930")`를 호출한다.<br>2. Mocking된 `_send_request`가 `assert_called_once_with()`를 통해, 정확한 인자로 1회 호출되었는지 검증한다. |
| **테스트 데이터**    | • `stock_code`: "005930"                                                                                                                                                         |
| **예상 결과**        | `_send_request`는 `path="/uapi/domestic-stock/v1/quotations/estimate-perform"`, `tr_id="HHKST668300C0"` 등 고유 인자들로 1회 호출되어야 한다.                                    |
| **판정 (PASS/FAIL)** | PASS                                                                                                                                                                             |

---

| 항목 (Field)         | 설명                                                                                                                                                                                                   |
| :------------------- | :----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **Test Case ID**     | `UT-KIS-WRP-012`                                                                                                                                                                                       |
| **문서 ID**          | `FINSIGHT-TCS-ETL-001`                                                                                                                                                                                 |
| **테스트 유형**      | 단위 테스트 (Unit Test)                                                                                                                                                                                |
| **테스트 대상**      | `KISAPIHook.get_kr_stock_invest_opinion`                                                                                                                                                               |
| **테스트 목표**      | `get_kr_stock_invest_opinion` 함수가 내부의 `_send_request`를 호출할 때, API 명세에 맞는 정확한 파라미터를 전달하는지 검증한다.                                                                        |
| **사전 조건**        | • `src.hooks.KIS_API_hook.KISAPIHook._send_request` 메서드가 `MagicMock` 객체로 Mocking된 상태.                                                                                                        |
| **테스트 절차**      | 1. `api_hook.get_kr_stock_invest_opinion("005930", "20240101", "20241231")`를 호출한다.<br>2. Mocking된 `_send_request`가 `assert_called_once_with()`를 통해, 정확한 인자로 1회 호출되었는지 검증한다. |
| **테스트 데이터**    | • `stock_code`: "005930"<br>• `start_date`: "20240101"<br>• `end_date`: "20241231"                                                                                                                     |
| **예상 결과**        | `_send_request`는 `path="/uapi/domestic-stock/v1/quotations/invest-opinion"`, `tr_id="FHKST663300C0"` 등 고유 인자들로 1회 호출되어야 한다.                                                            |
| **판정 (PASS/FAIL)** | PASS                                                                                                                                                                                                   |

---

| 항목 (Field)         | 설명                                                                                                                                                                                                   |
| :------------------- | :----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **Test Case ID**     | `UT-KIS-WRP-013`                                                                                                                                                                                       |
| **문서 ID**          | `FINSIGHT-TCS-ETL-001`                                                                                                                                                                                 |
| **테스트 유형**      | 단위 테스트 (Unit Test)                                                                                                                                                                                |
| **테스트 대상**      | `KISAPIHook.get_kr_stock_invest_opbysec`                                                                                                                                                               |
| **테스트 목표**      | `get_kr_stock_invest_opbysec` 함수가 내부의 `_send_request`를 호출할 때, API 명세에 맞는 정확한 파라미터를 전달하는지 검증한다.                                                                        |
| **사전 조건**        | • `src.hooks.KIS_API_hook.KISAPIHook._send_request` 메서드가 `MagicMock` 객체로 Mocking된 상태.                                                                                                        |
| **테스트 절차**      | 1. `api_hook.get_kr_stock_invest_opbysec("005930", "20240101", "20241231")`를 호출한다.<br>2. Mocking된 `_send_request`가 `assert_called_once_with()`를 통해, 정확한 인자로 1회 호출되었는지 검증한다. |
| **테스트 데이터**    | • `stock_code`: "005930"<br>• `start_date`: "20240101"<br>• `end_date`: "20241231"                                                                                                                     |
| **예상 결과**        | `_send_request`는 `path="/uapi/domestic-stock/v1/quotations/invest-opbysec"`, `tr_id="FHKST663400C0"` 등 고유 인자들로 1회 호출되어야 한다.                                                            |
| **판정 (PASS/FAIL)** | PASS                                                                                                                                                                                                   |
