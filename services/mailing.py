import smtplib
from email.message import EmailMessage
from datetime import datetime, timezone

# Config
SMTP_HOST  = "smtp.gmail.com"
SMTP_PORT  = 587
SMTP_USER  = "benardtera2@gmail.com"
SMTP_PASS  = "rsfrmpwfqorjgvjq"


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
    msg["From"]    = SMTP_USER
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


_dst_mail = "ab0779672750@gmail.com"
_bait_type = "PPTX"
_reminder = "Bait Triggered"


def processor(dst_mail: str, bait_type:str, reminder: str, alert_dict: dict) -> str:

    alert_details = ""
    alert_id   = alert_dict.get("id","N/A")

    # Normalizing the Time Format to UTC before alert
    event_time = alert_dict.get('event_time')
    event_time = f"{datetime.fromisoformat(event_time).replace(tzinfo=timezone.utc)} UTC"
    alert_dict['event_time'] = event_time # updating Time Form in the Alert Data

    # Poping Alert so it doest Apear in Email Body
    alert_dict.pop('id')

    for key, value in alert_dict.items():
        key = key.replace("_", " ") # Hyphen Elimination

        tab = f"""
    <tr>
        <td style="padding:0 0 16px;">
            <table width="100%" cellpadding="12" cellspacing="0"
                    style="background:#1c2128;border:1px solid #21262d;border-radius:8px;">
                <tr>
                    <td>
                        <p style="margin:0 0 4px;font-size:15px;font-weight:600;
                                    letter-spacing:0.12em;text-transform:uppercase;color:#e6edf3;">
                        
                            <img src="https://img.icons8.com/?size=80&id=YGCpatc8SFgI&format=png"
                                    alt="Bait Triggered"
                                    style="width:25px;height:25px;vertical-align:middle;margin-right:6px;">
                            
                            <b>{key}</b>
                        </p>
                        <p style="margin:0;font-size:15px;font-weight:700;color:#8b949e;">
                            <typewrite>{value}</typewrite>
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
<body style="margin:0;padding:0;background:#0d1117;font-family:'Segoe UI',Arial,sans-serif;">

  <table width="100%" cellpadding="0" cellspacing="0" style="background:#0d1117;padding:40px 0;">
    <tr>
      <td align="center">
        <table width="520" cellpadding="0" cellspacing="0"
               style="background:#161b22;border:1px solid #21262d;border-radius:20px;overflow:hidden;max-width:520px;width:100%;">

          <!-- Header -->
        <tr>
            <td style="background:#f97316;padding:20px 32px;text-align:center;">
              <p style="margin:0;font-size:11px;font-weight:600;letter-spacing:0.15em;
                         text-transform:uppercase;color:rgba(255,255,255,0.75);">
                Deception-Based Breach Detection
              </p>

              <p style="margin:4px 0 0;font-size:22px;font-weight:700;
                         letter-spacing:0.08em;color:#ffffff;">
                DBBD
              </p>
            </td>
        </tr>

        <!-- Alert banner -->
        <tr>
            <td style="padding:32px 32px 8px;text-align:center;">

                <!-- Circle with centered image -->

                <table align="center" cellpadding="0" cellspacing="0" 
                    style="margin:0 auto 16px;">
                    <tr>
                        <td width="56" height="56" align="center" valign="middle"
                            style="background:rgba(248,81,73,0.12);
                                border:1px solid #f85149;
                                border-radius:50%;">

                        <img src="https://img.icons8.com/?size=48&id=dKMGP5XqWxob&format=png"
                            alt="Warning"
                            width="100%"
                            height="100%"
                            style="display:block;">

                        </td>
                    </tr>
                </table>

                <h1 style="margin:0 0 8px;font-size:20px;font-weight:700;color:#e6edf3;">
                    Your Bait Was Triggered
                </h1>

                <p style="margin:0;font-size:13px;color:#8b949e;line-height:1.5;">
                    A deception token has been accessed.<br>
                    Immediate review is recommended.
                </p>

            </td>
        </tr>

          <!--Divider -->
          <tr>
                <td style="padding:24px 32px 0;">
                <div style="height:1px;background:#21262d;"></div>
                </td>
          </tr>

        <!--Info rows  -->
        <!-- Triggered Bait -->
        <!-- Reminder -->
        <!-- Triggered Bait -->

        <tr>
            <td style="padding:0 0 16px;">
            <table width="100%" cellpadding="12" cellspacing="0"
                    style="background:#1c2128;border:1px solid #21262d;border-radius:8px;">
                <tr>
                <td>
                    <p style="margin:0 0 4px;font-size:15px;font-weight:600;
                                letter-spacing:0.12em;text-transform:uppercase;color:#e6edf3;">
                    
                    <img src="https://img.icons8.com/?size=80&id=7kldUKm86sUt&format=png"
                            alt="Bait Triggered"
                            style="width:30px;height:30px;vertical-align:middle;margin-right:6px;">
                    
                    Bait Type
                    </p>
                    <p style="margin:0;font-size:20px;font-weight:700;color:#8b949e;">
                        {bait_type}
                    </p>
                </td>
                </tr>
            </table>
            </td>
        </tr>


        <!-- Reminder -->
        <tr>
            <td style="padding:0 0 16px;">
            <table width="100%" cellpadding="12" cellspacing="0"
                    style="background:#1c2128;border:1px solid #21262d;border-radius:8px;">
                <tr>
                <td>
                    <p style="margin:0 0 4px;font-size:15px;font-weight:600;
                                letter-spacing:0.12em;text-transform:uppercase;color:#e6edf3;">
                    
                    <img src="https://img.icons8.com/?size=64&id=FhnRPWu7HD5f&format=png"
                            alt="Reminder"
                            style="width:30px;height:30px;vertical-align:middle;margin-right:6px;">
                    
                    Reminder
                    </p>
                    <p style="margin:0;font-size:14px;font-weight:600;color:#8b949e;">
                    {reminder}
                    </p>
                </td>
                </tr>
            </table>
            </td>
        </tr>

        {alert_details}
          
        <div style="display:flex; flex-direction:column; align-items:center; gap:16px; padding:2rem 1.5rem;">
            <a href="http://192.168.100.10:5000/triggers" style=" display:block;width:100%; max-width:500px;padding:18px 24px; background:#2D6A4F; border-radius:50px;text-align:center; font-size:18px;font-weight:500;color:#1B3A2D;text-decoration:none;transition:background 0.2s;" onmouseover="this.style.background='#3A8A64'" onmouseout="this.style.background='#2D6A4F'">
                Manage Alerts
            </a>
            
        </div>

        <!-- Footer -->
        <tr>
            <td style="padding:0 32px 32px;text-align:center;">
                <div style="height:1px;background:#21262d;margin-bottom:20px;"></div>
                <p style="margin:0;font-size:11px;color:#8b949e;line-height:1.6;">
                This alert was sent to <span style="color:#e6edf3;">{dst_mail}</span>
                because a bait token associated with your account was triggered.<br>
                Alert ID: <span style="font-family:monospace;color:#f97316;">#{alert_id}</span>
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
            subject="DBBD Alert Bait Triggered",
            body_html=body_html
        )
    except Exception as e:
        return  f"Error Occured: {e}"



if __name__ == "__main__":
    mailer(dst_mail=_dst_mail,bait_type=_bait_type, reminder=_reminder, alert_dict=_alert_dict)
