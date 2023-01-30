from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import EmailMultiAlternatives
from django.db.models.signals import post_save
from django.dispatch import receiver

from timesheet.models import MonthlyEntry


def send_email(to, subject, body, from_email='bhp.se.dmc@gmail.com'):
    msg = EmailMultiAlternatives(subject=subject, body=body, from_email=from_email, to=(to,))
    msg.content_subtype = 'html'
    print(f"Sending to: {to}")
    try:
        msg.send()
    except Exception as e:
        raise


@receiver(post_save, weak=False, sender=MonthlyEntry, dispatch_uid='timesheet_on_post_save')
def timesheet_notification(sender, instance, raw, created, **kwargs):
    employee = instance.employee
    site_url = f"https://{get_current_site(request=None).domain}"
    supervisor = employee.supervisor
    if not raw:
        if created:
            subject = "Timesheet submission"
            recipient = supervisor.email
            body = f"""\
                        Dear {supervisor.first_name} {supervisor.last_name},
                        <br>
                        <br>
                        This is an automated notification to inform you that {employee.first_name} (Employee ID: {employee.employee_code}),
                         has submitted their timesheet for review. Please log in to the system to review it.
                        <br>
                        <br>
                        <a href="{site_url}" target="_blank">Visit Site</a>
                        <br>
                        <br>
                        Thank you,
                        """
            send_email(recipient, subject, body)
        elif not created and instance.status == 'approved':
            subject = "Timesheet Approval"
            recipient = "dthebe@bhp.org.bw"
            body = f"""\
                        Dear HR,
                        <br>
                        <br>
                        This is an automated notification to inform you that  {instance.approved_by},
                        has approved the {instance.month} timesheet for {employee.employee_code} 
                        (Employee ID: {employee.employee_code}). 
                        <br>
                        Please log in to the system to verify it.
                        <br>
                        <br>
                        <a href="{site_url}" target="_blank">Visit Site</a>
                        <br>
                        <br>
                        Thank you,
                        """
            send_email(recipient, subject, body)
