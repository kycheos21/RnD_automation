# NTIS 크롤링 자동화 프로젝트 설치 가이드 📋

## 📅 최종 업데이트
**확인일**: 2025년 9월 2일  
**시스템 환경**: Windows NT x64 10.0.26100

---

## ✅ 설치 완료 현황

### 1.1 기본 개발 환경 ✅ **완료**

| 프로그램 | 설치된 버전 | 요구사항 | 상태 | 확인 명령어 |
|----------|-------------|----------|------|-------------|
| **Python** | 3.13.7 | 3.8+ | ✅ **충족** | `py --version` |
| **Node.js** | v22.18.0 | 18+ | ✅ **충족** | `node --version` |
| **npm** | 10.9.3 | - | ✅ **설치됨** | `npm --version` |
| **Git** | 2.50.1 | - | ✅ **설치됨** | `git --version` |

### 1.2 개발 도구 ✅ **완료**

| 도구 | 버전 정보 | 상태 |
|------|-----------|------|
| **Cursor IDE** | Version 1.5.5 (user setup) | ✅ **사용 중** |
| **VSCode Engine** | 1.99.3 | ✅ **최신** |
| **Electron** | 34.5.8 | ✅ **최신** |

---

## 🚀 설치 가이드 (신규 설치 시)

### 1단계: 기본 프로그램 설치

#### Python 3.8+ 설치
- **공식 사이트**: https://www.python.org/downloads/
- **설치 시 주의**: "Add Python to PATH" 체크 필수
- **Windows 명령어**: `py --version` (python 대신 py 사용)

#### Node.js 18+ 설치  
- **공식 사이트**: https://nodejs.org/
- **권장**: LTS 버전
- **확인**: `node --version`, `npm --version`

#### Git 설치
- **공식 사이트**: https://git-scm.com/download/win
- **확인**: `git --version`

#### 코드 에디터 설치
- **Cursor** (AI 기반, 추천): https://cursor.sh/
- **또는 VS Code**: https://code.visualstudio.com/

---

## 📦 Python 환경 설정

### 2.1 가상환경 생성 ✅ **완료**
```powershell
# Windows에서 가상환경 생성
py -m venv venv

# 가상환경 활성화
venv\Scripts\activate

# 성공 시 (venv) 표시됨
(venv) PS C:\Users\kyche\Desktop\kycheos_workspace\01RND_auto>
```

### 2.2 설치된 Python 패키지 ✅ **완료**

| 패키지 | 설치된 버전 | 용도 | 상태 |
|--------|-------------|------|------|
| **pandas** | 2.3.2 | 데이터 분석, 엑셀 처리 | ✅ |
| **openpyxl** | 3.1.5 | 엑셀 파일 생성/스타일링 | ✅ |
| **schedule** | 1.2.2 | 작업 스케줄링 | ✅ |
| **requests** | 2.32.5 | HTTP 요청, API 호출 | ✅ |
| **beautifulsoup4** | 4.13.5 | HTML 파싱 | ✅ |
| **firecrawl-py** | 4.3.1 | Firecrawl Python SDK | ✅ |
| **python-dotenv** | 1.1.1 | 환경변수 관리 | ✅ |

**의존성 패키지**: numpy 2.3.2, urllib3 2.5.0 등 30+ 개 자동 설치 ✅

### 2.3 신규 설치 시 명령어
```bash
# 전체 패키지 설치
pip install pandas openpyxl schedule requests beautifulsoup4 firecrawl-py python-dotenv

# 또는 requirements.txt 사용
pip install -r requirements.txt
```

---

## 🔥 Firecrawl API 설정

