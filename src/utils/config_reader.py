"""
MD 문서에서 설정값을 동적으로 읽어오는 유틸리티
"""
import re
import os
from typing import List, Optional, Dict, Any

class ConfigReader:
    """MD 문서에서 설정값을 파싱하는 클래스"""
    
    def __init__(self, docs_path: str = "docs"):
        self.docs_path = docs_path
        self.setup_requirements_file = os.path.join(docs_path, "setup-requirements.md")
        self.ui_elements_file = os.path.join(docs_path, "ntis-ui-elements.md")
    
    def get_search_keywords(self) -> Dict[str, List[str]]:
        """
        ntis-ui-elements.md에서 검색키워드를 추출
        
        Returns:
            Dict[str, List[str]]: 키워드 카테고리별 리스트
        """
        try:
            if not os.path.exists(self.ui_elements_file):
                print(f"경고: UI 요소 파일을 찾을 수 없습니다: {self.ui_elements_file}")
                return self._get_default_keywords()
            
            with open(self.ui_elements_file, 'r', encoding='utf-8') as f:
                content = f.read()
            
            keywords_dict = {}
            
            # 각 키워드 카테고리 추출
            patterns = {
                'primary': r'PRIMARY_KEYWORDS=([^\n\r]+)',
                'secondary': r'SECONDARY_KEYWORDS=([^\n\r]+)',
                'tertiary': r'TERTIARY_KEYWORDS=([^\n\r]+)',
                'exclude': r'EXCLUDE_KEYWORDS=([^\n\r]+)'
            }
            
            for category, pattern in patterns.items():
                match = re.search(pattern, content)
                if match:
                    keywords_str = match.group(1).strip()
                    keywords = [kw.strip() for kw in keywords_str.split(',') if kw.strip()]
                    keywords_dict[category] = keywords
                else:
                    keywords_dict[category] = []
            
            # 검색 옵션도 추출
            search_options = {}
            option_patterns = {
                'search_type': r'SEARCH_TYPE=([^\n\r]+)',
                'search_limit': r'SEARCH_LIMIT=([^\n\r]+)',
                'search_sort': r'SEARCH_SORT=([^\n\r]+)'
            }
            
            for option, pattern in option_patterns.items():
                match = re.search(pattern, content)
                if match:
                    search_options[option] = match.group(1).strip()
            
            keywords_dict['options'] = search_options
            
            if any(keywords_dict[cat] for cat in ['primary', 'secondary', 'tertiary']):
                print(f"성공: UI 요소 파일에서 검색 키워드 로드: {keywords_dict}")
                return keywords_dict
            else:
                print("경고: UI 요소 파일에서 키워드를 찾을 수 없습니다")
                return self._get_default_keywords()
                
        except Exception as e:
            print(f"오류: UI 요소 파일 읽기 실패: {str(e)}")
            return self._get_default_keywords()
    
    def _get_default_keywords(self) -> Dict[str, List[str]]:
        """기본 키워드 반환"""
        default_keywords = {
            'primary': ["AI", "인공지능", "머신러닝", "딥러닝"],
            'secondary': ["빅데이터", "IoT", "블록체인", "클라우드"],
            'tertiary': ["스마트팩토리", "디지털트윈", "메타버스", "NFT"],
            'exclude': ["완료", "마감", "종료", "취소"],
            'options': {
                'search_type': '본공고',
                'search_limit': '100',
                'search_sort': '마감일순'
            }
        }
        print(f"기본값: 기본 키워드 사용: {default_keywords}")
        return default_keywords
    
    def get_ui_elements(self) -> Dict[str, Dict[str, str]]:
        """
        ntis-ui-elements.md에서 UI 요소 정보를 추출
        
        Returns:
            Dict[str, Dict[str, str]]: UI 요소별 속성 정보
        """
        try:
            if not os.path.exists(self.ui_elements_file):
                print(f"경고: UI 요소 파일을 찾을 수 없습니다: {self.ui_elements_file}")
                return self._get_default_ui_elements()
            
            with open(self.ui_elements_file, 'r', encoding='utf-8') as f:
                content = f.read()
            
            ui_elements = {}
            
            # 검색 입력창 정보 추출
            search_input_pattern = r'### 검색 입력창\s*```\s*([\s\S]*?)\s*```'
            match = re.search(search_input_pattern, content)
            if match:
                input_info = self._parse_element_info(match.group(1))
                ui_elements['search_input'] = input_info
            
            # 검색 버튼 정보 추출  
            search_button_pattern = r'### 검색 버튼\s*```\s*([\s\S]*?)\s*```'
            match = re.search(search_button_pattern, content)
            if match:
                button_info = self._parse_element_info(match.group(1))
                ui_elements['search_button'] = button_info
            
            # 리스트 개수 선택 드롭다운 정보 추출
            page_unit_pattern = r'### 리스트 개수 선택 드롭다운\s*```\s*([\s\S]*?)\s*```'
            match = re.search(page_unit_pattern, content)
            if match:
                page_unit_info = self._parse_element_info(match.group(1))
                ui_elements['page_unit'] = page_unit_info
            
            if ui_elements:
                print(f"성공: MD 문서에서 UI 요소 로드: {list(ui_elements.keys())}")
                return ui_elements
            else:
                print("경고: MD 문서에서 UI 요소를 찾을 수 없습니다")
                return self._get_default_ui_elements()
                
        except Exception as e:
            print(f"오류: UI 요소 MD 파일 읽기 실패: {str(e)}")
            return self._get_default_ui_elements()
    
    def _parse_element_info(self, element_text: str) -> Dict[str, str]:
        """요소 정보 텍스트를 파싱"""
        info = {}
        for line in element_text.strip().split('\n'):
            if '=' in line:
                key, value = line.split('=', 1)
                info[key.strip()] = value.strip()
        return info
    
    def _get_default_ui_elements(self) -> Dict[str, Dict[str, str]]:
        """기본 UI 요소 정보 반환"""
        default_elements = {
            'search_input': {
                'ID': 'searchKeyword',
                'NAME': 'searchKeyword',
                'TYPE': 'text'
            },
            'search_button': {
                'TAG': 'a',
                'CLASS': 'button blue',
                'ONCLICK': "javascript: fn_search('1', ''); return false;"
            },
            'page_unit': {
                'TAG': 'select',
                'NAME': 'pageUnit',
                'CLASS': 'selbp90',
                'TARGET_VALUE': '30'
            }
        }
        print(f"기본값: 기본 UI 요소 사용: {list(default_elements.keys())}")
        return default_elements
    
    def get_selenium_selector(self, element_name: str) -> str:
        """UI 요소 이름으로 Selenium 셀렉터 생성"""
        ui_elements = self.get_ui_elements()
        
        if element_name not in ui_elements:
            print(f"경고: '{element_name}' UI 요소를 찾을 수 없습니다")
            return ""
        
        element_info = ui_elements[element_name]
        
        # ID가 있으면 ID 우선 사용
        if 'ID' in element_info:
            return f"#{element_info['ID']}"
        
        # CLASS가 있으면 클래스 사용
        if 'CLASS' in element_info:
            classes = element_info['CLASS'].replace(' ', '.')
            if 'TAG' in element_info:
                return f"{element_info['TAG']}.{classes}"
            else:
                return f".{classes}"
        
        # 마지막으로 태그만 사용
        if 'TAG' in element_info:
            return element_info['TAG']
        
        return ""
    
    def get_config_summary(self) -> Dict[str, Any]:
        """현재 설정 요약 정보 반환"""
        keywords_dict = self.get_search_keywords()
        ui_elements = self.get_ui_elements()
        
        # 전체 키워드 개수 계산
        total_keywords = 0
        for category in ['primary', 'secondary', 'tertiary']:
            total_keywords += len(keywords_dict.get(category, []))
        
        return {
            "source_file": self.ui_elements_file,
            "ui_elements_file": self.ui_elements_file,
            "keywords_count": total_keywords,
            "keywords": keywords_dict,
            "ui_elements_count": len(ui_elements),
            "ui_elements": list(ui_elements.keys()),
            "status": "loaded_from_md" if os.path.exists(self.ui_elements_file) else "using_defaults"
        }

