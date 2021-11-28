from creds import creds
from zenpy import Zenpy
from textwrap import wrap
from datetime import datetime


class ZendeskTicket:
    """docstring"""

    def __init__(self):
        """docstring"""
        self._tickets = {}
        self._search_results = None
        self._page_display = 25

    def get_tickets(self):
        """docstring"""
        try:
            self._tickets = {}
            zenpy_client = Zenpy(**creds)
            for ticket in zenpy_client.tickets(type='ticket'):
                self._tickets[ticket.id] = ticket.to_dict()
                self._tickets[ticket.id]["API"] = datetime.now()
        except:
            print("An exception has occurred. Please check your login credentials and try again.")

    def get_ticket_data(self):
        """docstring"""
        return self._tickets

    def get_page_display(self):
        """docstring"""
        return self._page_display

    def set_page_display(self, new_page):
        """docstring"""
        self._page_display = new_page

    def get_tags_info(self):
        """docstring"""
        all_tags = []
        for id in self._tickets:
            for tag in self._tickets[id]["tags"]:
                all_tags.append(tag)
        tags = set(all_tags)
        tags_dict = {}
        for tag in tags:
            tags_dict[tag] = all_tags.count(tag)
        number = len(tags)
        print("\n", end="")
        print(f"There are {number} unique tags applied to your tickets.")
        print("\n", end="")
        count = 0
        for tag in tags_dict:
            display = f"{tag} ({tags_dict[tag]})"
            print(f"{display: <24}", end="")
            count += 1
            if count % 5 == 0:
                print("\n", end="")
        print("\n", end="")
        print("\n", end="")
        return tags

    def add_API_timestamp(self, id):
        message = "Zendesk API Called: "
        timestamp = f"{message}{self._tickets[id]['API']}"
        return timestamp

    def display_tickets(self):
        """docstring"""
        page = self._page_display
        max_width = 70
        count = 0
        if self._search_results is None:
            tickets = self._tickets
        else:
            tickets = self._search_results
        total = len(tickets)
        desired_fields = ["requester_id", "assignee_id", "subject", "description", "tags"]
        ticket_break = max_width * "_"
        print(ticket_break)
        for id in tickets:
            print(f"[Ticket ID #{id}]")
            count += 1
            for key in desired_fields:
                key_text = format_key_display(key)
                print(f"{key_text}", end="")
                if type(tickets[id][key]) is str:
                    if key == "description":
                        print("\n", end="")
                    text = wrap(tickets[id][key], width=max_width)
                    for line in text:
                        print(line)
                    print("\n", end="")
                elif type(tickets[id][key]) is list:
                    for item in tickets[id][key]:
                        if item == list(tickets[id][key])[-1]:
                            print(f"{item} ", end="")
                        else:
                            print(f"{item}, ", end="")
                else:
                    print(tickets[id][key])
            print("\n", "\n", end="")
            print(self.add_API_timestamp(id))
            print(ticket_break)
            id_list = list(tickets)
            if count % page == 0:
                if page == 1:
                    print(f"Ticket #{id} is displayed out of {total} tickets.")
                else:
                    print(
                        f"Tickets #{id_list[id_list.index(id) - (page - 1)]} through #{id} are displayed out of {total} tickets.")

                if list(tickets)[-1] == id:
                    print("This is the end of the ticket display.")
                    print("Press any key to exit the display function.")
                    input()
                else:
                    print(
                        "Press any key to display the next batch of tickets -or- enter 'Q' to leave the ticket display.")
                    user_input = input().lower()
                    if user_input == 'q':
                        print("\n", end="")
                        return
            if total < page and total == count:
                if total == 1:
                    print(f"There is {total} ticket displayed.")
                    print("\n", end="")
                else:
                    print(f"There are {total} tickets displayed.")
                    print("\n", end="")
        self._search_results = None

    def search_subject(self, search_term):
        """docstring"""
        search_results = {}
        for ticket in self._tickets:
            if search_term in self._tickets[ticket]["subject"].lower():
                search_results[ticket] = self._tickets[ticket]
        total = len(search_results)
        if total == 0:
            print(f"There are no results that match your subject search for: {search_term}")
        else:
            print(f"There are {total} tickets that match your subject search for: {search_term}")
            print("Press any key to display results.")
            input()
            self._search_results = search_results
            self.display_tickets()

    def search_description(self, search_term):
        """docstring"""
        search_results = {}
        for ticket in self._tickets:
            if search_term in self._tickets[ticket]["description"].lower():
                search_results[ticket] = self._tickets[ticket]
        total = len(search_results)
        if total == 0:
            print(f"There are no results that match your description search for: {search_term}")
        else:
            print(f"There are {total} tickets that match your description search for: {search_term}")
            print("Press any key to display results.")
            input()
            self._search_results = search_results
            self.display_tickets()

    def search_tags(self, search_term):
        """docstring"""
        search_results = {}
        for ticket in self._tickets:
            if search_term in self._tickets[ticket]["tags"]:
                search_results[ticket] = self._tickets[ticket]
        total = len(search_results)
        if total == 0:
            print(f"There are no results that match your tag search for: {search_term}")
        else:
            print(f"There are {total} tickets that match your tag search for: {search_term}")
            print("Press any key to display results.")
            input()
            self._search_results = search_results
            self.display_tickets()

    def search_ticket_id(self, id_number):
        """docstring"""
        search_results = {}
        try:
            search_results[id_number] = self._tickets[id_number]
        except KeyError:
            print(f"Ticket #{id_number} cannot be found.")
        total = len(search_results)
        if total == 0:
            print(f"There are no results that match your ticket ID search for #{id_number}.")
        else:
            print(f"Ticket #{id_number} has been retrieved.")
            print("Press any key to display results.")
            input()
            self._search_results = search_results
            self.display_tickets()


