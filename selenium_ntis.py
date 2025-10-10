import os
import sys
import time
import json
import re
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from webdriver_manager.chrome import ChromeDriverManager

# UTF-8 인코딩 설정
if sys.platform == 'win32':
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')

# 프로젝트 src 경로 추가
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

# 설정 파일 import
try:
    from utils.config_reader import get_search_keywords, get_ui_selector, get_page_unit_target_value
except ImportError as e:
    print(f"⚠️ 모듈 import 실패: {e}")
    print("   기본 설정으로 진행합니다.")

def extract_uid_from_url(url):
    """상세_URL에서 roRndUid 추출"""
    try:
        match = re.search(r'roRndUid=(\d+)', url)
        return match.group(1) if match else ""
    except Exception:
        return ""

def crawl_announcement_list(driver, target_count=30):
    """
    NTIS 검색 결과에서 공고 리스트를 크롤링합니다.
    
    중요사항:
    - 접수일을 기준으로 내림차순 정렬하여 최신 공고가 위로 오도록 함
    - roRndUid를 고유 식별자로 사용하여 중복 판별
    """
    print(f"\n📋 공고 리스트 크롤링 시작 (목표: {target_count}개)")
    print("=" * 50)
    
    try:
        # 1. 검색 결과 테이블이 로드될 때까지 명시적으로 대기
        print("1️⃣ 검색 결과 테이블 로딩 대기...")
        table = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "table.basic_list"))
        )
        print("   ✅ basic_list 테이블 발견")

        # 2. 테이블의 모든 행(rows)을 우선 수집
        rows = table.find_elements(By.CSS_SELECTOR, "tbody tr")
        print(f"   📊 발견된 공고 항목: {len(rows)}개")
        if not rows:
            print("   ⚠️ 검색 결과가 없습니다.")
            return []

        # 3. 모든 행의 데이터를 파싱하여 리스트에 저장
        print("\n2️⃣ 모든 공고 정보 임시 추출 중...")
        all_rows_data = []
        for i, row in enumerate(rows):
            try:
                cells = row.find_elements(By.TAG_NAME, "td")
                if len(cells) < 8:
                    continue
                
                item_data = {
                    "현황": cells[2].find_element(By.TAG_NAME, "span").text.strip(),
                    "공고명": cells[3].find_element(By.TAG_NAME, "a").text.strip(),
                    "상세_URL": cells[3].find_element(By.TAG_NAME, "a").get_attribute('href'),
                    "부처명": cells[4].text.strip(),
                    "접수일": cells[5].text.strip(),
                    "마감일": cells[6].text.strip(),
                }
                all_rows_data.append(item_data)
            except Exception as e:
                print(f"   ❌ {i+1}번째 행 추출 중 오류 발생: {str(e)}")
                continue
        
        # 4. '접수일'을 기준으로 데이터를 내림차순 정렬 (최신 공고가 위로 오도록)
        print("\n3️⃣ 접수일 기준으로 데이터 정렬 중...")
        
        def parse_date_for_sort(date_str):
            """정렬을 위한 날짜 파싱 (YYYY.MM.DD 형식)"""
            try:
                return datetime.strptime(date_str, "%Y.%m.%d")
            except:
                return datetime.min  # 파싱 실패시 가장 오래된 날짜로 처리
        
        sorted_data = sorted(all_rows_data, key=lambda x: parse_date_for_sort(x['접수일']), reverse=True)
        print("   ✅ 접수일 기준 내림차순 정렬 완료!")
        
        # 5. 목표 개수만큼 최종 데이터 선택
        final_data = sorted_data[:target_count]

        print(f"\n4️⃣ 크롤링 완료! (성공: {len(final_data)}개)")
        
        # 결과 요약 출력 (접수일 기준으로 정렬된 상태)
        print("\n📋 크롤링 결과 요약 (접수일 기준 내림차순):")
        print("-" * 50)
        for i, data in enumerate(final_data[:5]):  # 처음 5개만 미리보기
            print(f"{i+1}. [{data['현황']}] {data['공고명'][:60]}...")
            print(f"    접수일: {data['접수일']} | 부처: {data['부처명']}")
        
        if len(final_data) > 5:
            print(f"... 외 {len(final_data) - 5}개 항목")
        
        return final_data

    except Exception as e:
        print(f"   ❌ 크롤링 중 심각한 오류 발생: {str(e)}")
        return []

