#!/usr/bin/env python3
"""
Firecrawl API 연결 테스트 스크립트
"""

import os
from dotenv import load_dotenv
from firecrawl import FirecrawlApp

def test_firecrawl_connection():
    """Firecrawl API 연결 테스트"""
    
    # 환경변수 로드 시도
    try:
        load_dotenv()
    except:
        print("⚠️ .env 파일 로드 실패, 직접 설정된 환경변수 사용")
    
    # API 키 확인 (직접 설정도 시도)
    api_key = os.getenv('FIRECRAWL_API_KEY')
    if not api_key:
        # 직접 설정 시도
        api_key = "fc-6c348fc20f0045a2bf8601c1d99a559c"
        print("💡 직접 설정된 API 키 사용")
    
    if not api_key:
        print("❌ FIRECRAWL_API_KEY를 찾을 수 없습니다.")
        return False
    
    try:
        # Firecrawl 앱 초기화
        app = FirecrawlApp(api_key=api_key)
        print("✅ Firecrawl 클라이언트 초기화 성공")
        
        # 간단한 테스트 - 단일 페이지 크롤링
        test_url = "https://example.com"
        print(f"🔍 테스트 URL 크롤링 시도: {test_url}")
        
        # 크롤링 실행
        result = app.scrape(test_url)
        
        if result and hasattr(result, 'markdown'):
            print("✅ Firecrawl API 연결 테스트 성공!")
            print(f"📄 크롤링된 콘텐츠 길이: {len(result.markdown)} 문자")
            print(f"🔗 URL: {result.metadata.url if result.metadata else 'N/A'}")
            print(f"📋 제목: {result.metadata.title if result.metadata else 'N/A'}")
            print(f"💳 사용된 크레딧: {result.metadata.credits_used if result.metadata else 'N/A'}")
            return True
        else:
            print("⚠️  크롤링 결과가 예상과 다릅니다.")
            print(f"결과: {result}")
            return False
            
    except Exception as e:
        print(f"❌ Firecrawl API 연결 실패: {str(e)}")
        print("💡 API 키가 올바른지 확인해주세요.")
        return False

def main():
    """메인 함수"""
    print("🚀 Firecrawl API 연결 테스트 시작")
    print("=" * 50)
    
    success = test_firecrawl_connection()
    
    print("=" * 50)
    if success:
        print("🎉 모든 테스트가 성공적으로 완료되었습니다!")
        print("📝 이제 NTIS 크롤링 프로젝트를 시작할 수 있습니다.")
    else:
        print("❌ 테스트 실패. 설정을 다시 확인해주세요.")

if __name__ == "__main__":
    main()
