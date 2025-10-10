#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Claude API 기반 사업공고 요약기
Anthropic Claude를 사용하여 사업개요를 구조화된 요약으로 변환
"""

import anthropic
import os
import time
import re
from typing import Optional, Dict
import json
from dotenv import load_dotenv

# .env 파일 로드
load_dotenv()

class ClaudeSummarizer:
    """Claude API 기반 사업공고 요약기"""
    
    def __init__(self, api_key: Optional[str] = None):
        """
        초기화
        
        Args:
            api_key: Claude API 키 (없으면 환경변수에서 가져오기)
        """
        # API 키 설정
        self.api_key = api_key or os.getenv("ANTHROPIC_API_KEY")
        
        if not self.api_key:
            print("⚠️ Claude API 키가 설정되지 않았습니다.")
            print("환경변수 ANTHROPIC_API_KEY를 설정하거나 직접 전달해주세요.")
            self.client = None
        else:
            try:
                self.client = anthropic.Anthropic(api_key=self.api_key)
                print("✅ Claude API 클라이언트 초기화 완료")
            except Exception as e:
                print(f"❌ Claude API 클라이언트 초기화 실패: {str(e)}")
                self.client = None
        
        # 요약 설정
        self.model = "claude-3-haiku-20240307"  # 빠르고 비용 효율적
        self.max_tokens = 1000  # 요약 최대 길이
        self.temperature = 0.3  # 일관성 있는 요약을 위해 낮은 값
        
        # 토큰 제한 (입력 텍스트)
        self.max_input_chars = 8000  # 약 2000 토큰
        
        print("Claude 요약기 초기화 완료")
    
    def _create_summary_prompt(self, business_overview: str, announcement_title: str = "") -> str:
        """요약 프롬프트 생성"""
        
        prompt = f"""다음은 정부 R&D 사업공고의 사업개요입니다. 이 내용을 명확하고 구조화된 형태로 요약해주세요.

공고제목: {announcement_title}

요약 요구사항:
1. 10-20줄 분량으로 작성
2. 다음 구조로 정리:
   - 사업목적: 이 사업이 추진되는 핵심 목적
   - 지원내용: 구체적으로 무엇을 지원하는지
   - 지원규모: 예산, 기간, 선정규모 등
   - 신청대상: 누가 신청할 수 있는지
   - 주요특징: 이 사업만의 특별한 점

3. 전문용어는 이해하기 쉽게 설명
4. 핵심 내용만 간결하게 정리
5. 불필요한 절차적 내용은 제외

사업개요 원문:
{business_overview}

