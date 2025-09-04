# Git 사용설명서 📚

## 📋 목차
1. [Git 기본 개념](#git-기본-개념)
2. [초기 설정](#초기-설정)
3. [기본 명령어](#기본-명령어)
4. [브랜치와 업스트림](#브랜치와-업스트림)
5. [회사 ↔ 집 작업 흐름](#회사--집-작업-흐름)
6. [문제 해결](#문제-해결)

---

## Git 기본 개념

### 🎯 Git이란?
- **버전 관리 시스템**: 파일 변경 이력을 추적하고 관리
- **협업 도구**: 여러 사람이 동시에 작업할 수 있게 도움
- **백업 시스템**: 코드 분실 방지

### 📦 주요 구성 요소

#### Repository (저장소)
- **전체 프로젝트를 담는 큰 컨테이너**
- 로컬 저장소: 내 컴퓨터에 있는 프로젝트
- 원격 저장소: GitHub 등 서버에 있는 프로젝트

#### Branch (브랜치)
- **독립적인 작업 공간** (나무의 가지처럼)
- 기능별로 다른 브랜치에서 작업
- `main`: 메인 브랜치 (완성된 코드)
- `feature-xxx`: 새 기능 개발용
- `bugfix-xxx`: 버그 수정용

#### Upstream (업스트림)
- **로컬 브랜치와 연결된 원격 브랜치**
- 로컬 `main` ↔ 원격 `origin/main` 연결
- `git push -u origin main`으로 설정

---

## 초기 설정

### 🔧 Git 사용자 정보 설정 (최초 한 번)
```powershell
# 전역 사용자 정보 설정
git config --global user.name "당신의GitHub사용자명"
git config --global user.email "당신의이메일@gmail.com"
```

### 📁 새 프로젝트 시작
```powershell
# 1. 로컬 Git 저장소 초기화
git init

# 2. GitHub 저장소 연결
git remote add origin https://github.com/사용자명/저장소명.git

# 3. 첫 번째 업로드
git add .
git commit -m "초기 프로젝트 설정"
git push -u origin main
```

---

## 기본 명령어

### 📷 git add - 파일 선택하기
```powershell
git add .                    # 모든 변경된 파일 선택
git add test.py             # 특정 파일만 선택
git add docs/               # 특정 폴더만 선택
```
**비유**: 인스타그램에 올릴 사진들을 선택하는 것

### 📦 git commit - 버전 저장하기
```powershell
git commit -m "작업 내용 설명"
```
**비유**: 선택한 사진들을 하나의 앨범으로 만들고 제목 붙이기
**좋은 메시지 예시**:
- `"Firecrawl API 설정 완료"`
- `"NTIS 크롤링 기능 구현"`
- `"이메일 발송 오류 수정"`

### 🚀 git push - 서버에 업로드
```powershell
git push                    # 기본 업로드
git push -u origin main     # 최초 업로드 (업스트림 설정)
```
**비유**: 앨범을 구글 포토에 업로드

### 📥 git pull - 서버에서 다운로드
```powershell
git pull
```
**비유**: 다른 기기에서 구글 포토의 최신 앨범들 다운로드

### 📋 상태 확인 명령어
```powershell
git status              # 현재 상태 확인
git log --oneline       # 커밋 히스토리 보기
git branch              # 브랜치 목록 보기
git remote -v           # 원격 저장소 확인
```

---

## 브랜치와 업스트림

### 🌳 브랜치 관리
```powershell
# 브랜치 생성 및 이동
git branch feature-crawling         # 새 브랜치 생성
git checkout feature-crawling       # 브랜치로 이동
git checkout -b feature-login       # 생성과 이동을 한 번에

# 브랜치 이름 변경
git branch -M main                  # 현재 브랜치를 main으로 변경

# 브랜치 병합
git checkout main                   # main 브랜치로 이동
git merge feature-crawling          # feature-crawling을 main에 병합
```

### 🔗 업스트림 설정
```powershell
# 브랜치별 업스트림 설정
git push -u origin main             # main 브랜치 연결
git push -u origin feature          # feature 브랜치 연결

# 설정 확인
git branch -vv                      # 각 브랜치의 업스트림 확인
```

---

## 회사 ↔ 집 작업 흐름

### 🏢 회사에서 (프로젝트 시작)
```powershell
# 1. 작업 완료 후
git add .
git commit -m "오늘 한 작업 내용"
git push
```

### 🏠 집에서 (처음 작업할 때)
```powershell
# 1. 전체 프로젝트 다운로드
cd Desktop
git clone https://github.com/사용자명/저장소명.git
cd 저장소명

# 2. 작업 후 업로드
git add .
git commit -m "집에서 한 작업"
git push
```

### 🔄 이후 작업 흐름

#### 작업 시작 전 (항상!)
```powershell
git pull                # 다른 곳에서 한 작업 가져오기
```

#### 작업 완료 후
```powershell
git add .
git commit -m "작업 내용"
git push                # 서버에 업로드
```

### 📅 일주일 작업 예시
```
월요일 회사: git pull → 작업 → git push
월요일 집:   git pull → 작업 → git push
화요일 회사: git pull → 작업 → git push
화요일 집:   git pull → 작업 → git push
...
```

---

## 문제 해결

### ❌ "fatal: The current branch master has no upstream branch"
**원인**: 업스트림이 설정되지 않음
**해결**:
```powershell
git branch -M main              # 브랜치를 main으로 변경
git push -u origin main         # 업스트림 설정하며 push
```

### ❌ GitHub에서 파일이 안 보임
**확인사항**:
1. GitHub에 로그인했는지 확인
2. 올바른 저장소 URL인지 확인
3. `main` 브랜치가 선택되어 있는지 확인
4. `git remote -v`로 연결 상태 확인

### ❌ "Authentication failed"
**해결**:
1. GitHub에서 브라우저 인증 완료
2. Personal Access Token 사용 (필요시)
3. `git config --list`로 사용자 정보 확인

### ❌ 이전 커밋 취소하고 싶을 때
```powershell
# 커밋은 취소하고 파일은 유지 (추천)
git reset --soft HEAD~1

# 커밋과 변경사항 모두 취소 (주의!)
git reset --hard HEAD~1
```

### ❌ .gitignore 파일 관련
**개인 작업시**: `.gitignore` 삭제해서 모든 파일 동기화
**팀 작업시**: `.gitignore` 사용해서 민감한 파일 보호

---

## 💡 실용적인 팁

### 🎯 좋은 커밋 메시지 작성법
```powershell
# 좋은 예시 ✅
git commit -m "Firecrawl API 연결 기능 추가"
git commit -m "엑셀 파일 생성 오류 수정"
git commit -m "UI 디자인 개선"

# 나쁜 예시 ❌
git commit -m "수정"
git commit -m "작업함"
git commit -m "test"
```

### 📋 자주 사용하는 명령어 조합
```powershell
# 일반적인 작업 흐름
git pull                        # 시작 전 최신 상태로 업데이트
# 작업...
git add .
git commit -m "작업 내용"
git push                        # 완료 후 업로드

# 현재 상태 한 눈에 보기
git status && git log --oneline -5
```

### 🔍 Git 히스토리 예쁘게 보기
```powershell
git log --oneline --graph --decorate --all
```

---

## 📚 참고 자료

### 🌐 유용한 링크
- [GitHub 공식 가이드](https://docs.github.com/)
- [Git 공식 문서](https://git-scm.com/doc)

### 📖 추가 학습 주제
- Git Flow (브랜치 전략)
- Pull Request (코드 리뷰)
- Git Hooks (자동화)
- Merge vs Rebase

---

## 🎯 요약

### Git의 핵심 3단계
1. **add**: 변경사항 선택
2. **commit**: 버전 저장 
3. **push**: 서버 업로드

### 회사 ↔ 집 작업의 핵심
1. **시작 전**: `git pull` (최신 상태로)
2. **완료 후**: `add → commit → push` (업로드)

### 기억할 점
- 커밋 메시지는 명확하게
- 작업 시작 전에는 항상 `git pull`
- 문제 발생시 `git status`로 상태 확인

---

*이 문서는 실제 프로젝트 경험을 바탕으로 작성되었습니다. 궁금한 점이 있으면 언제든 문의하세요! 😊*
