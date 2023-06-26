from __future__ import print_function
import time
import sib_api_v3_sdk
from sib_api_v3_sdk.rest import ApiException
from pprint import pprint
import util.config as config
import util.logger as logger

my_logger = logger.get_logger("sendEmail.py")


def send_email(lead):

    # Configure API key authorization: api-key
    configuration = sib_api_v3_sdk.Configuration()
    configuration.api_key['api-key'] = config.keys["brevo_api_key"]

    contact_api_instance = sib_api_v3_sdk.ContactsApi(sib_api_v3_sdk.ApiClient(configuration))
    email = lead["email"]
    existing_contact = contact_api_instance.get_contact_info(email)
    if (existing_contact):
        create_contact = sib_api_v3_sdk.CreateContact(email = email)
        create_contact.attributes = lead["params"]
        created_contact = contact_api_instance.create_contact(create_contact)
        my_logger.info("Successfully added contact: " + str(created_contact))
    else: 
        my_logger.info("Found contact: " + str(existing_contact))

    # create an instance of the API class
    api_instance = sib_api_v3_sdk.TransactionalEmailsApi(sib_api_v3_sdk.ApiClient(configuration))

    send_smtp_email = sib_api_v3_sdk.SendSmtpEmail(
        to=[{
        "email": lead["email"],
        "name": lead["name"]
        }], 
        template_id = lead["template"], 
        params = lead["params"], 
        headers = {"X-Mailin-custom": "custom_header_1:custom_value_1|custom_header_2:custom_value_2|custom_header_3:custom_value_3", "charset": "iso-8859-1"}) 
    send_smtp_email
    # SendSmtpEmail | Values to send a transactional email

    try:
        # Send a transactional email
        api_response = api_instance.send_transac_email(send_smtp_email)
        # my_logger.info("Successfully sent email from Brevo: " + to_attribute[0]["email"])
        my_logger.info("Successfully sent email from Brevo: ")
        pprint(api_response)
    except ApiException as e:
        my_logger.error("Exception when calling SMTPApi->send_transac_email: %s\n" % e)

