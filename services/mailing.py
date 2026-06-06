import os
import smtplib
from email.message import EmailMessage
from datetime import datetime, timezone
from flask import current_app # For Fetching USER, APP_PASS
from dotenv import load_dotenv

load_dotenv()

# Config
SMTP_HOST  = os.environ.get('SMTP_HOST', 'smtp.gmail.com')
SMTP_PORT  = os.environ.get('SMTP_PORT', 587)
SMTP_USER  = os.environ.get('SMTP_USER')
SMTP_PASS  = os.environ.get('SMTP_PASS')


def send_mail(to_addr: str, subject: str, body_html: str, attachment: bytes = None, attachment_name: str = None):
    """
    Send an email alert.

    Args:
        to_addr:         Recipient email address
        subject:         Email subject line
        body_html:       HTML body content
        attachment:      Optional file bytes to attach
        attachment_name: Filename for the attachment
    """
    msg = EmailMessage()
    msg["From"]    = f"SilentHook <{SMTP_USER}>"
    msg["To"]      = to_addr
    msg["Subject"] = subject

    # Plain text fallback + HTML body
    msg.set_content("You have a new DBBD alert. Please view this in an HTML-capable email client.")
    msg.add_alternative(body_html, subtype="html")

    # Optional attachment
    if attachment and attachment_name:
        msg.add_attachment(
            attachment,
            maintype="application",
            subtype="octet-stream",
            filename=attachment_name
        )

    try:
        with smtplib.SMTP(SMTP_HOST, SMTP_PORT) as server:
            server.starttls()
            server.login(SMTP_USER, SMTP_PASS)
            server.send_message(msg)
    except smtplib.SMTPException as e:
        print(f"[MAIL ERROR] Failed to send to {to_addr}: {e}")
        raise

    except Exception as e:
        print("Error", e)
        raise



_alert_dict = {'user_agent': 'curl/7.88.1', 'event_time': '2026-02-06T11:59:25', 'id': 13, 'token': '2d37b8db-0490-4b0d-9f8a-89f4f3c0ab8a', 'source_ip': '127.0.0.1'}
_fim_dict = {
    'id': 10,
	"user": "Administrator" ,
	"path" : "C:\\Program Files (x86)\\confidential" ,
	"access" : "0x500" ,
	"process" : "C:\\Program Files (x86)\\powershell\\powershell.exe",
	"event_time" : "2026-05-07 01:32:21" 
}


_dst_mail = "test@gmail.com"
_bait_type = "PPTX"
_reminder = "Bait Triggered"

from datetime import datetime, timezone