def search_with_keyword(driver, keyword):
    """실제 검색 기능"""
    print(f"\n🔍 '{keyword}' 키워드로 검색 테스트 시작")
    print("=" * 50)
    
    # 검색창 찾기 (여러 셀렉터 시도)
    print("1️⃣ 검색창 찾기 중...")
    
    search_input = None
    possible_search_selectors = [
        (By.CSS_SELECTOR, "input[placeholder*='키워드']"),
        (By.NAME, "searchKeyword"),
        (By.ID, "searchKeyword"),
        (By.CSS_SELECTOR, "input[type='text']")
    ]
    
    for by_type, selector in possible_search_selectors:
        try:
            search_input = WebDriverWait(driver, 2).until(
                EC.presence_of_element_located((by_type, selector))
            )
            print(f"   ✅ 검색창 발견: {by_type} = '{selector}'")
            break
        except:
            continue
    
    if not search_input:
        print("   ❌ 검색창을 찾을 수 없습니다!")
        return False
    
    # 검색어 입력
    print(f"2️⃣ '{keyword}' 키워드 입력 중...")
    search_input.clear()
    search_input.send_keys(keyword)
    print("   ✅ 키워드 입력 완료")
    
    # 잠시 대기
    time.sleep(1)
    
    # 리스트 개수 30개 설정 (검색 전에!)
    print("3️⃣ 리스트 개수 30개 설정 중...")
    page_unit_success = set_page_unit_to_30(driver)
    
    if not page_unit_success:
        print("   ⚠️ 리스트 개수 설정 실패, 기본값으로 진행")
    
    time.sleep(1)
    
    # 검색 버튼 찾기 및 클릭 (정확한 셀렉터 사용)
    print("4️⃣ 검색 버튼 클릭 중...")
    
    # onclick="javascript: fn_search('1', ''); return false;" 와 class="button blue"를 가진 a 태그
    search_button = WebDriverWait(driver, 5).until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, "a.button.blue[onclick*='fn_search']"))
    )
    print("   ✅ 검색 버튼 발견: a.button.blue[onclick*='fn_search']")
    search_button.click()
    print("   ✅ 검색 버튼 클릭 완료")
    
    # 검색 결과 로딩 대기
    print("5️⃣ 검색 결과 로딩 대기...")
    time.sleep(3)
    
    # 현재 URL 확인
    current_url = driver.current_url
    print(f"   📍 검색 후 URL: {current_url}")
    
    # 검색 결과 확인
    page_source = driver.page_source.lower()
    result_indicators = ['검색결과', '검색 결과', 'search result', keyword.lower()]
    
    found_results = []
    for indicator in result_indicators:
        if indicator in page_source:
            found_results.append(indicator)
    
    if found_results:
        print(f"   ✅ 검색 결과 페이지 확인됨: {', '.join(found_results)}")
        
        # 결과 스크린샷 저장
        os.makedirs("output", exist_ok=True)
        driver.save_screenshot(f"output/search_result_{keyword}.png")
        print(f"   📸 검색 결과 스크린샷 저장: output/search_result_{keyword}.png")
        
        return True
    else:
        print("   ⚠️ 검색 결과를 확인할 수 없습니다")
        return False

def set_page_unit_to_30(driver):
    """리스트 표시 개수를 30개로 설정"""
    print("📊 리스트 표시 개수 설정")
    print("-" * 30)
    
    # 페이지 단위 드롭다운 찾기
    print("1️⃣ 페이지 단위 드롭다운 찾기...")
    page_unit_select = WebDriverWait(driver, 5).until(
        EC.presence_of_element_located((By.NAME, "pageUnit"))
    )
    print("   ✅ pageUnit 드롭다운 발견")
    
    # Select 객체 생성
    select = Select(page_unit_select)
    print("2️⃣ 30개 옵션 선택 중...")
    
    # 30 선택
    select.select_by_value("30")
    print("   ✅ 30개 옵션 선택 완료")
    
    # 선택된 값 확인
    selected_option = select.first_selected_option
    print(f"   📊 현재 선택된 값: {selected_option.get_attribute('value')}개")
    
    return True

