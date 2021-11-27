# ZendeskCodingChallenge
A ticket viewer for the Zendesk customer service tool.

#TODO: 
# 1) include a README with installation and usage instructions

- install ZenPy: http://docs.facetoe.com.au/zenpy.html#installation
- create a file called creds.py
- insert this dictionary in the creds.py file populated with your login credentials
creds = {
    "email": "your@email.com",
    "password": "YourPassword",
    "subdomain": "YourSubdomain"
}

- Make sure that your settings allow API calls.
  - go to: https://{YourSubdomain}.zendesk.com/admin/apps-integrations/apis/apis/settings
  - enable password access

curl https://zccmzrithm.zendesk.com/api/v2/imports/tickets/create_many.json -v -u zelechom@oregonstate.edu:MBbFZMLoDewZpB POST -d @tickets.json -H "Content-Type:
application/json"
