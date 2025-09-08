"""
SMS and Email Notification Service
Implements automated communication for loan management as per SML Project specifications
"""

import logging
from django.conf import settings
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils import timezone
from datetime import datetime, timedelta

logger = logging.getLogger(__name__)

class NotificationService:
    """Centralized notification service for SMS and Email"""
    
    def __init__(self):
        self.sms_enabled = getattr(settings, 'SMS_ENABLED', True)
        self.email_enabled = getattr(settings, 'EMAIL_ENABLED', True)
    
    def send_payment_reminder(self, borrower, loan, days_before=3):
        """Send payment reminder before due date"""
        try:
            # Email notification
            if self.email_enabled and borrower.email:
                self._send_payment_reminder_email(borrower, loan, days_before)
            
            # SMS notification
            if self.sms_enabled and borrower.mobile:
                self._send_payment_reminder_sms(borrower, loan, days_before)
                
            logger.info(f"Payment reminder sent to {borrower.full_name} for loan {loan.id}")
            return True
            
        except Exception as e:
            logger.error(f"Failed to send payment reminder: {str(e)}")
            return False
    
    def send_overdue_alert(self, borrower, loan, days_overdue):
        """Send overdue payment alert"""
        try:
            # Email notification
            if self.email_enabled and borrower.email:
                self._send_overdue_alert_email(borrower, loan, days_overdue)
            
            # SMS notification
            if self.sms_enabled and borrower.mobile:
                self._send_overdue_alert_sms(borrower, loan, days_overdue)
                
            logger.info(f"Overdue alert sent to {borrower.full_name} for loan {loan.id}")
            return True
            
        except Exception as e:
            logger.error(f"Failed to send overdue alert: {str(e)}")
            return False
    
    def send_payment_confirmation(self, borrower, loan, payment_amount):
        """Send payment confirmation"""
        try:
            # Email notification
            if self.email_enabled and borrower.email:
                self._send_payment_confirmation_email(borrower, loan, payment_amount)
            
            # SMS notification
            if self.sms_enabled and borrower.mobile:
                self._send_payment_confirmation_sms(borrower, loan, payment_amount)
                
            logger.info(f"Payment confirmation sent to {borrower.full_name}")
            return True
            
        except Exception as e:
            logger.error(f"Failed to send payment confirmation: {str(e)}")
            return False
    
    def send_loan_approval_notification(self, borrower, loan):
        """Send loan approval notification"""
        try:
            # Email notification
            if self.email_enabled and borrower.email:
                self._send_loan_approval_email(borrower, loan)
            
            # SMS notification
            if self.sms_enabled and borrower.mobile:
                self._send_loan_approval_sms(borrower, loan)
                
            logger.info(f"Loan approval notification sent to {borrower.full_name}")
            return True
            
        except Exception as e:
            logger.error(f"Failed to send loan approval notification: {str(e)}")
            return False
    
    def send_kyc_verification_notification(self, borrower, kyc_status):
        """Send KYC verification status notification"""
        try:
            # Email notification
            if self.email_enabled and borrower.email:
                self._send_kyc_verification_email(borrower, kyc_status)
            
            # SMS notification
            if self.sms_enabled and borrower.mobile:
                self._send_kyc_verification_sms(borrower, kyc_status)
                
            logger.info(f"KYC verification notification sent to {borrower.full_name}")
            return True
            
        except Exception as e:
            logger.error(f"Failed to send KYC verification notification: {str(e)}")
            return False
    
    # Private methods for email notifications
    def _send_payment_reminder_email(self, borrower, loan, days_before):
        """Send payment reminder email"""
        subject = f"Payment Reminder - Loan #{loan.id}"
        context = {
            'borrower_name': borrower.full_name,
            'loan_id': loan.id,
            'due_date': loan.next_payment_date,
            'amount': loan.next_payment_amount,
            'days_before': days_before
        }
        
        html_message = render_to_string('notifications/payment_reminder_email.html', context)
        plain_message = render_to_string('notifications/payment_reminder_email.txt', context)
        
        send_mail(
            subject=subject,
            message=plain_message,
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[borrower.email],
            html_message=html_message
        )
    
    def _send_overdue_alert_email(self, borrower, loan, days_overdue):
        """Send overdue alert email"""
        subject = f"Payment Overdue - Loan #{loan.id}"
        context = {
            'borrower_name': borrower.full_name,
            'loan_id': loan.id,
            'overdue_amount': loan.overdue_amount,
            'days_overdue': days_overdue
        }
        
        html_message = render_to_string('notifications/overdue_alert_email.html', context)
        plain_message = render_to_string('notifications/overdue_alert_email.txt', context)
        
        send_mail(
            subject=subject,
            message=plain_message,
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[borrower.email],
            html_message=html_message
        )
    
    def _send_payment_confirmation_email(self, borrower, loan, payment_amount):
        """Send payment confirmation email"""
        subject = f"Payment Confirmation - Loan #{loan.id}"
        context = {
            'borrower_name': borrower.full_name,
            'loan_id': loan.id,
            'payment_amount': payment_amount,
            'payment_date': timezone.now().date()
        }
        
        html_message = render_to_string('notifications/payment_confirmation_email.html', context)
        plain_message = render_to_string('notifications/payment_confirmation_email.txt', context)
        
        send_mail(
            subject=subject,
            message=plain_message,
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[borrower.email],
            html_message=html_message
        )
    
    def _send_loan_approval_email(self, borrower, loan):
        """Send loan approval email"""
        subject = f"Loan Approved - Loan #{loan.id}"
        context = {
            'borrower_name': borrower.full_name,
            'loan_id': loan.id,
            'loan_amount': loan.amount,
            'interest_rate': loan.interest_rate,
            'tenure': loan.tenure_months
        }
        
        html_message = render_to_string('notifications/loan_approval_email.html', context)
        plain_message = render_to_string('notifications/loan_approval_email.txt', context)
        
        send_mail(
            subject=subject,
            message=plain_message,
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[borrower.email],
            html_message=html_message
        )
    
    def _send_kyc_verification_email(self, borrower, kyc_status):
        """Send KYC verification email"""
        subject = f"KYC Verification {kyc_status.title()}"
        context = {
            'borrower_name': borrower.full_name,
            'kyc_status': kyc_status
        }
        
        html_message = render_to_string('notifications/kyc_verification_email.html', context)
        plain_message = render_to_string('notifications/kyc_verification_email.txt', context)
        
        send_mail(
            subject=subject,
            message=plain_message,
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[borrower.email],
            html_message=html_message
        )
    
    # Private methods for SMS notifications
    def _send_payment_reminder_sms(self, borrower, loan, days_before):
        """Send payment reminder SMS"""
        message = f"Dear {borrower.full_name}, your EMI of ₹{loan.next_payment_amount} for Loan #{loan.id} is due on {loan.next_payment_date}. Please ensure timely payment to avoid penalties."
        self._send_sms(borrower.mobile, message)
    
    def _send_overdue_alert_sms(self, borrower, loan, days_overdue):
        """Send overdue alert SMS"""
        message = f"Your payment for Loan #{loan.id} is overdue by {days_overdue} days. Please pay ₹{loan.overdue_amount} immediately to avoid additional charges."
        self._send_sms(borrower.mobile, message)
    
    def _send_payment_confirmation_sms(self, borrower, loan, payment_amount):
        """Send payment confirmation SMS"""
        message = f"Thank you for your payment of ₹{payment_amount}. Your EMI for {timezone.now().strftime('%B %Y')} is successfully processed."
        self._send_sms(borrower.mobile, message)
    
    def _send_loan_approval_sms(self, borrower, loan):
        """Send loan approval SMS"""
        message = f"Congratulations! Your loan application #{loan.id} for ₹{loan.amount} has been approved. You will receive the disbursement within 24-48 hours."
        self._send_sms(borrower.mobile, message)
    
    def _send_kyc_verification_sms(self, borrower, kyc_status):
        """Send KYC verification SMS"""
        if kyc_status == 'verified':
            message = f"Your KYC verification is complete. You can now proceed with loan applications."
        else:
            message = f"Your KYC verification is {kyc_status}. Please check your email for details."
        self._send_sms(borrower.mobile, message)
    
    def _send_sms(self, mobile_number, message):
        """Send SMS using configured gateway"""
        try:
            # Integration with SMS gateway (example with Twilio)
            if hasattr(settings, 'TWILIO_ACCOUNT_SID') and hasattr(settings, 'TWILIO_AUTH_TOKEN'):
                from twilio.rest import Client
                client = Client(settings.TWILIO_ACCOUNT_SID, settings.TWILIO_AUTH_TOKEN)
                client.messages.create(
                    body=message,
                    from_=settings.TWILIO_PHONE_NUMBER,
                    to=f"+91{mobile_number}"
                )
            else:
                # Fallback: Log SMS for development
                logger.info(f"SMS to {mobile_number}: {message}")
                
        except Exception as e:
            logger.error(f"Failed to send SMS to {mobile_number}: {str(e)}")

# Global notification service instance
notification_service = NotificationService()







