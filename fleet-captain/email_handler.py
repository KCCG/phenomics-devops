import logging
import requests
import uuid


class email_handler():
    logger = logging.getLogger(__name__)

    email_service_url = 'http://52.62.22.150:9090/email/'

    def process_item(notification_message, time_stamp, alarm, terminating):
        request_params = email_handler._get_params (notification_message, time_stamp, alarm, terminating)
        response = requests.post(email_handler.email_service_url, json=request_params)
        if response.status_code != 200 or response.text == '[]':
            logging.info("Error in sending email.")
        else:
            logging.info("Email sent.")

    @staticmethod
    def _get_params(message, time_stamp, alarm, terminating):
        subject = "FleetAlert"
        if terminating:
            subject = subject +":Terminating"
        elif alarm:
            subject = subject +":Alarm"

        data = {
            "toRecipients": [
                "fastmuaz@gmail.com"],
            "message": '<html> <table border="1"><caption>Workers Status {}</caption>  {} </table></html>'.format(time_stamp, email_handler._format_message(message)),
            "subject": subject,
            "sender": "Fleet Captain",
            "uniqueID": str(uuid.uuid4())
        }
        return data


    @staticmethod
    def _format_message(messages):
        string_message = "<tr><th>WorkerID</th> <th>LastRun</th> <th>PMIDs</th> <th>Active</th> <th>Healthy</th> <th>Terminating</th></tr>"
        for m in messages:
            string_message = string_message + str(m)
        return string_message;





# email_handler.process_item("nice", "12")