### 3.1 API 연동 설정 ✅ **완료**
- [x] Firecrawl 계정 생성 (https://firecrawl.dev/)
- [x] API 키 발급: `fc-6c348fc20f0045a2bf8601c1d99a559c`
- [x] `.env` 파일 구성
- [x] API 연결 테스트 성공

### 3.2 신규 설정 시 절차
1. **Firecrawl 회원가입**
   - 사이트: https://firecrawl.dev/
   - 무료 플랜: 월 500 크레딧 제공

2. **API 키 발급**
   - 대시보드에서 API 키 생성
   - `.env` 파일에 저장

3. **Python SDK 설치**
   ```bash
   pip install firecrawl-py
   ```

4. **API 테스트**
   ```bash
   python test_firecrawl.py
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

---

## 📁 프로젝트 구조

### 5.1 현재 프로젝트 구조 ✅ **완료**
```
C:\Users\kyche\Desktop\kycheos_workspace\01RND_auto\
├── docs\                           # 문서 폴더
│   ├── development-roadmap.md       # 개발 로드맵
│   ├── setup-requirements.md       # 현재 파일
│   └── project-overview.md          # 프로젝트 개요
├── venv\                           # Python 가상환경
├── test_firecrawl.py               # API 테스트 코드
├── .env                            # 환경변수 파일
└── README.md                       # 프로젝트 설명
```

---

## ⚙️ 환경 변수 설정

### 6.1 .env 파일 설정 ✅ **완료**
현재 설정된 환경변수:
```env
# Firecrawl API (설정 완료)
FIRECRAWL_API_KEY=fc-6c348fc20f0045a2bf8601c1d99a559c

# 이메일 설정 (향후 설정 예정)
# SMTP_SERVER=mail.company.co.kr
# SMTP_PORT=587
# EMAIL_USER=your_email@company.co.kr
# EMAIL_PASSWORD=your_password
# EMAIL_TO=team@company.co.kr

# 검색 키워드 (향후 설정)
# SEARCH_KEYWORDS=AI,인공지능,디지털전환,스마트팩토리
```

### 6.2 신규 설정 시 절차
1. 프로젝트 루트에 `.env` 파일 생성
2. 위의 템플릿 복사
3. 실제 값으로 수정
4. Git에 업로드하지 않도록 주의 (`.gitignore` 설정)

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

---

## 📊 설치 진행률

### 완료된 단계: 9/12 (75%) ✅

#### ✅ 완료
- [x] Python 3.13.7 설치
- [x] Node.js v22.18.0 설치  
- [x] Git 2.50.1 설치
- [x] Cursor IDE 1.5.5 설치
- [x] 프로젝트 폴더 생성 및 GitHub 연동
- [x] Python 가상환경 생성 및 활성화
- [x] Python 패키지 설치 (7개 주요 + 의존성)
- [x] Firecrawl 계정 생성 및 API 키 발급
- [x] 환경변수 파일(.env) 생성 및 테스트

#### ⏳ 진행 예정
- [ ] 회사 SMTP 정보 확인 및 설정
- [ ] 이메일 발송 테스트
- [ ] NTIS 크롤링 개발 시작

---

## 🚀 신규 설치 시 순서

1. **Python 3.8+ 설치** (PATH 추가)
2. **Node.js 18+ 설치**
3. **Git 설치**
4. **Cursor 또는 VS Code 설치**
5. **프로젝트 폴더 생성 및 이동**
6. **Python 가상환경 생성 및 활성화**
7. **Python 패키지 설치** (`pip install -r requirements.txt`)
8. **Firecrawl 계정 생성 및 API 키 발급**
9. **환경변수 파일(.env) 생성**
10. **API 연결 테스트** (`python test_firecrawl.py`)
11. **Git 저장소 초기화 및 GitHub 연동**
12. **회사 SMTP 정보 확인 및 설정** (선택)

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

---

## 🎯 현재 상태 요약

### ✅ **완료된 환경 설정**
- **개발 환경**: Python 3.13.7, Node.js v22.18.0, Git 2.50.1, Cursor IDE
- **Python 패키지**: 7개 주요 패키지 + 의존성 30+ 개 설치 완료
- **API 연동**: Firecrawl API 설정 및 테스트 성공
- **버전 관리**: GitHub 저장소 연동 완료

### 🚀 **다음 단계**
**Phase 2: 핵심 크롤링 기능 개발** 진행 준비 완료!

---

## 📚 관련 문서
- `development-roadmap.md` - 전체 개발 계획
- `project-overview.md` - 프로젝트 개요
- `test_firecrawl.py` - API 테스트 코드

**이 가이드를 따라하시면 개발 환경 구성이 완료됩니다!** 🎉

*마지막 업데이트: 2025년 9월 2일*