def create_chrome_driver():
    """Chrome WebDriver 생성"""
    print("🌐 Chrome 브라우저 설정 중...")
    
    # Chrome 옵션 설정
    chrome_options = Options()
    chrome_options.add_argument("--window-size=1200,800")
    
    # ChromeDriver 서비스 설정
    service = Service(ChromeDriverManager().install())
    
    # WebDriver 생성
    driver = webdriver.Chrome(service=service, options=chrome_options)
    print("   ✅ Chrome 브라우저 준비 완료")
    
    return driver

def main():
    """메인 실행 함수"""
    print("🚀 NTIS 공고 크롤링 시작")
    print("=" * 50)
    
    driver = None
    
    try:
        # 1. 브라우저 시작
        driver = create_chrome_driver()
        
        # 2. NTIS 사이트 접속
        print("\n🌍 NTIS 사이트 접속 중...")
        
        # 정확한 NTIS 국가R&D통합공고 URL
        target_url = "https://www.ntis.go.kr/rndgate/eg/un/ra/mng.do"
        print(f"   🎯 목표 URL: {target_url}")
        
        # 재시도 로직 추가
        max_retries = 3
        for attempt in range(1, max_retries + 1):
            try:
                print(f"   시도 {attempt}/{max_retries}...")
                driver.get(target_url)
                
                # document.readyState가 complete가 될 때까지 대기
                print("   페이지 로딩 완료 대기 중...")
                WebDriverWait(driver, 20).until(
                    lambda d: d.execute_script("return document.readyState") == "complete"
                )
                print("   ✅ 페이지 로딩 완료!")
                break  # 성공하면 루프 탈출
                
            except Exception as e:
                print(f"   ⚠️ 시도 {attempt} 실패: {str(e)}")
                if attempt < max_retries:
                    print(f"   {3}초 후 재시도...")
                    time.sleep(3)
                else:
                    print("   ❌ 모든 재시도 실패!")
                    raise Exception("NTIS 사이트 접속 실패")
        
        time.sleep(2)  # 추가 안정화 대기
        
        # 실제 접속된 URL 확인
        current_url = driver.current_url
        print(f"   📍 실제 URL: {current_url}")
        
        # 페이지 제목 확인
        page_title = driver.title
        print(f"   📄 페이지 제목: {page_title}")
        
        # 검색창 확인 (여러 가능한 셀렉터 시도)
        search_found = False
        possible_search_selectors = [
            "input[placeholder*='키워드']",
            "input[name='searchKeyword']", 
            "input[id='searchKeyword']",
            "input[type='text']"
        ]
        
        for selector in possible_search_selectors:
            try:
                search_element = driver.find_element(By.CSS_SELECTOR, selector)
                print(f"   ✅ 검색창 발견! 셀렉터: {selector}")
                search_found = True
                break
            except:
                continue
        
        if not search_found:
            print("   ⚠️ 검색창을 찾을 수 없습니다. 페이지를 확인해주세요.")
            # 그래도 진행해보기
        
        print("   ✅ NTIS 사이트 접속 완료")
        
        # 3. 검색 키워드 가져오기
        try:
            keywords = get_search_keywords()
            if keywords:
                keyword = keywords[0]  # 첫 번째 키워드 사용
                print(f"   📝 설정 키워드 사용: {keyword}")
            else:
                keyword = "AI"
                print(f"   📝 기본 키워드 사용: {keyword}")
        except:
            keyword = "AI"
            print(f"   📝 기본 키워드 사용: {keyword}")
        
        # 4. 키워드 검색
        search_success = search_with_keyword(driver, keyword)
        
        if not search_success:
            print("❌ 검색이 실패했습니다.")
            return
        
        # 5. 리스트 크롤링
        crawled_data = crawl_announcement_list(driver, target_count=30)
        
        if not crawled_data:
            print("❌ 크롤링이 실패했습니다.")
            return
        
        # 6. 데이터 관리 (기존 데이터와 비교, 신규 항목 처리)
        try:
            print("\n📊 데이터 관리 시작...")
            os.makedirs("output", exist_ok=True)
            
            # 기존 old_data.json 로드
            existing_data = []
            old_data_file = "output/old_data.json"
            if os.path.exists(old_data_file):
                with open(old_data_file, "r", encoding="utf-8") as f:
                    existing_data = json.load(f)
            print(f"   📂 기존 데이터: {len(existing_data)}개")
            
            # 기존 데이터의 roRndUid 추출
            existing_uids = set()
            for item in existing_data:
                uid = extract_uid_from_url(item.get("상세_URL", ""))
                if uid:
                    existing_uids.add(uid)
            
            # 신규 항목 찾기
            new_items = []
            for item in crawled_data:
                uid = extract_uid_from_url(item.get("상세_URL", ""))
                if uid and uid not in existing_uids:
                    new_items.append(item)
            
            print(f"   🆕 신규 항목: {len(new_items)}개")
            print(f"   🔄 중복 항목: {len(crawled_data) - len(new_items)}개")
            
            # 신규 항목이 있으면 처리
            if new_items:
                # 기존 + 신규 합치기
                all_items = existing_data + new_items
                
                # 접수일 기준 내림차순 정렬
                def parse_date_for_sort(date_str):
                    try:
                        return datetime.strptime(date_str, "%Y.%m.%d")
                    except:
                        return datetime.min
                
                sorted_items = sorted(all_items, key=lambda x: parse_date_for_sort(x.get("접수일", "")), reverse=True)
                
                # 최신 30개만 유지
                final_items = sorted_items[:30]
                
                # old_data.json 업데이트 (전체 30개 저장)
                with open(old_data_file, "w", encoding="utf-8") as f:
                    json.dump(final_items, f, ensure_ascii=False, indent=2)
                print(f"   💾 전체 데이터 저장: output/old_data.json ({len(final_items)}개)")
                
                # 신규 항목만 별도 저장
                with open("output/new_data.json", "w", encoding="utf-8") as f:
                    json.dump(new_items, f, ensure_ascii=False, indent=2)
                print(f"   🆕 신규 데이터 저장: output/new_data.json ({len(new_items)}개)")
                
            else:
                print("   ℹ️ 신규 항목이 없어 데이터 업데이트를 건너뜁니다.")
                # 신규 항목이 없어도 old_data.json은 업데이트 (크롤링된 최신 30개)
                with open(old_data_file, "w", encoding="utf-8") as f:
                    json.dump(crawled_data[:30], f, ensure_ascii=False, indent=2)
                print(f"   💾 전체 데이터 업데이트: output/old_data.json ({len(crawled_data[:30])}개)")
                
                # new_data.json은 빈 배열로 초기화
                with open("output/new_data.json", "w", encoding="utf-8") as f:
                    json.dump([], f, ensure_ascii=False, indent=2)
                print(f"   🆕 신규 데이터 없음: output/new_data.json (0개)")
            
            print(f"\n📋 최종 요약:")
            print(f"   - 크롤링 항목: {len(crawled_data)}개")
            print(f"   - 신규 항목: {len(new_items)}개")
            print(f"   - 처리 완료: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
            
        except Exception as e:
            print(f"⚠️ 데이터 관리 중 오류: {str(e)}")
            print("   크롤링 데이터만 저장합니다.")
            
            # 기본 JSON 저장
            with open("output/ntis_crawled_raw.json", "w", encoding="utf-8") as f:
                json.dump(crawled_data, f, ensure_ascii=False, indent=2)
            print("   💾 원시 데이터 저장: output/ntis_crawled_raw.json")
        
        print("\n🎉 크롤링 완료!")
        
    except Exception as e:
        print(f"❌ 메인 실행 중 오류: {str(e)}")
    
    finally:
        if driver:
            print("\n🔒 브라우저 종료 중...")
            driver.quit()
            print("   ✅ 브라우저 종료 완료")

if __name__ == "__main__":
    main()