def format_key_display(key):
    """docstring"""
    offset = 15
    length = len(key)
    diff = offset - length
    space_string = diff * " "
    key = key.replace("_", " ")
    key = key.title()
    key += ":"
    key += space_string
    return key


def display_menu():
    low = 1
    high = 8
    print("*************************************")
    print("Welcome to the Zendesk Ticket Viewer!")
    print("*************************************")
    print("Please make a selection.")
    menu = {
        1: "Display Tickets",
        2: "Display Search Tags",
        3: "Search Tickets by Subject",
        4: "Search Tickets by Description",
        5: "Search Tickets by Tag Identifier",
        6: "Search Tickets by Ticket ID Number",
        7: "Update Local Tickets from Zendesk API",
        8: "Change Number of Tickets Displayed Per Page",
        "Q": "Quit Zendesk Ticket Viewer"
    }
    for key in menu:
        print(f"{key} : {menu[key]}")
    selection = input().strip()
    if selection.lower() == "q":
        return selection
    elif selection.isnumeric():
        if low <= int(selection) <= high:
            return selection
        else:
            display_menu()


if __name__ == "__main__":

    user_engaged = True
    zt = ZendeskTicket()
    zt.get_tickets()
    while user_engaged:
        user_input = display_menu()
        if user_input.isnumeric():  # number is validated by display_menu()
            user_input = int(user_input)
            if user_input == 1:  # display tickets
                zt.display_tickets()
            elif user_input == 2:  # display search tags
                zt.get_tags_info()
            elif user_input == 3:  # search tickets by subject
                print("Please enter the * SUBJECT * search term.")
                search_term = input().strip().lower()
                zt.search_subject(search_term)
            elif user_input == 4:  # search tickets by description
                print("Please enter the * DESCRIPTION * search term.")
                search_term = input().strip().lower()
                zt.search_description(search_term)
            elif user_input == 5:  # search tickets by tag identifier
                zt.get_tags_info()
                print("Please enter the * TAGS * search term.")
                search_term = input().strip().lower()
                zt.search_tags(search_term)
            elif user_input == 6:
                ticket_ids = list(zt.get_ticket_data())
                first_ticket = ticket_ids[0]
                last_ticket = ticket_ids[-1]
                searching = True
                while searching:
                    print(f"You have Ticket IDs in the range of #{first_ticket} to #{last_ticket}.")
                    print(f"Please enter the * TICKET ID * number.")
                    id_number = input().strip()
                    if id_number.isnumeric() and first_ticket <= int(id_number) <= last_ticket:
                        searching = False
                        zt.search_ticket_id(int(id_number))
                    elif id_number.lower() == "q":
                        searching = False
                    else:
                        print("Invalid entry. Please try again or enter 'Q' to quit.")
            elif user_input == 7:  # update local tickets from zendesk api
                zt.get_tickets()
                print("* Your Zendesk API call was successful! *")
                print("\n", end="")
            elif user_input == 8:  # change number of tickets displayed per page scroll
                print(f"You are currently seeing {zt.get_page_display()} ticket(s) per page.")
                print("Please enter a number in the range of 1 to 25 -or- press any key to keep the default value.")
                page_input = input().strip()
                if page_input.isnumeric() and 0 < int(page_input) < 26:
                    zt.set_page_display(int(page_input))
                print("\n", end="")
                print(f"* You will see {zt.get_page_display()} ticket(s) per page. *")
                print("\n", end="")
        else:  # quit program
            user_engaged = False
            print("Thank you for using the Zendesk Ticket Viewer. Goodbye!")
