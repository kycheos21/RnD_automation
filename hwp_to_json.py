#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
전체 프로세스 테스트: 단일 공고 처리
URL → 다운로드 → 파싱 → 텍스트 추출
"""

import os
import sys
import time
import glob
import subprocess
import shutil
import uuid
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup

# UTF-8 인코딩 설정
if sys.platform == 'win32':
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')

def setup_chrome_driver(download_path):
    """Chrome 드라이버 설정"""
    try:
        print("Chrome 브라우저 설정 중...")
        
        chrome_options = Options()
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        chrome_options.add_argument("--window-size=1920,1080")
        
        abs_download_path = os.path.abspath(download_path)
        os.makedirs(abs_download_path, exist_ok=True)
        
        print(f"   다운로드 경로: {abs_download_path}")
        
        prefs = {
            "download.default_directory": abs_download_path,
            "download.prompt_for_download": False,
            "download.directory_upgrade": True,
            "safebrowsing.enabled": True,
            "safebrowsing.disable_download_protection": True,
            "plugins.always_open_pdf_externally": True,
            "profile.default_content_settings.popups": 0,
            "profile.default_content_setting_values.automatic_downloads": 1
        }
        chrome_options.add_experimental_option("prefs", prefs)
        chrome_options.add_experimental_option("excludeSwitches", ["enable-logging"])
        
        service = Service(ChromeDriverManager().install())
        driver = webdriver.Chrome(service=service, options=chrome_options)
        
        print(f"   Chrome 준비 완료")
        return driver
        
    except Exception as e:
        print(f"브라우저 설정 실패: {str(e)}")
        return None

def download_announcement_file(driver, url, download_path):
    """공고 파일 다운로드 및 검증
    
    Returns:
        dict 또는 None
        성공: {"status": "success", "file_path": "경로"}
        실패: {"status": "no_attachment", "message": "첨부파일이 없습니다"}
              {"status": "image_file", "message": "공고문이 이미지 파일입니다", "filename": "파일명"}
              {"status": "error", "message": "오류 메시지"}
    """
    try:
        print(f"\n상세 페이지 접속: {url}")
        driver.get(url)
        time.sleep(10)
        
        print("첨부파일 찾기...")
        wait = WebDriverWait(driver, 10)
        file_div = wait.until(
            EC.presence_of_element_located((By.XPATH, "//div[contains(@class, 'file')]"))
        )
        
        file_links = file_div.find_elements(By.TAG_NAME, "a")
        print(f"   첨부파일 링크: {len(file_links)}개")
        
        # 첨부파일이 없는 경우
        if len(file_links) == 0:
            print("   ⚠️ 첨부파일이 없습니다.")
            return {"status": "no_attachment", "message": "첨부파일이 없습니다"}
        
        # "공고" 또는 "공고문" 키워드 찾기
        announcement_files = []
        image_files = []
        
        for i, link in enumerate(file_links):
            try:
                text = link.text.strip()
                if text:
                    # 이미지 파일 체크
                    if any(ext in text.lower() for ext in ['.png', '.jpg', '.jpeg', '.gif', '.bmp']):
                        image_files.append(text)
                        print(f"   [{i}] 이미지 파일 발견: {text}")
                    # 공고문 체크
                    elif any(keyword in text for keyword in ["공고", "공고문"]):
                        announcement_files.append({
                            "text": text,
                            "element": link
                        })
                        print(f"   [{i}] 발견: {text}")
            except:
                continue
        
        # 공고문 파일이 없고 이미지 파일만 있는 경우
        if not announcement_files and image_files:
            print(f"   ⚠️ 공고문이 이미지 파일입니다: {image_files[0]}")
            return {
                "status": "image_file", 
                "message": "공고문이 이미지 파일입니다",
                "filename": image_files[0]
            }
        
        # 공고문 파일도 없고 이미지도 아닌 경우
        if not announcement_files:
            print("   ⚠️ 공고 파일을 찾을 수 없습니다.")
            return {"status": "no_announcement", "message": "공고 파일을 찾을 수 없습니다"}
        
        # 모든 공고 파일 다운로드 시도 (최대 3개)
        max_downloads = min(3, len(announcement_files))
        downloaded_files = []
        
        for i in range(max_downloads):
            file_info = announcement_files[i]
            print(f"\n다운로드 시작 ({i+1}/{max_downloads}): {file_info['text']}")
            
            before_files = set(glob.glob(os.path.join(download_path, "*")))
            file_info['element'].click()
            print("   링크 클릭 완료")
            
            # 다운로드 대기
            print("   다운로드 대기 중...")
            downloaded_file = None
            for j in range(30):
                time.sleep(1)
                after_files = set(glob.glob(os.path.join(download_path, "*")))
                new_files = after_files - before_files
                downloading = any(".crdownload" in f for f in new_files)
                
                if new_files and not downloading:
                    downloaded_file = list(new_files)[0]
                    print(f"   다운로드 완료! ({j+1}초)")
                    break
            
            if downloaded_file:
                print(f"   파일: {os.path.basename(downloaded_file)}")
                downloaded_files.append(downloaded_file)
                # 다음 파일 다운로드를 위해 잠시 대기
                time.sleep(2)
            else:
                print("   다운로드 시간 초과")
        
        if not downloaded_files:
            print("   모든 다운로드 실패")
            return {"status": "download_failed", "message": "모든 다운로드 실패"}
        
        # 파일 검증 (HWP, PDF 등 통합)
        print(f"\n🔍 파일 검증 중... ({len(downloaded_files)}개 파일)")
        from src.utils.file_validator import FileValidator
        
        validator = FileValidator()
        valid_file = validator.select_valid_file(download_path, ["공고", "공고문"])
        
        if valid_file:
            file_type = valid_file.get('file_type', 'unknown')
            print(f"✅ 유효한 {file_type.upper()} 파일 선택: {valid_file['filename']}")
            
            # 검증 후 파일명을 짧게 변경 (hwp5html 호환성)
            original_path = valid_file['file_path']
            file_ext = os.path.splitext(original_path)[1]
            short_name = f"validated_{uuid.uuid4().hex[:8]}{file_ext}"
            short_path = os.path.join(download_path, short_name)
            
            try:
                shutil.move(original_path, short_path)
                print(f"   파일명 변경: {short_name}")
                return {"status": "success", "file_path": short_path}
            except Exception as e:
                print(f"   ⚠️ 파일명 변경 실패: {e}, 원본 사용")
                return {"status": "success", "file_path": original_path}
        else:
            print("❌ 유효한 파일을 찾을 수 없습니다.")
            # 다운로드된 파일 중 첫 번째 반환 (백업)
            return {"status": "success", "file_path": downloaded_files[0]}
        
    except Exception as e:
        print(f"다운로드 실패: {str(e)}")
        return {"status": "error", "message": str(e)}

def parse_hwp_to_text(hwp_file_path):
    """HWP 파일을 HTML로 변환 후 텍스트 추출"""
    try:
        print(f"\nHWP 파일 파싱 시작...")
        print(f"파일: {os.path.basename(hwp_file_path)}")
        
        # 절대 경로로 변환
        abs_hwp_path = os.path.abspath(hwp_file_path)
        print(f"절대경로!!!!!!!!!!: {abs_hwp_path}")
        
        temp_dir = os.path.join(os.path.dirname(abs_hwp_path), "temp_parse")
        os.makedirs(temp_dir, exist_ok=True)
        
        temp_hwp = os.path.join(temp_dir, f"temp_{uuid.uuid4().hex[:8]}.hwp")
        temp_html_dir = os.path.join(temp_dir, f"temp_{uuid.uuid4().hex[:8]}_html")
        
        try:
            print(f"   복사 시작: {abs_hwp_path} → {temp_hwp}")
            shutil.copy2(abs_hwp_path, temp_hwp)
            print(f"   복사 완료! 임시파일 존재: {os.path.exists(temp_hwp)}")
            
            print(f"   HTML 변환 중...")
            print(f"   출력 폴더: {temp_html_dir}")
            
            try:
                # hwp5html 전체 경로 사용
                hwp5html_path = os.path.join(os.path.dirname(sys.executable), "hwp5html.exe")
                print(f"   hwp5html 경로: {hwp5html_path}")
                
                result = subprocess.run(
                    [hwp5html_path, "--output", temp_html_dir, temp_hwp],
                    capture_output=True,
                    text=True,
                    timeout=60,
                    encoding='utf-8',
                    errors='ignore'
                )
                print(f"   html변환성공확인 코드 0이면 성공: {result.returncode}")
            except Exception as subprocess_error:
                print(f"   ❌ subprocess 실행 오류: {subprocess_error}")
                raise subprocess_error
            
            if result.returncode != 0:
                return {"success": False, "error": f"HTML 변환 실패: {result.stderr}"}
            
            
            html_file = os.path.join(temp_html_dir, "index.xhtml")
            if not os.path.exists(html_file):
                return {"success": False, "error": "HTML 파일 없음"}
            
            print(f"   텍스트 추출 중...")
            with open(html_file, 'r', encoding='utf-8') as f:
                html_content = f.read()
            
            soup = BeautifulSoup(html_content, 'html.parser')
            text = soup.get_text(separator='\n', strip=True)
            lines = [line.strip() for line in text.split('\n') if line.strip()]
            cleaned_text = '\n'.join(lines)
            
            # 앞부분 3000자만 추출
            front_text = cleaned_text[:3000]
            last_period = max(
                front_text.rfind('.\n'),
                front_text.rfind('\n\n')
            )
            if last_period > 2400:
                front_text = front_text[:last_period + 1]
            
            print(f"   추출 성공! (전체: {len(cleaned_text)}자, 앞부분: {len(front_text)}자)")
            
            return {
                "success": True,
                "full_text": cleaned_text,
                "front_text": front_text
            }
            
        finally:
            try:
                if os.path.exists(temp_hwp):
                    os.remove(temp_hwp)
                if os.path.exists(temp_html_dir):
                    shutil.rmtree(temp_html_dir)
                if os.path.exists(temp_dir) and not os.listdir(temp_dir):
                    os.rmdir(temp_dir)
            except:
                pass
        
    except Exception as e:
        print(f"파싱 실패: {str(e)}")
        return {"success": False, "error": str(e)}

def main():
    """메인 함수"""
    import json
    import sys
    from dotenv import load_dotenv
    
    # .env 파일 로드
    load_dotenv()
    
    # 프로젝트 경로 추가
    sys.path.append(os.path.dirname(os.path.abspath(__file__)))
    
    # PDF 파서 초기화
    try:
        from src.data_processor.pdf_parser import PDFParser
        pdf_parser = PDFParser()
        print("✅ PDF 파서 초기화 완료")
    except Exception as e:
        print(f"⚠️ PDF 파서 초기화 실패: {e}")
        pdf_parser = None
    
    # HWPX 파서 초기화
    try:
        from src.data_processor.hwpx_parser import HWPXParser
        hwpx_parser = HWPXParser()
        print("✅ HWPX 파서 초기화 완료")
    except Exception as e:
        print(f"⚠️ HWPX 파서 초기화 실패: {e}")
        hwpx_parser = None
    
    print("전체 프로세스: new_data.json 기반 모든 공고 처리")
    print("=" * 60)
    
    # Claude Summarizer 초기화
    try:
        from src.data_processor.claude_summarizer import ClaudeSummarizer
        summarizer = ClaudeSummarizer()
        print("✅ Claude API 요약기 초기화 완료")
    except Exception as e:
        print(f"⚠️ Claude API 요약기 초기화 실패: {e}")
        summarizer = None
    
    # new_data.json 로드
    new_data_file = "output/new_data.json"
    if not os.path.exists(new_data_file):
        print(f"❌ {new_data_file} 파일이 없습니다.")
        return
    
    with open(new_data_file, 'r', encoding='utf-8') as f:
        new_data = json.load(f)
    
    print(f"📂 {len(new_data)}개 공고 로드 완료")
    
    download_path = "output/downloaded_files"
    
    driver = setup_chrome_driver(download_path)
    if not driver:
        return
    
    try:
        # ====== 1단계: 모든 공고 다운로드 ======
        print(f"\n{'='*60}")
        print("📥 1단계: 모든 공고 파일 다운로드")
        print(f"{'='*60}")
        
        download_map = []  # {announcement, file_path, error} 리스트
        
        for i, announcement in enumerate(new_data, 1):
            print(f"\n[{i}/{len(new_data)}] {announcement.get('공고명', '제목 없음')[:60]}...")
            
            url = announcement.get("상세_URL", "")
            if not url:
                print("   ⚠️ URL 없음")
                download_map.append({
                    "announcement": announcement,
                    "file_path": None,
                    "error": "URL 없음"
                })
                continue
            
            download_result = download_announcement_file(driver, url, download_path)
            
            # 다운로드 결과 확인
            if not download_result or download_result.get("status") != "success":
                error_msg = download_result.get("message", "다운로드 실패") if download_result else "다운로드 실패"
                print(f"   ❌ {error_msg}")
                
                # 예외 상황을 JSON에 기록
                if download_result and download_result.get("status") in ["no_attachment", "image_file", "no_announcement"]:
                    announcement["처리상태"] = error_msg
                    if download_result.get("status") == "image_file":
                        announcement["첨부파일명"] = download_result.get("filename", "")
                
                download_map.append({
                    "announcement": announcement,
                    "file_path": None,
                    "error": error_msg
                })
            else:
                downloaded_file = download_result.get("file_path")
                print(f"   ✅ 다운로드 성공")
                download_map.append({
                    "announcement": announcement,
                    "file_path": downloaded_file,
                    "error": None
                })
            
            time.sleep(2)  # 다음 다운로드까지 대기
        
        # 브라우저 종료 (다운로드 완료)
        driver.quit()
        print(f"\n✅ 모든 다운로드 완료! ({len([d for d in download_map if d['file_path']])}개 성공)")
        
        # ====== 2단계: 파일 파싱 및 AI 요약 ======
        print(f"\n{'='*60}")
        print("🔍 2단계: 파일 파싱 및 AI 요약")
        print(f"{'='*60}")
        
        results = []
        success_count = 0
        
        for i, item in enumerate(download_map, 1):
            announcement = item["announcement"]
            downloaded_file = item["file_path"]
            title = announcement.get("공고명", "제목 없음")
            
            print(f"\n[{i}/{len(download_map)}] {title[:60]}...")
            
            # 다운로드 실패한 경우 스킵
            if not downloaded_file:
                print(f"   ⚠️ 다운로드 실패: {item.get('error', '알 수 없음')}")
                results.append({
                    "공고명": title,
                    "success": False,
                    "error": item.get('error', '다운로드 실패')
                })
                continue
            
            try:
                
                # 2단계: 파일 파싱 (HWP/PDF/HWPX 구분)
                print(f"\n2️⃣ 파일 파싱...")
                print(f"   파싱할 파일 경로: {downloaded_file}")
                print(f"   파일 존재 여부: {os.path.exists(downloaded_file)}")
                
                # 파일 확장자 확인
                file_ext = os.path.splitext(downloaded_file)[1].lower()
                
                if file_ext == '.pdf':
                    # PDF 파일 처리
                    if pdf_parser:
                        parse_result = pdf_parser.extract_text_from_pdf(downloaded_file)
                    else:
                        parse_result = {"success": False, "error": "PDF 파서가 초기화되지 않음"}
                elif file_ext == '.hwpx':
                    # HWPX 파일 처리
                    if hwpx_parser:
                        parse_result = hwpx_parser.extract_text_from_hwpx(downloaded_file)
                    else:
                        parse_result = {"success": False, "error": "HWPX 파서가 초기화되지 않음"}
                else:
                    # HWP 파일 처리 (기본)
                    parse_result = parse_hwp_to_text(downloaded_file)
                
                if not parse_result["success"]:
                    print(f"❌ 파싱 실패: {parse_result['error']}")
                    results.append({
                        "공고명": title,
                        "success": False,
                        "error": f"파싱 실패: {parse_result['error']}"
                    })
                    continue
                
                # 3단계: 결과 저장
                print(f"✅ 처리 성공!")
                
                # 파일 형식에 따른 텍스트 추출
                if file_ext == '.pdf':
                    full_text = parse_result.get('full_text', '')
                    front_text = parse_result.get('business_overview', '') or full_text[:3000]
                    print(f"   전체 텍스트: {len(full_text)}자")
                    print(f"   사업개요: {len(front_text)}자")
                elif file_ext == '.hwpx':
                    full_text = parse_result.get('full_text', '')
                    front_text = parse_result.get('business_overview', '') or full_text[:3000]
                    print(f"   전체 텍스트: {len(full_text)}자")
                    print(f"   앞부분 텍스트: {len(front_text)}자")
                else:
                    full_text = parse_result.get('full_text', '')
                    front_text = parse_result.get('front_text', '')
                    print(f"   전체 텍스트: {len(full_text)}자")
                    print(f"   앞부분 텍스트: {len(front_text)}자")
                
                # 텍스트 파일 저장
                base_name = os.path.splitext(downloaded_file)[0]
                output_file = f"{base_name}_parsed.txt"
                with open(output_file, 'w', encoding='utf-8') as f:
                    f.write(front_text)
                print(f"   저장: {os.path.basename(output_file)}")
                
                # 4단계: Claude API 요약
                ai_summary = None
                if summarizer and front_text:
                    print(f"\n3️⃣ Claude API 요약...")
                    try:
                        summary_result = summarizer.summarize_business_overview(
                            business_overview=front_text,
                            announcement_title=title
                        )
                        
                        if summary_result.get("success"):
                            print(f"   ✅ AI 요약 완료!")
                            ai_summary = summary_result.get("summary", {})
                            
                            # new_data의 해당 항목에 요약 추가
                            announcement["ai_요약"] = ai_summary
                            announcement["요약_처리시간"] = time.strftime("%Y-%m-%dT%H:%M:%S")
                            if summary_result.get("metadata"):
                                announcement["ai_메타데이터"] = summary_result["metadata"]
                        else:
                            print(f"   ⚠️ AI 요약 실패: {summary_result.get('error', '알 수 없는 오류')}")
                    except Exception as e:
                        print(f"   ⚠️ AI 요약 중 오류: {str(e)}")
                
                results.append({
                    "공고명": title,
                    "success": True,
                    "hwp_file": downloaded_file,
                    "parsed_file": output_file,
                    "text_length": len(parse_result['full_text']),
                    "ai_summary": ai_summary
                })
                
                success_count += 1
                
            except Exception as e:
                print(f"❌ 오류 발생: {str(e)}")
                results.append({
                    "공고명": title,
                    "success": False,
                    "error": str(e)
                })
            
            # 다음 공고 처리 전 잠시 대기
            if i < len(new_data):
                print(f"\n⏳ 다음 공고까지 3초 대기...")
                time.sleep(3)
        
        # 처리 결과 요약
        print(f"\n{'='*60}")
        print("🎯 처리 결과 요약")
        print(f"{'='*60}")
        print(f"총 처리 대상: {len(new_data)}개")
        print(f"성공: {success_count}개")
        print(f"실패: {len(new_data) - success_count}개")
        print(f"성공률: {success_count/len(new_data)*100:.1f}%")
        
        # new_data.json 저장 (AI 요약 추가됨)
        if success_count > 0 or len(new_data) > 0:
            print(f"\n💾 new_data.json 업데이트 중...")
            
            # AI 요약이 추가된 new_data.json 저장
            with open(new_data_file, 'w', encoding='utf-8') as f:
                json.dump(new_data, f, ensure_ascii=False, indent=2)
            print(f"   ✅ new_data.json 업데이트 완료! ({len(new_data)}개)")
        
        # 임시 파일 정리
        print(f"\n🧹 임시 파일 정리 중...")
        try:
            # downloaded_files 폴더의 모든 파일 삭제
            downloaded_files_dir = os.path.join("output", "downloaded_files")
            if os.path.exists(downloaded_files_dir):
                deleted_count = 0
                for file in os.listdir(downloaded_files_dir):
                    file_path = os.path.join(downloaded_files_dir, file)
                    if os.path.isfile(file_path):
                        os.remove(file_path)
                        deleted_count += 1
                print(f"   ✅ {deleted_count}개 임시 파일 삭제 완료")
            else:
                print(f"   ⚠️ {downloaded_files_dir} 폴더가 없습니다")
        except Exception as e:
            print(f"   ⚠️ 임시 파일 정리 실패: {str(e)}")
        
    except Exception as e:
        print(f"❌ 오류 발생: {str(e)}")
        import traceback
        traceback.print_exc()
    
    finally:
        # 브라우저 자동 종료 (자동화 프로세스용)
        # print("\n브라우저를 열어둡니다. 확인 후 Enter를 누르세요...")
        # input("Press Enter to close...")
        print("\n브라우저 종료 중...")
        driver.quit()
        print("   ✅ 브라우저 종료 완료")

if __name__ == "__main__":
    main()

