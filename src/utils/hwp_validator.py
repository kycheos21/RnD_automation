#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
HWP 파일 검증 및 선택 유틸리티
공고 관련 파일들 중에서 OLE 시그니처를 검증하여 처리 가능한 파일을 선택
"""

import os
import glob
import olefile
from typing import List, Dict, Optional, Tuple

class HWPValidator:
    """HWP 파일 검증 및 선택 클래스"""
    
    def __init__(self):
        """초기화"""
        self.ole_signature = b'\xd0\xcf\x11\xe0'  # OLE2 시그니처
        self.zip_signature = b'PK\x03\x04'        # ZIP 시그니처
    
    def get_file_signature(self, file_path: str) -> Optional[bytes]:
        """파일의 시그니처(헤더) 확인"""
        try:
            with open(file_path, 'rb') as f:
                return f.read(8)
        except Exception:
            return None
    
    def is_ole_file(self, file_path: str) -> bool:
        """OLE 파일인지 확인"""
        try:
            return olefile.isOleFile(file_path)
        except Exception:
            return False
    
    def is_hwp_file(self, file_path: str) -> bool:
        """HWP 파일인지 확인 (OLE 시그니처 기반)"""
        signature = self.get_file_signature(file_path)
        if not signature:
            return False
        
        # OLE2 시그니처 확인
        return signature.startswith(self.ole_signature)
    
    def get_file_info(self, file_path: str) -> Dict:
        """파일 정보 수집"""
        try:
            info = {
                "file_path": file_path,
                "filename": os.path.basename(file_path),
                "size": os.path.getsize(file_path),
                "signature": self.get_file_signature(file_path),
                "is_ole": self.is_ole_file(file_path),
                "is_hwp": self.is_hwp_file(file_path),
                "signature_hex": None
            }
            
            if info["signature"]:
                info["signature_hex"] = info["signature"].hex()
            
            return info
        except Exception as e:
            return {
                "file_path": file_path,
                "error": str(e),
                "is_hwp": False
            }
    
    def find_announcement_files(self, directory: str, keywords: List[str] = None) -> List[str]:
        """공고 관련 파일들 찾기"""
        if keywords is None:
            keywords = ["공고", "공고문", "announcement"]
        
        all_files = []
        
        # 모든 파일 확장자 확인
        extensions = ["*.hwp", "*.HWP", "*.doc", "*.DOC", "*.docx", "*.DOCX"]
        
        for ext in extensions:
            pattern = os.path.join(directory, ext)
            files = glob.glob(pattern)
            all_files.extend(files)
        
        # 키워드 필터링
        announcement_files = []
        for file_path in all_files:
            filename = os.path.basename(file_path).lower()
            if any(keyword.lower() in filename for keyword in keywords):
                announcement_files.append(file_path)
        
        return announcement_files
    
    def validate_hwp_files(self, file_paths: List[str]) -> List[Dict]:
        """HWP 파일들 검증"""
        validated_files = []
        
        for file_path in file_paths:
            info = self.get_file_info(file_path)
            validated_files.append(info)
        
        return validated_files
    
    def select_valid_hwp_file(self, directory: str, keywords: List[str] = None) -> Optional[Dict]:
        """공고 관련 파일들 중에서 유효한 HWP 파일 선택"""
        try:
            # 1. 공고 관련 파일들 찾기
            announcement_files = self.find_announcement_files(directory, keywords)
            
            if not announcement_files:
                print(f"❌ 공고 관련 파일을 찾을 수 없습니다: {directory}")
                return None
            
            print(f"📁 공고 관련 파일 {len(announcement_files)}개 발견:")
            for file_path in announcement_files:
                print(f"  - {os.path.basename(file_path)}")
            
            # 2. 파일들 검증
            validated_files = self.validate_hwp_files(announcement_files)
            
            # 3. 유효한 HWP 파일들만 필터링
            valid_hwp_files = [f for f in validated_files if f.get("is_hwp", False) and f.get("is_ole", False)]
            
            if not valid_hwp_files:
                print(f"❌ 유효한 HWP 파일이 없습니다:")
                for f in validated_files:
                    if "error" in f:
                        print(f"  - {f['filename']}: 오류 - {f['error']}")
                    else:
                        print(f"  - {f['filename']}: OLE={f['is_ole']}, HWP={f['is_hwp']}, 시그니처={f.get('signature_hex', 'None')}")
                return None
            
            # 4. 가장 적합한 파일 선택 (크기가 가장 큰 파일 우선)
            selected_file = max(valid_hwp_files, key=lambda x: x["size"])
            
            print(f"✅ 선택된 파일: {selected_file['filename']}")
            print(f"   크기: {selected_file['size']:,} bytes")
            print(f"   시그니처: {selected_file.get('signature_hex', 'None')}")
            
            return selected_file
            
        except Exception as e:
            print(f"❌ 파일 선택 중 오류: {str(e)}")
            return None
    
    def get_file_comparison_report(self, file_paths: List[str]) -> str:
        """파일 비교 보고서 생성"""
        if not file_paths:
            return "비교할 파일이 없습니다."
        
        validated_files = self.validate_hwp_files(file_paths)
        
        report = "📊 HWP 파일 비교 보고서\n"
        report += "=" * 50 + "\n\n"
        
        for i, info in enumerate(validated_files, 1):
            if "error" in info:
                report += f"{i}. {info['filename']}: 오류 - {info['error']}\n"
            else:
                report += f"{i}. {info['filename']}\n"
                report += f"   크기: {info['size']:,} bytes\n"
                report += f"   OLE 파일: {'✅' if info['is_ole'] else '❌'}\n"
                report += f"   HWP 파일: {'✅' if info['is_hwp'] else '❌'}\n"
                report += f"   시그니처: {info.get('signature_hex', 'None')}\n"
        
        # 추천 파일
        valid_files = [f for f in validated_files if f.get("is_hwp", False) and f.get("is_ole", False)]
        if valid_files:
            recommended = max(valid_files, key=lambda x: x["size"])
            report += f"\n🎯 추천 파일: {recommended['filename']}\n"
        else:
            report += f"\n⚠️ 유효한 HWP 파일이 없습니다.\n"
        
        return report

def main():
    """테스트용 메인 함수"""
    print("HWP 파일 검증 테스트")
    print("=" * 50)
    
    validator = HWPValidator()
    
    # 테스트 디렉토리
    test_dir = "output/hwp_files"
    
    if not os.path.exists(test_dir):
        print(f"❌ 테스트 디렉토리가 없습니다: {test_dir}")
        return
    
    # 공고 관련 파일들 찾기
    announcement_files = validator.find_announcement_files(test_dir)
    print(f"\n📁 공고 관련 파일 {len(announcement_files)}개 발견")
    
    # 비교 보고서 생성
    if announcement_files:
        report = validator.get_file_comparison_report(announcement_files)
        print(f"\n{report}")
    
    # 유효한 파일 선택
    selected = validator.select_valid_hwp_file(test_dir)
    if selected:
        print(f"\n🎯 최종 선택: {selected['file_path']}")
    else:
        print(f"\n❌ 유효한 HWP 파일을 찾을 수 없습니다.")

if __name__ == "__main__":
    main()
