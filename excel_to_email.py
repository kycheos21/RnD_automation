#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Excel to Email 발송기
최신 Excel 파일을 찾아서 이메일로 발송
"""

import os
import sys
import glob
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
from datetime import datetime
from dotenv import load_dotenv

# UTF-8 인코딩 설정
if sys.platform == 'win32':
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')

# .env 파일 로드
load_dotenv()

def find_latest_excel():
    """최신 Excel 파일 찾기"""
    try:
        excel_files = glob.glob("output/NTIS_신규공고_*.xlsx")
        
        if not excel_files:
            print("❌ Excel 파일을 찾을 수 없습니다.")
            return None
        
        # 가장 최신 파일 선택
        latest_file = max(excel_files, key=os.path.getmtime)
        print(f"📎 첨부할 파일: {os.path.basename(latest_file)}")
        
        return latest_file
        
    except Exception as e:
        print(f"❌ Excel 파일 찾기 실패: {str(e)}")
        return None

def send_email(excel_file, announcement_count):
    """이메일 발송"""
    try:
        print("\n📧 이메일 발송 준비 중...")
        
        # 이메일 설정 로드
        smtp_server = os.getenv("SMTP_SERVER", "outbound.daouoffice.com")
        smtp_port_str = os.getenv("SMTP_PORT", "25")
        smtp_port = int(smtp_port_str) if smtp_port_str else 25
        email_sender = os.getenv("EMAIL_SENDER")
        email_password = os.getenv("EMAIL_PASSWORD")
        email_receiver = os.getenv("EMAIL_RECEIVER")
        
        if not all([email_sender, email_password, email_receiver]):
            print("❌ .env 파일에 이메일 설정이 없습니다.")
            print("   필요한 설정: EMAIL_SENDER, EMAIL_PASSWORD, EMAIL_RECEIVER")
            return False
        
        print(f"   발신: {email_sender}")
        print(f"   수신: {email_receiver}")
        print(f"   서버: {smtp_server}:{smtp_port}")
        
        # 이메일 메시지 생성
        msg = MIMEMultipart()
        msg['From'] = email_sender
        msg['To'] = email_receiver
        msg['Subject'] = f"NTIS 신규 공고 알림 ({datetime.now().strftime('%Y-%m-%d')})"
        
        # 이메일 본문
        body = f"""
안녕하세요,

NTIS에서 신규 공고 {announcement_count}건이 발견되었습니다.

📋 신규 공고 상세 정보는 첨부된 Excel 파일을 확인해주세요.

---
자동 발송 시스템
생성 시간: {datetime.now().strftime('%Y년 %m월 %d일 %H:%M:%S')}
        """
        
        msg.attach(MIMEText(body, 'plain', 'utf-8'))
        
        # Excel 파일 첨부
        print("   Excel 파일 첨부 중...")
        filename = os.path.basename(excel_file)
        
        with open(excel_file, 'rb') as f:
            part = MIMEBase('application', 'vnd.openxmlformats-officedocument.spreadsheetml.sheet')
            part.set_payload(f.read())
            encoders.encode_base64(part)
            
            # 파일명을 RFC 2231 형식으로 인코딩 (한글 파일명 지원)
            from email.utils import encode_rfc2231
            encoded_filename = encode_rfc2231(filename, 'utf-8')
            part.add_header(
                'Content-Disposition',
                'attachment',
                filename=('utf-8', '', filename)
            )
            msg.attach(part)
        
        # SMTP 서버 연결 및 전송
        print("   SMTP 서버 연결 중...")
        
        # SSL 포트(465) 사용
        server = smtplib.SMTP_SSL(smtp_server, smtp_port)
        
        print("   로그인 중...")
        server.login(email_sender, email_password)
        
        print("   이메일 전송 중...")
        server.send_message(msg)
        
        server.quit()
        
        print("✅ 이메일 발송 완료!")
        return True
        
    except smtplib.SMTPAuthenticationError:
        print("❌ 이메일 인증 실패!")
        print("   - 이메일 주소와 비밀번호를 확인해주세요.")
        print("   - DaouOffice 계정 비밀번호가 맞는지 확인해주세요.")
        return False
        
    except smtplib.SMTPException as e:
        print(f"❌ SMTP 오류: {str(e)}")
        return False
        
    except Exception as e:
        print(f"❌ 이메일 발송 실패: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

def count_announcements():
    """new_data.json에서 공고 개수 확인"""
    try:
        import json
        with open("output/new_data.json", 'r', encoding='utf-8') as f:
            data = json.load(f)
        return len(data)
    except:
        return 0

def main():
    """메인 함수"""
    print("=" * 60)
    print("Excel to Email 발송기")
    print("=" * 60)
    
    # 1. 최신 Excel 파일 찾기
    excel_file = find_latest_excel()
    if not excel_file:
        return
    
    # 2. 공고 개수 확인
    announcement_count = count_announcements()
    print(f"📊 신규 공고 개수: {announcement_count}건")
    
    if announcement_count == 0:
        print("\n⚠️ 신규 공고가 없어 이메일을 발송하지 않습니다.")
        return
    
    # 3. 이메일 발송
    success = send_email(excel_file, announcement_count)
    
    if success:
        print(f"\n🎉 전송 완료!")
    else:
        print("\n❌ 전송 실패!")

if __name__ == "__main__":
    main()

