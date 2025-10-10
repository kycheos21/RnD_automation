# 테스트 가이드

NTIS 자동화 프로젝트의 단위 테스트 및 통합 테스트에 대한 가이드입니다.

## 📋 목차

- [테스트 구조](#테스트-구조)
- [테스트 설정](#테스트-설정)
- [테스트 실행](#테스트-실행)
- [테스트 유형](#테스트-유형)
- [코드 커버리지](#코드-커버리지)
- [CI/CD 통합](#ci-cd-통합)

## 🗂️ 테스트 구조

```
tests/
├── __init__.py
├── test_announcement_db.py      # 데이터베이스 관리 테스트
├── test_claude_summarizer.py    # Claude API 요약기 테스트
├── test_hwp_processor.py        # HWP 처리기 테스트
├── test_hwp_parser.py          # HWP 파서 테스트
├── test_excel_generator.py     # 엑셀 생성기 테스트
└── test_integration.py         # 통합 테스트

conftest.py                     # pytest 설정 및 픽스처
pytest.ini                     # pytest 설정 파일
requirements-test.txt           # 테스트 의존성
run_tests.py                   # 테스트 실행 스크립트
```

## ⚙️ 테스트 설정

### 1. 테스트 의존성 설치

```bash
# 테스트 의존성 설치
pip install -r requirements-test.txt

# 또는 스크립트로 설치
python run_tests.py --install
```

### 2. 환경변수 설정

```bash
# Claude API 테스트용 (선택사항)
export ANTHROPIC_API_KEY="your_api_key_here"
```

## 🚀 테스트 실행

### 기본 테스트 실행

```bash
# 빠른 테스트 (기본)
python run_tests.py

# 또는 직접 pytest 사용
pytest tests/ -v -m "not slow and not selenium and not api"
```

### 상세 테스트 옵션

```bash
# 단위 테스트만
python run_tests.py --unit

# 통합 테스트만
python run_tests.py --integration

# 모든 테스트 (Selenium 제외)
python run_tests.py --all

# 코드 커버리지와 함께
python run_tests.py --coverage

# API 테스트 (실제 API 키 필요)
python run_tests.py --api

# Selenium 테스트 (브라우저 필요)
python run_tests.py --selenium

# HTML 테스트 리포트 생성
python run_tests.py --report
```

### pytest 직접 사용

```bash
# 특정 파일만 테스트
pytest tests/test_announcement_db.py -v

# 특정 테스트 함수만
pytest tests/test_announcement_db.py::TestAnnouncementDatabase::test_init_with_new_database -v

# 마커별 실행
pytest -m unit -v                    # 단위 테스트만
pytest -m integration -v             # 통합 테스트만
pytest -m "not slow" -v              # 빠른 테스트만
```

## 🏷️ 테스트 유형

### 테스트 마커

- `@pytest.mark.unit`: 단위 테스트
- `@pytest.mark.integration`: 통합 테스트
- `@pytest.mark.slow`: 오래 걸리는 테스트
- `@pytest.mark.api`: API 호출 테스트
- `@pytest.mark.selenium`: Selenium 브라우저 테스트

### 테스트 카테고리

#### 1. 단위 테스트 (Unit Tests)
- 개별 함수/메서드의 기능 테스트
- Mock 객체를 사용하여 의존성 격리
- 빠른 실행 속도

```python
@pytest.mark.unit
def test_extract_announcement_id_from_link(self):
    """링크에서 공고 ID 추출 테스트"""
    db = AnnouncementDatabase()
    announcement = {
        "링크": "https://www.ntis.go.kr/rndgate/eg/un/ra/view.do?roRndUid=1246080"
    }
    result = db.extract_announcement_id(announcement)
    assert result == "1246080"
```

#### 2. 통합 테스트 (Integration Tests)
- 여러 모듈 간의 상호작용 테스트
- 실제 파일 시스템 사용
- 전체 워크플로우 검증

```python
@pytest.mark.integration
def test_database_and_excel_integration(self, temp_db_file, multiple_sample_announcements):
    """데이터베이스와 엑셀 생성기 통합 테스트"""
    # 데이터베이스에 공고 추가 → 엑셀 리포트 생성
```

#### 3. API 테스트
- 실제 Claude API 호출 테스트
- API 키 필요
- 비용이 발생할 수 있음

```python
@pytest.mark.api
def test_real_api_call(self, sample_hwp_text):
    """실제 API 호출 테스트 (API 키 필요)"""
    api_key = os.getenv("ANTHROPIC_API_KEY")
    if not api_key or not api_key.startswith("sk-"):
        pytest.skip("실제 API 키가 필요합니다")
```

#### 4. Selenium 테스트
- 브라우저 자동화 테스트
- 실제 웹사이트 접근
- 수동 실행 권장

```python
@pytest.mark.selenium
def test_browser_interaction(self, mock_driver):
    """브라우저 상호작용 테스트"""
```

## 📊 코드 커버리지

### 커버리지 리포트 생성

```bash
# HTML 커버리지 리포트
python run_tests.py --coverage

# 리포트 확인
open htmlcov/index.html  # macOS
start htmlcov/index.html # Windows
```

### 커버리지 목표

- **전체 커버리지**: 80% 이상
- **핵심 모듈**: 90% 이상
- **테스트 제외 영역**: GUI 코드, 외부 API 호출 등

## 🔧 픽스처 (Fixtures)

### 기본 픽스처

- `temp_db_file`: 임시 데이터베이스 파일
- `sample_announcement`: 샘플 공고 데이터
- `multiple_sample_announcements`: 여러 샘플 공고
- `sample_hwp_text`: 샘플 HWP 텍스트
- `mock_selenium_driver`: Mock WebDriver
- `mock_claude_client`: Mock Claude API 클라이언트

### 사용 예시

```python
def test_my_function(self, temp_db_file, sample_announcement):
    """픽스처를 사용한 테스트"""
    db = AnnouncementDatabase(temp_db_file)
    result = db.add_announcement(sample_announcement)
    assert result is True
```

## 🐛 디버깅 및 트러블슈팅

### 테스트 실패 시

1. **상세 정보 확인**:
   ```bash
   pytest tests/test_module.py -v --tb=long
   ```

2. **특정 테스트만 실행**:
   ```bash
   pytest tests/test_module.py::TestClass::test_function -v -s
   ```

3. **디버그 모드**:
   ```bash
   pytest tests/test_module.py --pdb
   ```

### 일반적인 문제

1. **ImportError**: 프로젝트 루트에서 실행하세요
2. **API 키 오류**: ANTHROPIC_API_KEY 환경변수 확인
3. **파일 권한 오류**: 임시 디렉토리 권한 확인
4. **Selenium 오류**: Chrome 드라이버 설치 확인

## 📈 성능 테스트

### 대용량 데이터 테스트

```python
@pytest.mark.slow
def test_large_dataset_processing(self, temp_db_file):
    """대량 데이터 처리 테스트"""
    # 100개 공고 처리
```

### 메모리 사용량 모니터링

```bash
# 메모리 프로파일링
pytest tests/test_integration.py --memray
```

## 🚀 CI/CD 통합

### GitHub Actions 예시

```yaml
name: Tests
on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - name: Set up Python
        uses: actions/setup-python@v3
        with:
          python-version: '3.9'
      - name: Install dependencies
        run: |
          pip install -r requirements.txt
          pip install -r requirements-test.txt
      - name: Run tests
        run: python run_tests.py --coverage
      - name: Upload coverage
        uses: codecov/codecov-action@v3
```

## 📋 테스트 작성 가이드

### 좋은 테스트 작성 원칙

1. **명확한 테스트 이름**: 테스트하는 기능이 명확히 드러나도록
2. **단일 책임**: 하나의 테스트는 하나의 기능만 검증
3. **독립성**: 테스트 간 의존성 없이 독립 실행 가능
4. **반복 가능성**: 몇 번 실행해도 같은 결과

### 테스트 패턴

```python
def test_function_name_expected_behavior():
    """테스트 설명"""
    # Arrange (준비)
    input_data = {"key": "value"}
    
    # Act (실행)
    result = function_under_test(input_data)
    
    # Assert (검증)
    assert result == expected_output
    assert "key" in result
```

## 📚 추가 리소스

- [pytest 공식 문서](https://docs.pytest.org/)
- [Python Mock 가이드](https://docs.python.org/3/library/unittest.mock.html)
- [코드 커버리지 best practices](https://pytest-cov.readthedocs.io/)

## 🤝 기여 가이드

새로운 기능을 추가할 때는:

1. 해당 기능에 대한 단위 테스트 작성
2. 통합 테스트에 시나리오 추가
3. 모든 테스트가 통과하는지 확인
4. 코드 커버리지 80% 이상 유지

---

**문의사항이나 개선 제안이 있으시면 이슈를 등록해주세요!** 🚀