# 전역 인스턴스 생성 (싱글톤 패턴)
_config_reader = None

def get_config_reader() -> ConfigReader:
    """ConfigReader 인스턴스 반환 (싱글톤)"""
    global _config_reader
    if _config_reader is None:
        _config_reader = ConfigReader()
    return _config_reader

def get_search_keywords() -> Dict[str, List[str]]:
    """검색 키워드를 간편하게 가져오는 함수"""
    return get_config_reader().get_search_keywords()

def get_primary_keywords() -> List[str]:
    """주요 검색 키워드만 가져오는 함수"""
    keywords_dict = get_config_reader().get_search_keywords()
    return keywords_dict.get('primary', [])

def get_all_search_keywords() -> List[str]:
    """모든 검색 키워드를 하나의 리스트로 가져오는 함수"""
    keywords_dict = get_config_reader().get_search_keywords()
    all_keywords = []
    all_keywords.extend(keywords_dict.get('primary', []))
    all_keywords.extend(keywords_dict.get('secondary', []))
    all_keywords.extend(keywords_dict.get('tertiary', []))
    return all_keywords

def get_exclude_keywords() -> List[str]:
    """제외 키워드를 가져오는 함수"""
    keywords_dict = get_config_reader().get_search_keywords()
    return keywords_dict.get('exclude', [])

