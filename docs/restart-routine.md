# NTIS 크롤링 자동화 프로젝트 재시작 루틴

## 📅 작성일
**2025년 9월 2일**

## 🔄 컴퓨터 재시작 후 해야 할 작업

### 1단계: Cursor IDE 실행 및 프로젝트 열기
```
1. Cursor 실행
2. File > Open Folder
3. C:\Users\kyche\Desktop\kycheos_workspace\01RND_auto 선택
4. 프로젝트 폴더 열기 완료
```

### 2단계: PowerShell 터미널 열기
```
1. Cursor에서 Ctrl + ` (백틱) 또는 Terminal > New Terminal
2. PowerShell이 기본으로 열리는지 확인
3. 현재 위치가 프로젝트 폴더인지 확인
```

### 3단계: 프로젝트 폴더 위치 확인
```powershell
# 현재 위치 확인
pwd

# 결과 예상값:
# Path
# ----
# C:\Users\kyche\Desktop\kycheos_workspace\01RND_auto
```

### 4단계: Python 가상환경 활성화
```powershell
# 가상환경 활성화
venv\Scripts\activate
```

### 5단계: 가상환경 활성화 확인
```powershell
# 프롬프트 변경 확인 - (venv)가 앞에 붙어야 함
(venv) PS C:\Users\kyche\Desktop\kycheos_workspace\01RND_auto>

# Python 경로 확인 (선택사항)
Get-Command python
```

### 6단계: 설치된 패키지 확인 (선택사항)
```powershell
# 설치된 패키지 목록 확인
python -m pip list

# 주요 패키지 확인 (pandas, openpyxl, schedule, requests, beautifulsoup4, firecrawl-py, python-dotenv)
```

## ✅ 체크리스트

- [ ] **Cursor 실행** 및 프로젝트 폴더 열기
- [ ] **PowerShell 터미널** 열기
- [ ] **현재 위치** 확인 (`pwd`)
- [ ] **가상환경 활성화** (`venv\Scripts\activate`)
- [ ] **프롬프트 (venv) 표시** 확인
- [ ] **패키지 설치 상태** 확인 (선택사항)

## 🚨 문제 해결

### 문제 1: 가상환경 활성화 안됨
```powershell
# 해결책 1: 직접 경로로 실행
C:\Users\kyche\Desktop\kycheos_workspace\01RND_auto\venv\Scripts\activate

# 해결책 2: PowerShell 실행 정책 확인
Get-ExecutionPolicy
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

### 문제 2: Python 인식 안됨
```powershell
# py 명령어 사용
py --version

# 또는 직접 경로
venv\Scripts\python.exe --version
```

### 문제 3: pip 명령어 안됨
```powershell
# python -m pip 사용
python -m pip list

# 또는 직접 경로
venv\Scripts\pip.exe list
```

## 📂 중요 파일 위치

### 프로젝트 문서들
- `docs/project-overview.md` - 프로젝트 전체 개요
- `docs/setup-requirements.md` - 설치 요구사항
- `docs/installation-status.md` - 현재 설치 상황
- `docs/restart-routine.md` - 현재 파일

### 가상환경 관련
- `venv/` - 가상환경 폴더
- `venv/Scripts/activate.bat` - 활성화 스크립트
- `venv/Scripts/python.exe` - Python 실행파일
- `venv/Scripts/pip.exe` - pip 패키지 매니저

## 🔧 자동화 스크립트 (선택사항)

### start_project.bat 파일 생성
프로젝트 루트에 다음 내용으로 `start_project.bat` 파일을 생성하면 더블클릭으로 자동 실행 가능:

```batch
@echo off
echo NTIS 크롤링 프로젝트 시작...
cd /d "C:\Users\kyche\Desktop\kycheos_workspace\01RND_auto"
echo 프로젝트 폴더로 이동 완료
call venv\Scripts\activate
echo 가상환경 활성화 완료
echo 패키지 목록:
python -m pip list
echo.
echo 준비 완료! 개발을 시작하세요.
powershell
```

## 💡 팁

### 1. **즐겨찾기 설정**
- Cursor에서 이 프로젝트를 Recent Projects에 고정
- Windows 탐색기에서 프로젝트 폴더를 즐겨찾기 추가

### 2. **단축키 활용**
- `Ctrl + `` : 터미널 토글
- `Ctrl + Shift + `` : 새 터미널
- `Ctrl + P` : 파일 빠른 열기

### 3. **상태 확인 습관**
- 항상 `(venv)` 프롬프트가 있는지 확인
- 의심스러우면 `python -m pip list`로 패키지 확인

## 🚀 다음 단계

재시작 루틴 완료 후:
1. **현재 문서들 검토** (docs 폴더의 .md 파일들)
2. **이전 진행상황 파악** (installation-status.md 참조)
3. **다음 작업 계획** (Firecrawl API 설정 등)

---

**이 파일을 북마크해두고 컴퓨터 재시작 시마다 참고하세요!** 📚

