from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import EmailMultiAlternatives
from django.db.models.signals import post_save
from django.dispatch import receiver

from timesheet.models import MonthlyEntry


@receiver(post_save, weak=False, sender=MonthlyEntry,
          dispatch_uid='timesheet_on_post_save')
def timesheet_on_post_save(sender, instance, raw, created, **kwargs):
    if not raw:
        if created:
            employee = instance.employee
            supervisor = employee.supervisor
            site_url = f"https://{get_current_site(request=None).domain}"
            from_email = "bhp.se.dmc@gmail.com"
            subject = "Timesheet submission"

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
            msg = EmailMultiAlternatives(subject=subject, body=body,
                                         from_email=from_email, to=(supervisor.email,) )
            msg.content_subtype = 'html'
            print("Sending to : ", supervisor.email)
            try:
                msg.send()
            except Exception as e:
                raise


@receiver(post_save, weak=False, sender=MonthlyEntry,
          dispatch_uid='timesheet_on_post_save')
def timesheet_on_status_update(sender, instance, raw, created, **kwargs):
    # triggered when status changes
    if instance and not created:
        if instance.status == 'approved':
            employee = instance.employee
            site_url = f"https://{get_current_site(request=None).domain}"
            hr_email = "dthebe@bhp.org.bw"
            from_email = "bhp.se.dmc@gmail.com"
            subject = "Timesheet submission"

            body = f"""\
                        Dear HR,
                        <br>
                        <br>
                        This is an automated notification to inform you that  {instance.approved_by},
                        has approved the { instance.month } timesheet for {employee.employee_code} 
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
            msg = EmailMultiAlternatives(subject=subject, body=body,
                                         from_email=from_email, to=(hr_email,))
            msg.content_subtype = 'html'
            print("Sending to : ", hr_email)
            try:
                msg.send()
            except Exception as e:
                raise



