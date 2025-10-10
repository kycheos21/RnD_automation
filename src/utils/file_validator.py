#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
통합 파일 검증 및 선택 유틸리티
HWP, PDF, HWPX 등 다양한 파일 형식을 지원하는 통합 검증기
"""

import os
import glob
from typing import List, Dict, Optional
from .hwp_validator import HWPValidator
from .pdf_validator import PDFValidator

class FileValidator:
    """통합 파일 검증 및 선택 클래스"""
    
    def __init__(self):
        """초기화"""
        self.hwp_validator = HWPValidator()
        self.pdf_validator = PDFValidator()
        print("통합 파일 검증기 초기화 완료")
    
    def find_announcement_files(self, directory: str, keywords: List[str] = None) -> Dict[str, List[str]]:
        """공고 관련 파일들을 형식별로 찾기"""
        if keywords is None:
            keywords = ["공고", "공고문", "announcement"]
        
        result = {
            "hwp": [],
            "pdf": [],
            "hwpx": [],
            "doc": [],
            "docx": []
        }
        
        # 각 파일 형식별로 검색
        file_patterns = {
            "hwp": ["*.hwp", "*.HWP"],
            "pdf": ["*.pdf", "*.PDF"],
            "hwpx": ["*.hwpx", "*.HWPX"],
            "doc": ["*.doc", "*.DOC"],
            "docx": ["*.docx", "*.DOCX"]
        }
        
        for file_type, patterns in file_patterns.items():
            for pattern in patterns:
                full_pattern = os.path.join(directory, pattern)
                files = glob.glob(full_pattern)
                
                # 키워드 필터링
                for file_path in files:
                    filename = os.path.basename(file_path).lower()
                    if any(keyword.lower() in filename for keyword in keywords):
                        result[file_type].append(file_path)
        
        return result
    
    def select_valid_file(self, directory: str, keywords: List[str] = None, 
                         preferred_formats: List[str] = None) -> Optional[Dict]:
        """공고 관련 파일들 중에서 유효한 파일 선택 (우선순위 기반)"""
        
        if preferred_formats is None:
            preferred_formats = ["hwp", "pdf", "hwpx", "doc", "docx"]
        
        try:
            print(f"🔍 공고 관련 파일 검색 중...")
            
            # 1. 모든 형식의 파일들 찾기
            all_files = self.find_announcement_files(directory, keywords)
            
            total_files = sum(len(files) for files in all_files.values())
            if total_files == 0:
                print(f"❌ 공고 관련 파일을 찾을 수 없습니다: {directory}")
                return None
            
            print(f"📁 총 {total_files}개 파일 발견:")
            for file_type, files in all_files.items():
                if files:
                    print(f"  - {file_type.upper()}: {len(files)}개")
            
            # 2. 우선순위에 따라 파일 검증 및 선택
            for file_type in preferred_formats:
                if file_type in all_files and all_files[file_type]:
                    print(f"\n🔍 {file_type.upper()} 파일 검증 중...")
                    
                    selected_file = self._validate_and_select_by_type(file_type, all_files[file_type])
                    
                    if selected_file:
                        selected_file["file_type"] = file_type
                        print(f"✅ {file_type.upper()} 파일 선택 완료")
                        return selected_file
                    else:
                        print(f"❌ 유효한 {file_type.upper()} 파일이 없습니다")
            
            print("❌ 모든 형식의 파일 검증 실패")
            return None
            
        except Exception as e:
            print(f"❌ 파일 선택 중 오류: {str(e)}")
            return None
    
    def _validate_and_select_by_type(self, file_type: str, file_paths: List[str]) -> Optional[Dict]:
        """파일 형식별 검증 및 선택"""
        try:
            if file_type == "hwp":
                return self.hwp_validator.select_valid_hwp_file(
                    os.path.dirname(file_paths[0]), ["공고", "공고문"]
                )
            elif file_type == "pdf":
                return self.pdf_validator.select_valid_pdf_file(
                    os.path.dirname(file_paths[0]), ["공고", "공고문"]
                )
            elif file_type == "hwpx":
                # HWPX는 HWP와 유사한 방식으로 처리
                return self.hwp_validator.select_valid_hwp_file(
                    os.path.dirname(file_paths[0]), ["공고", "공고문"]
                )
            elif file_type in ["doc", "docx"]:
                # DOC/DOCX는 기본 검증만 수행
                return self._select_largest_file(file_paths)
            else:
                return None
                
        except Exception as e:
            print(f"❌ {file_type.upper()} 파일 검증 실패: {str(e)}")
            return None
    
    def _select_largest_file(self, file_paths: List[str]) -> Optional[Dict]:
        """가장 큰 파일 선택 (기본 검증)"""
        try:
            largest_file = None
            largest_size = 0
            
            for file_path in file_paths:
                try:
                    size = os.path.getsize(file_path)
                    if size > largest_size:
                        largest_size = size
                        largest_file = {
                            "file_path": file_path,
                            "filename": os.path.basename(file_path),
                            "size": size
                        }
                except Exception:
                    continue
            
            if largest_file:
                print(f"✅ 가장 큰 파일 선택: {largest_file['filename']}")
                print(f"   크기: {largest_file['size']:,} bytes")
            
            return largest_file
            
        except Exception as e:
            print(f"❌ 파일 선택 실패: {str(e)}")
            return None
    
    def get_comprehensive_report(self, directory: str, keywords: List[str] = None) -> str:
        """포괄적인 파일 보고서 생성"""
        try:
            all_files = self.find_announcement_files(directory, keywords)
            
            report = "📊 통합 파일 검증 보고서\n"
            report += "=" * 60 + "\n\n"
            
            total_files = 0
            for file_type, files in all_files.items():
                if files:
                    total_files += len(files)
                    report += f"📁 {file_type.upper()} 파일 ({len(files)}개):\n"
                    
                    # 각 파일의 기본 정보 표시
                    for file_path in files:
                        try:
                            size = os.path.getsize(file_path)
                            report += f"  - {os.path.basename(file_path)} ({size:,} bytes)\n"
                        except Exception:
                            report += f"  - {os.path.basename(file_path)} (크기 확인 실패)\n"
                    report += "\n"
            
            if total_files == 0:
                report += "❌ 공고 관련 파일이 없습니다.\n"
            else:
                report += f"📊 총 {total_files}개 파일 발견\n\n"
                
                # 추천 파일 선택
                recommended = self.select_valid_file(directory, keywords)
                if recommended:
                    report += f"🎯 추천 파일: {recommended['filename']}\n"
                    report += f"   형식: {recommended.get('file_type', 'Unknown').upper()}\n"
                    report += f"   크기: {recommended['size']:,} bytes\n"
                else:
                    report += "⚠️ 유효한 파일을 찾을 수 없습니다.\n"
            
            return report
            
        except Exception as e:
            return f"❌ 보고서 생성 실패: {str(e)}"

def main():
    """테스트용 메인 함수"""
    print("통합 파일 검증기 테스트")
    print("=" * 50)
    
    validator = FileValidator()
    
    # 테스트 디렉토리
    test_dir = "output/files"
    
    if not os.path.exists(test_dir):
        print(f"❌ 테스트 디렉토리가 없습니다: {test_dir}")
        return
    
    # 포괄적인 보고서 생성
    report = validator.get_comprehensive_report(test_dir)
    print(report)
    
    # 파일 선택 테스트
    selected = validator.select_valid_file(test_dir)
    if selected:
        print(f"\n🎯 최종 선택된 파일:")
        print(f"   경로: {selected['file_path']}")
        print(f"   형식: {selected.get('file_type', 'Unknown')}")
        print(f"   크기: {selected['size']:,} bytes")
    else:
        print(f"\n❌ 유효한 파일을 찾을 수 없습니다.")

if __name__ == "__main__":
    main()