위 내용을 바탕으로 구조화된 요약을 작성해주세요."""

        return prompt
    
    def _clean_input_text(self, text: str) -> str:
        """입력 텍스트 전처리"""
        if not text:
            return ""
        
        # 길이 제한
        if len(text) > self.max_input_chars:
            text = text[:self.max_input_chars] + "..."
            print(f"입력 텍스트가 길어서 {self.max_input_chars}자로 제한됨")
        
        # 불필요한 문자 정리
        text = re.sub(r'\s+', ' ', text)  # 연속 공백 제거
        text = re.sub(r'\n{3,}', '\n\n', text)  # 연속 줄바꿈 제한
        text = text.strip()
        
        return text
    
    def _parse_summary_response(self, response_text: str) -> Dict:
        """Claude 응답을 구조화된 형태로 파싱"""
        try:
            # 기본 구조
            parsed = {
                "사업목적": "",
                "지원내용": "",
                "지원규모": "",
                "신청대상": "",
                "주요특징": "",
                "전체요약": response_text.strip()
            }
            
            # 구조화된 응답에서 각 섹션 추출
            sections = ["사업목적", "지원내용", "지원규모", "신청대상", "주요특징"]
            
            for section in sections:
                # 패턴: "- 사업목적: 내용" 또는 "사업목적: 내용"
                patterns = [
                    rf"[-•]\s*{section}:\s*([^\n]+(?:\n(?![-•]\s*\w+:)[^\n]+)*)",
                    rf"{section}:\s*([^\n]+(?:\n(?!\w+:)[^\n]+)*)"
                ]
                
                for pattern in patterns:
                    match = re.search(pattern, response_text, re.MULTILINE)
                    if match:
                        content = match.group(1).strip()
                        parsed[section] = content
                        break
            
            return parsed
            
        except Exception as e:
            print(f"응답 파싱 실패: {str(e)}")
            return {
                "사업목적": "",
                "지원내용": "",
                "지원규모": "",
                "신청대상": "",
                "주요특징": "",
                "전체요약": response_text.strip()
            }
    
    def summarize_business_overview(self, business_overview: str, announcement_title: str = "") -> Dict:
        """사업개요 요약 실행"""
        try:
            if not self.client:
                return {
                    "success": False,
                    "error": "Claude API 클라이언트가 초기화되지 않음",
                    "summary": None
                }
            
            if not business_overview or len(business_overview.strip()) < 50:
                return {
                    "success": False,
                    "error": "요약할 내용이 너무 짧거나 없음",
                    "summary": None
                }
            
            print(f"Claude API 요약 시작...")
            print(f"입력 텍스트: {len(business_overview)}자")
            
            # 입력 텍스트 전처리
            cleaned_text = self._clean_input_text(business_overview)
            
            # 프롬프트 생성
            prompt = self._create_summary_prompt(cleaned_text, announcement_title)
            
            # Claude API 호출
            start_time = time.time()
            
            response = self.client.messages.create(
                model=self.model,
                max_tokens=self.max_tokens,
                temperature=self.temperature,
                messages=[
                    {
                        "role": "user",
                        "content": prompt
                    }
                ]
            )
            
            elapsed_time = time.time() - start_time
            
            # 응답 처리
            if response.content and len(response.content) > 0:
                summary_text = response.content[0].text
                
                # 구조화된 파싱
                parsed_summary = self._parse_summary_response(summary_text)
                
                # 토큰 사용량 정보 (있는 경우)
                input_tokens = getattr(response.usage, 'input_tokens', 0)
                output_tokens = getattr(response.usage, 'output_tokens', 0)
                
                print(f"✅ Claude API 요약 완료!")
                print(f"   처리 시간: {elapsed_time:.1f}초")
                print(f"   입력 토큰: {input_tokens:,}")
                print(f"   출력 토큰: {output_tokens:,}")
                print(f"   요약 길이: {len(summary_text)}자")
                
                return {
                    "success": True,
                    "summary": parsed_summary,
                    "raw_response": summary_text,
                    "metadata": {
                        "model": self.model,
                        "input_tokens": input_tokens,
                        "output_tokens": output_tokens,
                        "processing_time": elapsed_time,
                        "input_length": len(business_overview),
                        "output_length": len(summary_text)
                    }
                }
            else:
                return {
                    "success": False,
                    "error": "Claude API에서 빈 응답을 받음",
                    "summary": None
                }
                
        except anthropic.RateLimitError as e:
            print(f"⚠️ Claude API 요청 한도 초과: {str(e)}")
            return {
                "success": False,
                "error": f"API 요청 한도 초과: {str(e)}",
                "summary": None,
                "retry_after": 60  # 60초 후 재시도 권장
            }
            
        except anthropic.APIError as e:
            print(f"❌ Claude API 오류: {str(e)}")
            return {
                "success": False,
                "error": f"Claude API 오류: {str(e)}",
                "summary": None
            }
            
        except Exception as e:
            print(f"❌ 요약 처리 중 오류: {str(e)}")
            return {
                "success": False,
                "error": f"요약 처리 오류: {str(e)}",
                "summary": None
            }
    
    def create_fallback_summary(self, business_overview: str, max_length: int = 500) -> str:
        """API 실패 시 대체 요약 생성 (단순 텍스트 자르기)"""
        try:
            if not business_overview:
                return "요약할 내용이 없습니다."
            
            # 첫 번째 문단이나 핵심 부분 추출
            lines = business_overview.split('\n')
            summary_lines = []
            current_length = 0
            
            for line in lines:
                line = line.strip()
                if line and current_length + len(line) < max_length:
                    summary_lines.append(line)
                    current_length += len(line)
                elif current_length > 100:  # 최소한의 내용 확보
                    break
            
            fallback_summary = ' '.join(summary_lines)
            if len(fallback_summary) > max_length:
                fallback_summary = fallback_summary[:max_length] + "..."
            
            return fallback_summary or business_overview[:max_length] + "..."
            
        except Exception as e:
            print(f"대체 요약 생성 실패: {str(e)}")
            return business_overview[:200] + "..." if business_overview else "요약 생성 실패"

def main():
    """테스트용 메인 함수"""
    print("Claude 요약기 테스트")
    print("=" * 50)
    
    # API 키 확인
    api_key = os.getenv("ANTHROPIC_API_KEY")
    if not api_key:
        print("❌ ANTHROPIC_API_KEY 환경변수가 설정되지 않았습니다.")
        print("API 키를 설정한 후 다시 실행해주세요.")
        return
    
    # 요약기 생성
    summarizer = ClaudeSummarizer()
    
    # 테스트 텍스트
    test_text = """
    사업개요
    본 사업은 AI 기술의 해외 우수 인재를 국내로 유치하여 AI 분야의 기술 경쟁력을 강화하고자 합니다.
    최고급 AI 해외인재를 대상으로 연구개발비, 정착지원금, 연구환경 조성비 등을 종합적으로 지원합니다.
    지원규모는 총 100억원이며, 개인당 최대 5억원까지 3년간 지원됩니다.
    신청대상은 AI 분야 박사학위 소지자 또는 동등 경력자로, 해외 거주 경험이 있는 자에 한합니다.
    """
    
    # 요약 실행
    result = summarizer.summarize_business_overview(
        business_overview=test_text,
        announcement_title="2025년도 최고급 AI 해외인재 유치지원 사업"
    )
    
    if result["success"]:
        print("✅ 요약 성공!")
        summary = result["summary"]
        
        print("\n📋 구조화된 요약:")
        print("-" * 30)
        for key, value in summary.items():
            if key != "전체요약" and value:
                print(f"{key}: {value}")
        
        print(f"\n📄 전체 요약:")
        print("-" * 30)
        print(summary["전체요약"])
        
        print(f"\n📊 메타데이터:")
        metadata = result["metadata"]
        print(f"모델: {metadata['model']}")
        print(f"처리시간: {metadata['processing_time']:.1f}초")
        print(f"토큰 사용: {metadata['input_tokens']:,} → {metadata['output_tokens']:,}")
        
    else:
        print(f"❌ 요약 실패: {result['error']}")

if __name__ == "__main__":
    main()