def processor(dst_mail: str, bait_type: str, reminder: str, alert_dict: dict) -> str:

    alert_details = ""
    alert_id  = alert_dict.get("id", "N/A")

    event_time = alert_dict.get('event_time')
    event_time = f"{datetime.fromisoformat(event_time).replace(tzinfo=timezone.utc)} UTC"
    alert_dict['event_time'] = event_time

    alert_dict.pop('id')

    BASE_URL = current_app.config['CALLBACK_URL'] # Fetch current url to append in email 
    
    for key, value in alert_dict.items():
        key = key.replace("_", " ")

        tab = f"""
    <tr>
        <td style="padding:0 0 12px;">
            <table width="100%" cellpadding="12" cellspacing="0"
                    style="background:#f6f8fa;border:1px solid #d0d7de;border-radius:8px;">
                <tr>
                    <td width="40" valign="middle" style="padding-right:0;">
                        <img src="https://img.icons8.com/?size=24&id=31657&format=png"
                            alt="" style="width:28px;height:28px;display:block;opacity:0.5;">
                    </td>
                    <td valign="middle">
                        <p style="margin:0 0 2px;font-size:11px;font-weight:600;
                                    letter-spacing:0.1em;text-transform:uppercase;color:#57606a;">
                            {key}
                        </p>
                        <p style="margin:0;font-size:14px;font-weight:500;color:#1f2328;">
                            {value}
                        </p>
                    </td>
                </tr>
            </table>
        </td>
    </tr>
    """
        alert_details += tab

    html = f"""
<!DOCTYPE html>
<html lang="en">
<head><meta charset="UTF-8"><meta name="viewport" content="width=device-width, initial-scale=1.0"></head>
<body style="margin:0;padding:0;background:#f6f8fa;font-family:'Segoe UI',Arial,sans-serif;">

  <table width="100%" cellpadding="0" cellspacing="0" style="background:#f6f8fa;padding:40px 0;">
    <tr>
      <td align="center">
        <table width="520" cellpadding="0" cellspacing="0"
               style="background:#ffffff;border:1px solid #d0d7de;border-radius:12px;
                      overflow:hidden;max-width:520px;width:100%;">

          <!-- Header -->
          <tr>
            <td style="background:#0d1117;padding:0;
                    border-radius:12px 12px 0 0;
                    border-bottom:2px solid #f97316;">
                <img src="https://raw.githubusercontent.com/BENARD256/SilentHook/main/static/images/email/header_mail.png"
                    alt="SilentHook"
                    width="520" height="auto"
                    style="display:block;width:100%;max-width:520px;">
            </td>
          </tr>

          <!-- Alert banner -->
          <tr>
            <td style="padding:32px 32px 8px;text-align:center;">

              <img src="https://img.icons8.com/?size=80&id=MexKOWjN2DR1&format=png"
                   alt="Warning"
                   width="68" height="68"
                   style="display:block;margin:0 auto 16px;">

              <h1 style="margin:0 0 8px;font-size:20px;font-weight:700;color:#1f2328;">
                Your Bait Was Triggered
              </h1>

              <p style="margin:0;font-size:13px;color:#57606a;line-height:1.6;">
                A deception token has been accessed.<br>
                Immediate review is recommended.
              </p>

            </td>
          </tr>

          <!-- Divider -->
          <tr>
            <td style="padding:24px 32px 16px;">
              <div style="height:1px;background:#d0d7de;"></div>
            </td>
          </tr>

        <!-- Bait Type -->
        <tr>
            <td style="padding:0 32px 12px;">
                <table width="100%" cellpadding="12" cellspacing="0"
                        style="background:#f6f8fa;border:1px solid #d0d7de;border-radius:8px;">
                    <tr>
                        <td width="40" valign="middle" style="padding-right:0;">
                            <img src="https://img.icons8.com/?size=64&id=9SPgCX6EQMCK&format=png"
                                alt="" style="width:28px;height:28px;display:block;opacity:0.5;">
                        </td>
                        <td valign="middle">
                            <p style="margin:0 0 2px;font-size:11px;font-weight:600;
                                        letter-spacing:0.1em;text-transform:uppercase;color:#57606a;">
                                Bait Type
                            </p>
                            <p style="margin:0;font-size:14px;font-weight:500;color:#1f2328;">
                                {bait_type}
                            </p>
                        </td>
                    </tr>
                </table>
            </td>
        </tr>

          <!-- Reminder -->
          <tr>
                <td style="padding:0 32px 12px;">
                    <table width="100%" cellpadding="12" cellspacing="0"
                            style="background:#f6f8fa;border:1px solid #d0d7de;border-radius:8px;">
                        <tr>
                            <td width="40" valign="middle" style="padding-right:0;">
                                <img src="https://img.icons8.com/?size=64&id=gnsB3xE8Q5Et&format=png"
                                    alt="" style="width:28px;height:28px;display:block;opacity:0.5;">
                            </td>
                            <td valign="middle">
                                <p style="margin:0 0 2px;font-size:11px;font-weight:600;
                                            letter-spacing:0.1em;text-transform:uppercase;color:#57606a;">
                                    Reminder
                                </p>
                                <p style="margin:0;font-size:14px;font-weight:500;color:#1f2328;">
                                    {reminder}
                                </p>
                            </td>
                        </tr>
                    </table>
                </td>
          </tr>

          <!-- Dynamic alert details -->
          <tr>
            <td style="padding:0 32px;">
              <table width="100%" cellpadding="0" cellspacing="0">
                {alert_details}
              </table>
            </td>
          </tr>

        <!-- CTA Buttons -->
        <tr>
            <td style="padding:20px 32px 8px;text-align:center;
                        background-color:#ffffff;">
                <a href="{BASE_URL+'/auth/login?next=/analytics'}"
                    style="display:inline-block;padding:10px 24px;
                            background-color:#f97316;border-radius:6px;
                            font-size:13px;font-weight:600;color:#ffffff;
                            text-decoration:none;margin:0 4px 8px;">
                    Alerts Analytics
                </a>
                <a href="{BASE_URL+'/auth/login?next=/triggers'}"
                    style="display:inline-block;padding:10px 24px;
                            background-color:#ffffff;border:1px solid #d0d7de;
                            border-radius:6px;font-size:13px;font-weight:600;
                            color:#24292f;text-decoration:none;margin:0 4px 8px;">
                    Manage Baits
                </a>
            </td>
        </tr>

          <!-- Footer -->
          <tr>
            <td style="padding:24px 32px 32px;text-align:center;">
              <div style="height:1px;background:#d0d7de;margin-bottom:20px;"></div>
              <p style="margin:0;font-size:11px;color:#57606a;line-height:1.6;">
                This alert was sent to <span style="color:#1f2328;font-weight:600;">{dst_mail}</span>
                because a bait token associated with your account was triggered.<br>
              </p>
            </td>
          </tr>

        </table>
      </td>
    </tr>
  </table>

</body>
</html>
"""
    return html


def mailer(dst_mail: str, bait_type:str, reminder: str, alert_dict: dict):
    
    body_html= processor(dst_mail=dst_mail,bait_type=bait_type, reminder=reminder,alert_dict=alert_dict)

    try:
        return send_mail(
            to_addr=dst_mail,
            subject="Alert Triggered",
            body_html=body_html
        )
    except Exception as e:
        return  f"Error Occured: {e}"



if __name__ == "__main__":
    mailer(dst_mail=_dst_mail,bait_type=_bait_type, reminder=_reminder, alert_dict=_alert_dict)
