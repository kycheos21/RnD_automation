# NTIS 크롤링 자동화 프로젝트 설치 요구사항

## 1. 필수 설치 프로그램

### 1.1 개발 환경
- **Python 3.8 이상**
  - 공식 사이트: https://www.python.org/downloads/
  - 설치 시 "Add Python to PATH" 체크 필수
  - 버전 확인: `python --version`

- **Node.js 18 이상** (Firecrawl 사용을 위해)
  - 공식 사이트: https://nodejs.org/
  - LTS 버전 권장
  - 버전 확인: `node --version`, `npm --version`

### 1.2 코드 에디터
- **Cursor** (AI 기반 코딩 어시스턴트)
  - 공식 사이트: https://cursor.sh/
  - 또는 **VS Code** + AI 확장프로그램

### 1.3 Git (버전 관리)
- **Git for Windows**
  - 공식 사이트: https://git-scm.com/download/win
  - 버전 확인: `git --version`

## 2. Python 패키지 설치

### 2.1 가상환경 생성 (권장)
```bash
# 가상환경 생성
python -m venv venv

# 가상환경 활성화 (Windows)
venv\Scripts\activate

# 가상환경 활성화 (Mac/Linux)
source venv/bin/activate
```

### 2.2 필수 Python 라이브러리
```bash
pip install pandas openpyxl schedule requests beautifulsoup4
```

#### 각 라이브러리 용도:
- **pandas**: 데이터 분석 및 엑셀 처리
- **openpyxl**: 엑셀 파일 생성 및 스타일링
- **schedule**: 작업 스케줄링 (매일 오전 9시 실행)
- **requests**: HTTP 요청 (API 호출용)
- **beautifulsoup4**: HTML 파싱 (보조 크롤링용)

## 3. Firecrawl 설정

### 3.1 Firecrawl 계정 및 API 키
1. **Firecrawl 회원가입**
   - 사이트: https://firecrawl.dev/
   - 무료 플랜: 월 500 크레딧 제공

2. **API 키 발급**
   - 대시보드에서 API 키 생성
   - 환경변수로 저장 필요

### 3.2 Node.js Firecrawl SDK 설치
```bash
npm init -y
npm install @mendable/firecrawl-js
```

### 3.3 Python Firecrawl SDK 설치
```bash
pip install firecrawl-py
```

## 4. 이메일 설정 준비사항

### 4.1 회사 웹메일 SMTP 정보 확인
**IT 담당자에게 문의할 정보:**
- SMTP 서버 주소 (예: mail.company.co.kr)
- SMTP 포트 번호 (587, 465, 25 중 하나)
- 보안 프로토콜 (TLS, SSL)
- 인증 방식

### 4.2 대안: Gmail SMTP (테스트용)
- Gmail 계정 필요
- 2단계 인증 설정
- 앱 비밀번호 생성
- SMTP 설정:
  - 서버: smtp.gmail.com
  - 포트: 587 (TLS)

## 5. 선택적 설치 프로그램

### 5.1 데이터베이스 (향후 확장용)
- **SQLite** (Python 기본 포함)
- **PostgreSQL** 또는 **MySQL** (대용량 데이터 처리 시)

### 5.2 작업 관리 도구
- **Postman** (API 테스트용)
- **DB Browser for SQLite** (데이터 확인용)

### 5.3 배포 관련 (클라우드 배포 시)
- **Docker** (컨테이너화)
- **AWS CLI** 또는 **Google Cloud SDK**

## 6. 환경 변수 설정

### 6.1 .env 파일 생성
프로젝트 루트에 `.env` 파일 생성:
```env
# Firecrawl API
FIRECRAWL_API_KEY=your_firecrawl_api_key_here

# Email Settings
SMTP_SERVER=mail.company.co.kr
SMTP_PORT=587
EMAIL_USER=your_email@company.co.kr
EMAIL_PASSWORD=your_password
EMAIL_TO=team@company.co.kr

# Search Keywords
SEARCH_KEYWORDS=AI,인공지능,디지털전환,스마트팩토리
```

### 6.2 환경변수 로드용 라이브러리
```bash
pip install python-dotenv
```

## 7. 설치 검증 스크립트

### 7.1 requirements.txt 생성
```txt
pandas>=1.5.0
openpyxl>=3.0.0
schedule>=1.2.0
requests>=2.28.0
beautifulsoup4>=4.11.0
firecrawl-py>=0.0.8
python-dotenv>=1.0.0
```

### 7.2 설치 검증 코드
```python
# check_installation.py
def check_python_packages():
    required_packages = [
        'pandas', 'openpyxl', 'schedule', 
        'requests', 'bs4', 'firecrawl', 'dotenv'
    ]
    
    for package in required_packages:
        try:
            __import__(package)
            print(f"✅ {package} 설치됨")
        except ImportError:
            print(f"❌ {package} 설치 필요")

def check_environment():
    import os
    required_env = ['FIRECRAWL_API_KEY', 'SMTP_SERVER', 'EMAIL_USER']
    
    for env_var in required_env:
        if os.getenv(env_var):
            print(f"✅ {env_var} 설정됨")
        else:
            print(f"❌ {env_var} 설정 필요")

if __name__ == "__main__":
    print("=== Python 패키지 확인 ===")
    check_python_packages()
    
    print("\n=== 환경변수 확인 ===")
    check_environment()
```

## 8. 설치 순서 요약

1. **Python 3.8+ 설치** (PATH 추가)
2. **Node.js 18+ 설치**
3. **Git 설치**
4. **Cursor 또는 VS Code 설치**
5. **프로젝트 폴더 생성 및 이동**
6. **Python 가상환경 생성 및 활성화**
7. **Python 패키지 설치** (`pip install -r requirements.txt`)
8. **Firecrawl 계정 생성 및 API 키 발급**
9. **Node.js Firecrawl SDK 설치**
10. **환경변수 파일(.env) 생성**
11. **회사 SMTP 정보 확인 및 설정**
12. **설치 검증 스크립트 실행**

## 9. 트러블슈팅

### 9.1 Python PATH 문제
- Windows: 시스템 환경변수에서 Python 경로 추가
- 재부팅 후 `python --version` 확인

### 9.2 pip 설치 오류
```bash
# pip 업그레이드
python -m pip install --upgrade pip

# 특정 패키지 설치 실패 시
pip install --user 패키지명
```

### 9.3 방화벽/보안 이슈
- 회사 방화벽에서 SMTP 포트 차단 시 IT 담당자 문의
- Firecrawl API 접근 차단 시 프록시 설정 필요

이 설치 가이드를 따라하시면 개발 환경 구성이 완료됩니다!

