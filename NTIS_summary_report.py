#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
NTIS 자동화 전체 실행 스크립트
1단계: 크롤링 → 2단계: HWP 처리 → 3단계: Excel 변환 → 4단계: 이메일 발송
"""

import subprocess
import sys
import os

# UTF-8 인코딩 설정
if sys.platform == 'win32':
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')

def run_script(script_name, description):
    """Python 스크립트 실행"""
    print(f"\n{'='*60}")
    print(f"🚀 {description}")
    print(f"{'='*60}")
    print(f"실행: {script_name}")
    print()
    
    try:
        # Python 스크립트 실행
        result = subprocess.run(
            [sys.executable, script_name],
            check=True,
            capture_output=False,
            text=True,
            encoding='utf-8'
        )
        
        print(f"\n✅ {description} 완료!")
        return True
        
    except subprocess.CalledProcessError as e:
        print(f"\n❌ {description} 실패!")
        print(f"오류 코드: {e.returncode}")
        return False
        
    except Exception as e:
        print(f"\n❌ {description} 중 오류 발생: {str(e)}")
        return False

def check_new_data():
    """new_data.json에 신규 데이터가 있는지 확인"""
    try:
        import json
        if not os.path.exists("output/new_data.json"):
            print("⚠️ new_data.json 파일이 없습니다.")
            return False
        
        with open("output/new_data.json", 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        if len(data) == 0:
            print("⚠️ 신규 공고가 없습니다.")
            return False
        
        print(f"✅ 신규 공고 {len(data)}건 발견!")
        return True
        
    except Exception as e:
        print(f"❌ new_data.json 확인 실패: {str(e)}")
        return False

def main():
    """메인 함수"""
    print("=" * 60)
    print("🤖 NTIS 자동화 전체 프로세스")
    print("=" * 60)
    print()
    print("실행 순서:")
    print("1️⃣ selenium_ntis.py - NTIS 크롤링")
    print("2️⃣ hwp_to_json.py - HWP 다운로드 & AI 요약")
    print("3️⃣ json_to_excel.py - Excel 리포트 생성")
    print("4️⃣ excel_to_email.py - 이메일 발송")
    print()
    print("🚀 자동 실행 시작...")
    print()
    
    # 1단계: NTIS 크롤링
    if not run_script("selenium_ntis.py", "1단계: NTIS 크롤링"):
        print("\n❌ 크롤링 단계에서 실패했습니다. 프로세스를 중단합니다.")
        return
    
    # new_data.json 확인
    print(f"\n{'='*60}")
    print("📊 신규 공고 확인")
    print(f"{'='*60}")
    
    if not check_new_data():
        print("\n⚠️ 신규 공고가 없어 프로세스를 종료합니다.")
        print("(이메일이 발송되지 않습니다.)")
        return
    
    # 2단계: HWP 처리 및 AI 요약
    if not run_script("hwp_to_json.py", "2단계: HWP 처리 & AI 요약"):
        print("\n❌ HWP 처리 단계에서 실패했습니다. 프로세스를 중단합니다.")
        return
    
    # 3단계: Excel 변환
    if not run_script("json_to_excel.py", "3단계: Excel 리포트 생성"):
        print("\n❌ Excel 변환 단계에서 실패했습니다. 프로세스를 중단합니다.")
        return
    
    # 4단계: 이메일 발송
    if not run_script("excel_to_email.py", "4단계: 이메일 발송"):
        print("\n❌ 이메일 발송 단계에서 실패했습니다.")
        return
    
    # 완료
    print(f"\n{'='*60}")
    print("🎉 전체 프로세스 완료!")
    print(f"{'='*60}")
    print()
    print("✅ 1단계: NTIS 크롤링 완료")
    print("✅ 2단계: HWP 처리 & AI 요약 완료")
    print("✅ 3단계: Excel 리포트 생성 완료")
    print("✅ 4단계: 이메일 발송 완료")
    print()
    print("📧 이메일함을 확인하세요!")

if __name__ == "__main__":
    main()

