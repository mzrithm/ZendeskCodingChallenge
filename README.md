# Zendesk Coding Challenge 2021

This is a **Zendesk Ticket Viewer** for the Zendesk customer service tool. This ticket viewer was created by me as part of the interview process for a **Zendesk Software Engineer Internship** for the **Summer of 2022**.

---

### Description:

This **Zendesk Ticket Viewer** uses the **Zenpy** library to make a call to the **Zendesk API** and to display all tickets at the `CLI`. 

![A screenshot of the zendesk ticket viewer menu](https://github.com/mzrithm/ZendeskCodingChallenge/blob/c44cb49ade4bcadbd23d2d20be1021556bb2a439/menu.png)

Tickets are stored locally in a **ZendeskTicket** object. This object has a `tickets` data member that is populated by a python dictionary with the first API call. For this python dictionary, the key is the **Ticket ID Number** and the value is a single **Ticket Dictionary**. This structure is ideal as it allows rapid access of ticket information based on key queries that match ticket fields.

![A screenshot of a single ticket display](https://github.com/mzrithm/ZendeskCodingChallenge/blob/c44cb49ade4bcadbd23d2d20be1021556bb2a439/ticket.png)

The **ZendeskTicket** class includes methods that do the following:
- display all tickets
- display all search tags
- display all tickets with a search term in the subject field
- display all tickets with a search term in the description field
- display all tickets with a tag identifier
- display a ticket with a particular ticket ID number
- update local ticket data with a new Zendesk API call
- change the number of tickets displayed per page (default is 25 tickets per page)

![A screenshot of a tags display](https://github.com/mzrithm/ZendeskCodingChallenge/blob/c44cb49ade4bcadbd23d2d20be1021556bb2a439/tags.png)

This **Zendesk Ticket Viewer** is run as a script from `main()` but the **ZendeskTicket** can also be used as an imported class. There are detailed docstrings regarding parameters, returns, and data validation for each class method and external function. 

I hope you enjoy my work!

---

### Program Requirements:
- Sign up for a free trial with [Zendesk](https://www.zendesk.com/register).
- Take note of the email address you use, your password, and your subdomain. You will need this information to create your login credentials for Zendesk API calls.
- Log in to your account and enable password access for Zendesk API calls. 
- Install the [Zenpy](http://docs.facetoe.com.au/zenpy.html#installation) library on your computer.
- `Fork` this repo.
- `Clone` the forked copy of this repo to your local computer.
- Follow the directions in `credentials.py` to add your login credentials.
- `Run ZendeskCodingChallenge.py`

---

### Troubleshooting:
- Check that your email address, password, and subdomain are all typed correctly, enclosed by quotation marks, contain no extra spaces or characters, and no extra punctuation.
- Passwords that included single or double quotation marks may not work; update your password and try again. 
- New Zendesk accounts have password authentication for API calls disabled by default; go to `https://YourSubdomain.zendesk.com/admin/apps-integrations/apis/apis/settings`, where `YourSubdomain` is the subdomain you chose in your free trial sign up, and change this setting to `enabled`.

---

#### authored by Michelle Zelechoski
