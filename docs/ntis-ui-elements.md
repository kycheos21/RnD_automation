# NTIS 웹사이트 UI 요소 매핑

## 설정 정보
- **업데이트 날짜**: 2024-09-24
- **테스트 URL**: https://www.ntis.go.kr/rndgate/eg/un/ra/mng.do
- **브라우저**: Chrome (최신버전)

## 검색 관련 UI 요소

### 검색키워드 설정
```
# 기본 검색키워드 (우선순위 순)
PRIMARY_KEYWORDS=AI,스마트팩토리
SECONDARY_KEYWORDS=빅데이터,IoT,블록체인,클라우드
TERTIARY_KEYWORDS=스마트팩토리,디지털트윈,메타버스,NFT

# 제외 키워드 (검색 결과에서 필터링)
EXCLUDE_KEYWORDS=완료,마감,종료,취소

# 검색 옵션
SEARCH_TYPE=본공고
SEARCH_LIMIT=100
SEARCH_SORT=마감일순
```

### 검색 입력창
```
ID=searchKeyword
NAME=searchKeyword
TYPE=text
PLACEHOLDER=국가R&D통합공고 키워드 검색
TITLE=국가R&D통합공고 키워드 검색
STYLE=width: 712px
TABINDEX=6
```

### 검색 버튼
```
TAG=a
CLASS=button blue
ONCLICK=javascript: fn_search('1', ''); return false;
TEXT=검색
HREF=#content
```

## 검색 결과 페이지 UI 요소

### 리스트 개수 선택 드롭다운
```
TAG=select
NAME=pageUnit
TITLE=리스트 개수
CLASS=selbp90
STYLE=width: 100px; height: 39px; margin-right: -5px; margin-top: -3px;
OPTIONS=10,20,30,50,100
DEFAULT_VALUE=10
TARGET_VALUE=30
```

### 결과 리스트 컨테이너
```
# 추후 검색 결과 분석 후 추가
CLASS=
ID=
```

### 페이지네이션
```
# 추후 페이지 이동 분석 후 추가
CLASS=
ID=
```

## 공고 상세 정보 UI 요소

### 공고 제목
```
# 추후 상세 페이지 분석 후 추가
CLASS=
ID=
```

### 첨부파일 다운로드
```
# 추후 HWP 파일 다운로드 분석 후 추가
CLASS=
ID=
```

---

## 사용 방법

이 설정 파일은 `config_reader.py`에서 자동으로 파싱되어 Selenium 테스트에 사용됩니다.

### 설정 형식
```
ELEMENT_NAME=
ID=element_id
CLASS=element_class
TAG=element_tag
SELECTOR=css_selector
```

### 우선순위
1. ID (가장 빠르고 정확)
2. CLASS + 속성 조합
3. CSS 셀렉터
4. XPath (최후의 수단)
