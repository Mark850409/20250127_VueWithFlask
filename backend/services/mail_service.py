from flask_mail import Message, Mail
from flask import current_app, render_template_string

mail = Mail()

class MailService:
    @staticmethod
    def send_reset_password_email(user, token):
        """發送重設密碼郵件"""
        frontend_url = current_app.config.get('FRONTEND_URL', 'http://localhost:5173')
        reset_url = f"{frontend_url}/reset-password/{token}"
        
        # HTML 郵件模板
        html_content = '''
        <div style="max-width: 600px; margin: 0 auto; padding: 20px; font-family: Arial, sans-serif;">
            <h2 style="color: #4F46E5;">重設密碼請求</h2>
            <p>親愛的 {{ username }}：</p>
            <p>我們收到了您重設密碼的請求。請點擊下方連結重設您的密碼：</p>
            <p style="margin: 25px 0;">
                <a href="{{ reset_url }}" 
                   style="background-color: #4F46E5; color: white; padding: 10px 20px; 
                          text-decoration: none; border-radius: 5px;">
                    重設密碼
                </a>
            </p>
            <p>此連結將在{{ expire_time }}分鐘後失效。</p>
            <p>如果您沒有要求重設密碼，請忽略此郵件。</p>
            <p>謝謝！</p>
        </div>
        '''
        
        # 渲染模板
        html = render_template_string(
            html_content,
            username=user.username,
            reset_url=reset_url,
            expire_time=current_app.config['RESET_TOKEN_EXPIRE_VALUE']
        )
        
        # 創建郵件
        msg = Message(
            '重設密碼請求',
            recipients=[user.email],
            html=html
        )
        
        # 發送郵件
        mail.send(msg) 