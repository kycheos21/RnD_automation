#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
HWPX 파일 파서
HWPX는 ZIP 압축된 XML 기반 형식이므로 압축 해제 후 XML 파싱
"""

import os
import re
import zipfile
import xml.etree.ElementTree as ET
from typing import Optional, Dict

class HWPXParser:
    """HWPX 파일 파서"""
    
    def __init__(self):
        """초기화"""
        print("HWPX 파서 초기화 완료")
    
    def extract_text_from_hwpx(self, hwpx_file_path: str) -> Dict:
        """HWPX 파일에서 텍스트 추출"""
        try:
            print(f"HWPX 파일 파싱 시작: {hwpx_file_path}")
            
            result = {
                "success": False,
                "hwpx_file": hwpx_file_path,
                "full_text": None,
                "business_overview": None,
                "error": None
            }
            
            # 파일 존재 확인
            if not os.path.exists(hwpx_file_path):
                result["error"] = f"파일이 존재하지 않음: {hwpx_file_path}"
                return result
            
            # HWPX 파일에서 텍스트 추출
            try:
                full_text = self._extract_text_from_zip(hwpx_file_path)
                
                if not full_text:
                    result["error"] = "HWPX에서 텍스트를 추출할 수 없음"
                    return result
                
                print("HWPX 텍스트 추출 성공")
            except Exception as e:
                result["error"] = f"HWPX 텍스트 추출 실패: {str(e)}"
                return result
            
            result["full_text"] = full_text
            print(f"전체 텍스트 추출 완료: {len(full_text)}자")
            
            # 앞부분 3000자 추출 (사업개요 포함)
            front_text = full_text[:3000] if len(full_text) > 3000 else full_text
            result["business_overview"] = front_text
            print(f"앞부분 텍스트 추출 완료: {len(front_text)}자")
            
            result["success"] = True
            return result
            
        except Exception as e:
            print(f"HWPX 파싱 실패: {str(e)}")
            return {
                "success": False,
                "hwpx_file": hwpx_file_path,
                "full_text": None,
                "business_overview": None,
                "error": str(e)
            }
    
    def _extract_text_from_zip(self, hwpx_file_path: str) -> str:
        """HWPX(ZIP) 파일에서 XML을 추출하고 텍스트 파싱"""
        try:
            print("   HWPX ZIP 파일 열기...")
            
            all_text = []
            
            with zipfile.ZipFile(hwpx_file_path, 'r') as zip_file:
                # ZIP 내부 파일 목록 확인
                file_list = zip_file.namelist()
                print(f"   ZIP 내부 파일 개수: {len(file_list)}")
                
                # Contents/section*.xml 파일들 찾기
                section_files = [f for f in file_list if f.startswith('Contents/section') and f.endswith('.xml')]
                section_files.sort()  # 순서대로 정렬
                
                print(f"   섹션 파일 발견: {len(section_files)}개")
                
                for section_file in section_files:
                    try:
                        # XML 파일 읽기
                        with zip_file.open(section_file) as xml_file:
                            xml_content = xml_file.read()
                            
                            # XML 파싱
                            root = ET.fromstring(xml_content)
                            
                            # 모든 텍스트 노드 추출
                            text = self._extract_text_from_xml(root)
                            if text:
                                all_text.append(text)
                    
                    except Exception as e:
                        print(f"   ⚠️ {section_file} 파싱 실패: {e}")
                        continue
            
            if not all_text:
                print("   ❌ 추출된 텍스트가 없음")
                return ""
            
            # 모든 섹션의 텍스트 합치기
            full_text = '\n\n'.join(all_text)
            
            # 텍스트 정리
            cleaned_text = self._clean_text(full_text)
            
            print(f"   ✅ HWPX 텍스트 추출 성공: {len(cleaned_text)}자")
            return cleaned_text
            
        except Exception as e:
            print(f"   ❌ HWPX ZIP 추출 실패: {e}")
            return ""
    
    def _extract_text_from_xml(self, element: ET.Element) -> str:
        """XML 엘리먼트에서 재귀적으로 텍스트 추출"""
        texts = []
        
        # 현재 엘리먼트의 텍스트
        if element.text:
            texts.append(element.text.strip())
        
        # 자식 엘리먼트들 순회
        for child in element:
            child_text = self._extract_text_from_xml(child)
            if child_text:
                texts.append(child_text)
            
            # tail 텍스트도 추출
            if child.tail:
                texts.append(child.tail.strip())
        
        return ' '.join(text for text in texts if text)
    
    def _clean_text(self, text: str) -> str:
        """텍스트 정리 (불필요한 문자 제거)"""
        try:
            if not text:
                return ""
            
            # 연속된 공백을 단일 공백으로
            cleaned = re.sub(r'\s+', ' ', text)
            
            # 연속된 줄바꿈 제거 (최대 2개까지)
            cleaned = re.sub(r'\n{3,}', '\n\n', cleaned)
            
            # 불필요한 특수문자 제거 (한글, 영문, 숫자, 기본 문장부호만 유지)
            cleaned = re.sub(r'[^\w\s가-힣.,():\-\n/·~•]', '', cleaned)
            
            # 앞뒤 공백 제거
            cleaned = cleaned.strip()
            
            return cleaned
            
        except Exception as e:
            print(f"텍스트 정리 실패: {str(e)}")
            return text

def main():
    """테스트용 메인 함수"""
    print("HWPX 파서 테스트")
    print("=" * 50)
    
    # 테스트할 HWPX 파일 경로
    test_file = "output/hwp_files/1. 2025년도 K-AI 신약개발 전임상·임상 모델개발(R&D) 사업 신규지원 대상과제 공고문.hwpx"
    
    if not os.path.exists(test_file):
        print(f"파일이 존재하지 않습니다: {test_file}")
        return
    
    parser = HWPXParser()
    result = parser.extract_text_from_hwpx(test_file)
    
    if result["success"]:
        print("\n✅ HWPX 파싱 성공!")
        print(f"📄 파일: {result['hwpx_file']}")
        print(f"📝 전체 텍스트: {len(result['full_text'])}자")
        print(f"🎯 앞부분 텍스트: {len(result['business_overview'])}자")
        
        print("\n앞부분 텍스트 미리보기:")
        print("-" * 50)
        print(result['business_overview'][:500] + "...")
    else:
        print(f"\n❌ 파싱 실패: {result['error']}")

if __name__ == "__main__":
    main()

