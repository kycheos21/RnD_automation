#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
HWP 파일 직접 파서
pyhwp 라이브러리를 사용하여 GUI 자동화 없이 HWP 파일에서 텍스트 추출
"""

import os
import re
from typing import Optional, Dict, List
import hwp5
from hwp5 import hwp5txt

class HWPParser:
    """HWP 파일 직접 파서 (pyhwp 사용)"""
    
    def __init__(self):
        """초기화"""
        print("HWP 파서 초기화 완료 (pyhwp 사용)")
    
    def extract_text_from_hwp(self, hwp_file_path: str) -> Dict:
        """HWP 파일에서 텍스트 추출"""
        try:
            print(f"HWP 파일 파싱 시작: {hwp_file_path}")
            
            result = {
                "success": False,
                "hwp_file": hwp_file_path,
                "full_text": None,
                "business_overview": None,
                "error": None
            }
            
            # 파일 존재 확인
            if not os.path.exists(hwp_file_path):
                result["error"] = f"파일이 존재하지 않음: {hwp_file_path}"
                return result
            
            # HWP 파일에서 텍스트 추출 (hwp5txt 사용)
            try:
                full_text = self._extract_text_with_hwp5txt(hwp_file_path)
                print("HWP 텍스트 추출 성공")
            except Exception as e:
                result["error"] = f"HWP 텍스트 추출 실패: {str(e)}"
                return result
            
            if not full_text:
                result["error"] = "추출된 텍스트가 없음"
                return result
            
            result["full_text"] = full_text
            print(f"전체 텍스트 추출 완료: {len(full_text)}자")
            
            # 사업개요 섹션 추출
            business_overview = self._find_business_overview_section(full_text)
            if business_overview:
                result["business_overview"] = business_overview
                print(f"사업개요 섹션 추출 완료: {len(business_overview)}자")
            else:
                print("사업개요 섹션을 찾을 수 없음 (전체 텍스트는 추출됨)")
            
            result["success"] = True
            return result
            
        except Exception as e:
            print(f"HWP 파싱 실패: {str(e)}")
            return {
                "success": False,
                "hwp_file": hwp_file_path,
                "full_text": None,
                "business_overview": None,
                "error": str(e)
            }
        finally:
            # 파일 정리
            try:
                if 'hwp_file' in locals():
                    hwp_file.close()
            except:
                pass
    
    def _extract_text_with_hwp5txt(self, hwp_file_path: str) -> str:
        """hwp5txt를 사용하여 HWP 파일에서 텍스트 추출"""
        try:
            import subprocess
            import sys
            
            # Python 실행 파일 경로 (가상환경 고려)
            python_exe = sys.executable
            
            # hwp5txt 명령어 실행
            cmd = [python_exe, "-m", "hwp5.hwp5txt", hwp_file_path]
            print(f"명령어 실행: {' '.join(cmd)}")
            
            # Windows 한글 인코딩 처리
            try:
                result = subprocess.run(
                    cmd,
                    capture_output=True,
                    text=True,
                    encoding='cp949'  # Windows 한글 인코딩
                )
            except UnicodeDecodeError:
                # cp949로 실패하면 utf-8 시도
                result = subprocess.run(
                    cmd,
                    capture_output=True,
                    text=True,
                    encoding='utf-8',
                    errors='ignore'  # 인코딩 에러 무시
                )
            
            print(f"명령어 실행 결과: returncode={result.returncode}")
            print(f"stdout 길이: {len(result.stdout) if result.stdout else 0}")
            print(f"stderr: {result.stderr}")
            
            if result.returncode == 0:
                extracted_text = result.stdout
                if extracted_text and extracted_text.strip():
                    # 텍스트 정리
                    cleaned_text = self._clean_text(extracted_text)
                    print(f"텍스트 추출 완료: {len(cleaned_text)}자")
                    return cleaned_text
                else:
                    print("추출된 텍스트가 없습니다 - 대체 방법 시도")
                    # 대체 방법 시도
                    return self._extract_text_fallback(hwp_file_path)
            else:
                print(f"hwp5txt 실행 실패: {result.stderr}")
                # 대체 방법 시도
                return self._extract_text_fallback(hwp_file_path)
                
        except Exception as e:
            print(f"hwp5txt 텍스트 추출 실패: {str(e)}")
            # 대체 방법 시도
            return self._extract_text_fallback(hwp_file_path)
    
    def _extract_text_fallback(self, hwp_file_path: str) -> str:
        """대체 텍스트 추출 방법 (olefile 사용)"""
        try:
            print("대체 텍스트 추출 방법 시도...")
            
            # olefile을 직접 사용해서 텍스트 추출 시도
            import subprocess
            import sys
            
            # 다른 hwp5 명령어들 시도
            commands = [
                [sys.executable, "-c", f"import hwp5; print('HWP5 버전:', hwp5.__version__)"],
                [sys.executable, "-c", f"from hwp5.hwp5txt import main; main(['{hwp_file_path}'])"]
            ]
            
            for cmd in commands:
                try:
                    print(f"시도: {' '.join(cmd[:2])}...")
                    # 인코딩 처리
                    try:
                        result = subprocess.run(cmd, capture_output=True, text=True, encoding='cp949')
                    except UnicodeDecodeError:
                        result = subprocess.run(cmd, capture_output=True, text=True, encoding='utf-8', errors='ignore')
                    
                    if result.returncode == 0 and result.stdout and result.stdout.strip():
                        print(f"대체 방법 성공: {len(result.stdout)}자")
                        print(f"추출된 내용: '{result.stdout[:200]}...'")  # 디버깅용
                        return self._clean_text(result.stdout)
                except Exception as e:
                    print(f"명령어 실패: {str(e)}")
                    continue
            
            print("모든 대체 방법 실패")
            return ""
                    
        except Exception as e:
            print(f"대체 텍스트 추출도 실패: {str(e)}")
            return ""
    
    def _find_business_overview_section(self, full_text: str) -> Optional[str]:
        """사업개요 섹션 찾기 및 추출"""
        try:
            print("사업개요 섹션 검색 중...")
            
            # 사업개요 관련 키워드들 (우선순위 순)
            overview_keywords = [
                "사업개요",
                "사업목적", 
                "추진배경",
                "사업내용",
                "지원내용",
                "사업 개요",
                "사업 목적",
                "추진 배경",
                "1. 사업개요",
                "가. 사업개요",
                "◦ 사업개요",
                "○ 사업개요"
            ]
            
            # 섹션 종료 키워드들
            end_keywords = [
                "지원대상",
                "신청자격", 
                "지원규모",
                "신청방법",
                "제출서류",
                "문의처",
                "접수방법",
                "신청기간",
                "2.",
                "나.",
                "◦ 지원대상",
                "○ 지원대상",
                "다."
            ]
            
            best_match = None
            best_score = 0
            
            for keyword in overview_keywords:
                # 키워드 위치 찾기 (대소문자 무시)
                keyword_pos = full_text.lower().find(keyword.lower())
                if keyword_pos != -1:
                    print(f"'{keyword}' 키워드 발견 (위치: {keyword_pos})")
                    
                    # 키워드 이후 텍스트에서 다음 섹션까지 추출
                    start_pos = keyword_pos
                    end_pos = len(full_text)
                    
                    # 종료 키워드 찾기
                    for end_keyword in end_keywords:
                        end_candidate = full_text.lower().find(end_keyword.lower(), start_pos + len(keyword))
                        if end_candidate != -1 and end_candidate < end_pos:
                            end_pos = end_candidate
                    
                    # 섹션 텍스트 추출
                    section_text = full_text[start_pos:end_pos].strip()
                    
                    # 점수 계산 (키워드 우선순위 + 텍스트 길이)
                    priority_score = len(overview_keywords) - overview_keywords.index(keyword)
                    length_score = min(len(section_text) // 100, 10)  # 최대 10점
                    total_score = priority_score * 10 + length_score
                    
                    if total_score > best_score and len(section_text) > 50:  # 최소 길이 확인
                        best_score = total_score
                        best_match = section_text
                        print(f"최적 매치 업데이트: '{keyword}' (점수: {total_score}, 길이: {len(section_text)})")
            
            if best_match:
                # 텍스트 정리
                cleaned_match = self._clean_text(best_match)
                print(f"사업개요 섹션 추출 완료: {len(cleaned_match)}자")
                print(f"섹션 미리보기: {cleaned_match[:200]}...")
                return cleaned_match
            else:
                print("사업개요 섹션을 찾을 수 없습니다")
                return None
                
        except Exception as e:
            print(f"사업개요 섹션 검색 실패: {str(e)}")
            return None
    
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
            cleaned = re.sub(r'[^\w\s가-힣.,():\-\n/]', '', cleaned)
            
            # 앞뒤 공백 제거
            cleaned = cleaned.strip()
            
            return cleaned
            
        except Exception as e:
            print(f"텍스트 정리 실패: {str(e)}")
            return text

def main():
    """테스트용 메인 함수"""
    print("HWP 파서 테스트")
    print("=" * 50)
    
    # 테스트할 HWP 파일 경로
    test_file = input("테스트할 HWP 파일 경로를 입력하세요: ")
    
    if not test_file or not os.path.exists(test_file):
        print("파일이 존재하지 않습니다.")
        return
    
    parser = HWPParser()
    result = parser.extract_text_from_hwp(test_file)
    
    if result["success"]:
        print("\n✅ HWP 파싱 성공!")
        print(f"📄 파일: {result['hwp_file']}")
        print(f"📝 전체 텍스트: {len(result['full_text'])}자")
        
        if result['business_overview']:
            print(f"🎯 사업개요: {len(result['business_overview'])}자")
            print("\n사업개요 내용:")
            print("-" * 50)
            print(result['business_overview'])
        else:
            print("🎯 사업개요 섹션을 찾을 수 없음")
            print("\n전체 텍스트 미리보기:")
            print("-" * 50)
            print(result['full_text'][:500] + "...")
    else:
        print(f"\n❌ 파싱 실패: {result['error']}")

if __name__ == "__main__":
    main()
