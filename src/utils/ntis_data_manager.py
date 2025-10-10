"""
NTIS 공고 데이터 관리자
- 30개 고정 크기 유지
- 새로운 데이터와 기존 데이터 비교
- 상세 크롤링 상태 관리
"""

import json
import os
import re
from datetime import datetime
from typing import List, Dict, Optional, Tuple

class NTISDataManager:
    """NTIS 공고 데이터를 관리하는 클래스"""
    
    def __init__(self, json_file_path: str = "output/ntis_managed_data.json"):
        self.json_file_path = json_file_path
        self.max_items = 30  # 최대 30개 유지
        self.data_structure = {
            "last_updated": "",
            "search_keyword": "",
            "total_count": 0,
            "announcements": []
        }
    
    def extract_uid_from_url(self, url: str) -> str:
        """상세_URL에서 roRndUid 추출"""
        try:
            # roRndUid=숫자 패턴 찾기
            match = re.search(r'roRndUid=(\d+)', url)
            if match:
                return match.group(1)
            else:
                return ""
        except Exception:
            return ""
    
    def load_existing_data(self) -> Dict:
        """기존 JSON 데이터 로드"""
        try:
            if os.path.exists(self.json_file_path):
                with open(self.json_file_path, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    print(f"✅ 기존 데이터 로드: {len(data.get('announcements', []))}개")
                    return data
            else:
                print("📄 기존 데이터 없음, 새로 시작")
                return self.data_structure.copy()
        except Exception as e:
            print(f"❌ 데이터 로드 실패: {str(e)}")
            return self.data_structure.copy()
    
    def save_data(self, data: Dict) -> bool:
        """데이터를 JSON 파일로 저장"""
        try:
            # output 폴더 생성
            os.makedirs(os.path.dirname(self.json_file_path), exist_ok=True)
            
            # 타임스탬프 업데이트
            data["last_updated"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            
            with open(self.json_file_path, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
            
            print(f"💾 데이터 저장 완료: {self.json_file_path}")
            return True
        except Exception as e:
            print(f"❌ 데이터 저장 실패: {str(e)}")
            return False
    
    def compare_and_find_new(self, new_crawled_data: List[Dict], keyword: str) -> Tuple[List[Dict], List[Dict]]:
        """새 데이터와 기존 데이터를 비교하여 신규 항목 찾기"""
        print(f"\n🔍 데이터 비교 시작 (키워드: {keyword})")
        
        # 기존 데이터 로드
        existing_data = self.load_existing_data()
        existing_announcements = existing_data.get("announcements", [])
        
        # 기존 공고 UID들 추출 (roRndUid 기준)
        existing_uids = set()
        for item in existing_announcements:
            uid = self.extract_uid_from_url(item.get("상세_URL", ""))
            if uid:
                existing_uids.add(uid)
        
        print(f"   📊 기존 데이터: {len(existing_uids)}개")
        print(f"   📊 새 데이터: {len(new_crawled_data)}개")
        
        # 신규 항목과 기존 항목 분류
        new_items = []
        existing_items = []
        
        for item in new_crawled_data:
            item_uid = self.extract_uid_from_url(item.get("상세_URL", ""))
            
            # 데이터 구조 표준화
            standardized_item = {
                "현황": item.get("현황", ""),
                "공고명": item.get("공고명", ""),
                "부처명": item.get("부처명", ""),
                "접수일": item.get("접수일", ""),
                "마감일": item.get("마감일", ""),
                "상세_URL": item.get("상세_URL", ""),
                "onclick": item.get("onclick", ""),
                "D_day": item.get("D_day", ""),
                "crawled_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "is_detailed": False,
                "detail_data": {}
            }
            
            if item_uid and item_uid not in existing_uids:
                new_items.append(standardized_item)
                print(f"   🆕 신규 발견: [UID:{item_uid}] {item.get('공고명', '')[:50]}...")
            else:
                existing_items.append(standardized_item)
        
        print(f"   ✅ 비교 완료: 신규 {len(new_items)}개, 기존 {len(existing_items)}개")
        
        return new_items, existing_items
    
    def update_data_with_new_items(self, new_items: List[Dict], all_current_items: List[Dict], keyword: str) -> Dict:
        """새 항목을 추가하고 30개로 제한하여 데이터 업데이트"""
        print(f"\n📝 데이터 업데이트 시작")
        
        # 기존 데이터 로드
        existing_data = self.load_existing_data()
        
        # 전체 현재 항목들을 최신 순으로 정렬 (접수일 기준 내림차순)
        try:
            # 접수일 형태: "2025.09.08" -> datetime 객체로 변환하여 정렬
            def parse_date(date_str):
                try:
                    return datetime.strptime(date_str, "%Y.%m.%d")
                except:
                    return datetime.min  # 파싱 실패시 가장 오래된 날짜로 처리
            
            all_current_items.sort(key=lambda x: parse_date(x.get("접수일", "")), reverse=True)
            print(f"   📅 접수일 기준 정렬 완료 (최신순)")
        except Exception as e:
            print(f"   ⚠️ 접수일 정렬 실패, 원본 순서 유지: {str(e)}")
            # 접수일 정렬이 실패하면 원본 순서 유지
        
        # 최신 30개만 유지
        final_items = all_current_items[:self.max_items]
        
        # 제거된 항목 개수 계산
        removed_count = len(all_current_items) - len(final_items)
        
        # 데이터 구조 업데이트
        updated_data = {
            "last_updated": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "search_keyword": keyword,
            "total_count": len(final_items),
            "new_items_count": len(new_items),
            "removed_old_count": removed_count,
            "announcements": final_items
        }
        
        print(f"   📊 업데이트 결과:")
        print(f"      🆕 신규 추가: {len(new_items)}개")
        print(f"      🗑️ 오래된 항목 제거: {removed_count}개")
        print(f"      📋 최종 유지: {len(final_items)}개")
        
        return updated_data
    
    def get_items_for_detail_crawling(self, data: Dict) -> List[Dict]:
        """상세 크롤링이 필요한 항목들 반환"""
        items_to_crawl = []
        
        for item in data.get("announcements", []):
            if not item.get("is_detailed", False):
                items_to_crawl.append(item)
        
        print(f"🔍 상세 크롤링 필요 항목: {len(items_to_crawl)}개")
        return items_to_crawl
    
    def mark_as_detailed(self, data: Dict, 순번: str, detail_data: Dict) -> Dict:
        """특정 항목을 상세 크롤링 완료로 마크"""
        for item in data.get("announcements", []):
            if item.get("순번") == 순번:
                item["is_detailed"] = True
                item["detail_data"] = detail_data
                item["detail_crawled_at"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                print(f"✅ 상세 크롤링 완료 마크: [{순번}] {item.get('공고명', '')[:30]}...")
                break
        
        return data
    
    def get_summary(self, data: Dict) -> Dict:
        """데이터 요약 정보 반환"""
        announcements = data.get("announcements", [])
        
        summary = {
            "총_항목수": len(announcements),
            "신규_항목수": data.get("new_items_count", 0),
            "제거된_항목수": data.get("removed_old_count", 0),
            "상세크롤링_완료": len([item for item in announcements if item.get("is_detailed", False)]),
            "상세크롤링_대기": len([item for item in announcements if not item.get("is_detailed", False)]),
            "마지막_업데이트": data.get("last_updated", ""),
            "검색_키워드": data.get("search_keyword", "")
        }
        
        return summary

if __name__ == "__main__":
    # 테스트 코드
    print("🧪 NTIS 데이터 매니저 테스트")
    print("=" * 50)
    
    manager = NTISDataManager()
    
    # 테스트 데이터
    test_data = [
        {"공고명": "테스트 공고 1", "부처명": "테스트부처", "상세_URL": "https://www.ntis.go.kr/rndgate/eg/un/ra/view.do?roRndUid=100&flag=rndList"},
        {"공고명": "테스트 공고 2", "부처명": "테스트부처", "상세_URL": "https://www.ntis.go.kr/rndgate/eg/un/ra/view.do?roRndUid=101&flag=rndList"}
    ]
    
    # 비교 테스트
    new_items, existing_items = manager.compare_and_find_new(test_data, "테스트")
    
    # 업데이트 테스트
    updated_data = manager.update_data_with_new_items(new_items, test_data, "테스트")
    
    # 요약 출력
    summary = manager.get_summary(updated_data)
    print(f"\n📊 요약: {summary}")
    
    print("\n✅ 테스트 완료!")