def get_search_options() -> Dict[str, str]:
    """검색 옵션을 가져오는 함수"""
    keywords_dict = get_config_reader().get_search_keywords()
    return keywords_dict.get('options', {})

def get_ui_selector(element_name: str) -> str:
    """UI 요소의 Selenium 셀렉터를 간편하게 가져오는 함수"""
    return get_config_reader().get_selenium_selector(element_name)

def get_page_unit_target_value() -> str:
    """페이지 단위 선택에서 목표 값을 가져오는 함수"""
    config = get_config_reader()
    ui_elements = config.get_ui_elements()
    
    if 'page_unit' in ui_elements:
        page_unit_info = ui_elements['page_unit']
        return page_unit_info.get('TARGET_VALUE', '100')
    
    return '100'  # 기본값

if __name__ == "__main__":
    # 테스트 코드
    print("MD 문서 설정 읽기 테스트")
    print("=" * 50)
    
    config = get_config_reader()
    summary = config.get_config_summary()
    
    print(f"설정 파일: {summary['source_file']}")
    print(f"UI 요소 파일: {summary['ui_elements_file']}")
    print(f"총 키워드 개수: {summary['keywords_count']}개")
    print(f"주요 키워드: {summary['keywords'].get('primary', [])}")
    print(f"보조 키워드: {summary['keywords'].get('secondary', [])}")
    print(f"추가 키워드: {summary['keywords'].get('tertiary', [])}")
    print(f"제외 키워드: {summary['keywords'].get('exclude', [])}")
    print(f"검색 옵션: {summary['keywords'].get('options', {})}")
    print(f"UI 요소 개수: {summary['ui_elements_count']}개")
    print(f"UI 요소 목록: {summary['ui_elements']}")
    print(f"상태: {summary['status']}")
    
    print("\nUI 셀렉터 생성 테스트")
    print("-" * 30)
    search_input_selector = get_ui_selector('search_input')
    search_button_selector = get_ui_selector('search_button')
    page_unit_selector = get_ui_selector('page_unit')
    target_value = get_page_unit_target_value()
    
    print(f"검색 입력창 셀렉터: {search_input_selector}")
    print(f"검색 버튼 셀렉터: {search_button_selector}")
    print(f"페이지 단위 선택 셀렉터: {page_unit_selector}")
    print(f"목표 페이지 단위 값: {target_value}개")
    
    print("\n" + "=" * 50)
    print("설정 읽기 테스트 완료!")
