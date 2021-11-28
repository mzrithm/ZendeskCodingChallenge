from creds import creds
from zenpy import Zenpy
from textwrap import wrap
from datetime import datetime


class ZendeskTicket:
    """
    This class creates a Zendesk ticket object with three
    private data members. This ticket object uses the Zenpy
    library to call the Zendesk API and populate a "tickets"
    data member with a python dictionary representing all
    Zendesk tickets associated with the user's account.
    This object is used to view and search tickets.
    Note: Login credentials must be entered in attached
    credentials.py file and API call requests made via
    account password authentication must be enabled on the
    Zendesk admin account being called.
    """

    def __init__(self):
        """
        This method initializes a Zendesk Ticket object.
        All data members are private. The "tickets" data member
        is populated by a python dictionary representing all available
        tickets on the user's account. The key is teh ticket ID number
        and the value is a ticket dictionary object including all possible
        data fields with their default values. Search results is initialized
        as None, and the page_display is set to a default value of 25 tickets
        per page.
        """
        self._tickets = None
        self._search_results = None
        self._page_display = 25

    def get_tickets(self):
        """
        This method calls the Zendesk API using the Zenpy library.
        This method saves all current ticket data associated with the user's
        account to the "tickets" data member. This method overwrites local data.
        A Zendesk API Call datatime object is added to every ticket so that the user
        can judge the required frequency of their API call requests based on the age
        of local data.
        """
        # A datetime object is added to every ticket because editing & adding tickets
        # are features that could be added to this program and these features would
        # cause staggered timestamps on the tickets. Currently they are all the same timestamp.
        try:
            self._tickets = {}
            zenpy_client = Zenpy(**creds)
            for ticket in zenpy_client.tickets(type='ticket'):
                self._tickets[ticket.id] = ticket.to_dict()
                self._tickets[ticket.id]["API"] = datetime.now()
        except:
            print("An exception has occurred. Please check your login credentials and try again.")
            # Login credentials must be entered in the associated credentials.py file and
            # email/password authentication must be enabled on the user's Zendesk admin account.

    def get_ticket_data(self):
        """
        This method allows access to the private data member "tickets"
        from outside the ZendeskTicket class. Returns a python dictionary
        populated with all available ticket data from the last Zendesk API call.
        """
        return self._tickets

    def get_page_display(self):
        """
        This method allows access to the private data member "page_display"
        from outside the ZendeskTicket class. Returns an integer representing
        the number of tickets displayed per page.
        """
        return self._page_display

    def set_page_display(self, new_page):
        """
        This method allows changes to the private data member "page_display"
        from outside the ZendeskTicket class. It accepts one parameter, an int
        representing the number of tickets to be viewed per page, and updates
        the page_display data member with that value. Returns nothing.
        """
        self._page_display = new_page

    def get_tags_info(self):
        """
        This method reviews available ticket data in the ZendeskTicket object and
        creates a set of all tags used along with a count of frequency of use of each tag.
        This method displays the total number of unique tags, followed by a
        formatted column display of tags, with the frequency count appearing after each tag
        in parentheses. If there are no tags associated with the tags, this method
        informs the user with a message and returns.
        """
        all_tags = []
        for id in self._tickets:
            for tag in self._tickets[id]["tags"]:
                all_tags.append(tag)        # append all tags to a list
        tags = set(all_tags)                # create a set of the list of tags to find all unique tags
        if len(tags) == 0:                  # handle edge case where user has not applied tags to tickets
            print("There are no tags associated with your Zendesk tickets.")
            return
        else:
            tags_dict = {}                  # dictionary structure allows recording of tag as key with count as value
            for tag in tags:                # iterate through tags set to create key, and count the presence of tag in all_tags
                tags_dict[tag] = all_tags.count(tag)
            number = len(tags)
            print("\n", end="")
            print(f"There are {number} unique tags applied to your tickets.")
            print("\n", end="")             # report the number of unique tags to the user
            count = 0
            for tag in tags_dict:           # format tags for column display so that all tags can be viewed at once
                display = f"{tag} ({tags_dict[tag]})"
                print(f"{display: <24}", end="")
                count += 1
                if count % 5 == 0:
                    print("\n", end="")
            print("\n", end="")
            print("\n", end="")

    def add_API_timestamp(self, id):
        """
        This method accepts a ticket ID number as a parameter
        and returns a timestamp message to be displayed at the bottom
        of the ticket display for each ticket. This method is applied to each
        ticket so that future features like ticket editing, or ticket addition
        will allow for staggered API call timestamps. This method is
        called by display_tickets().
        """
        message = "Zendesk API Called: "
        timestamp = f"{message}{self._tickets[id]['API']}"
        return timestamp

    def display_tickets(self):
        """
        This method displays all tickets associated with the Zendesk ticket object.
        This method is modular and gives precedence to the "search_results" data member
        over the "tickets" data member if the "search_results" data member is not None.
        This method uses the "page_display" data member to determine tickets displayed per page.
        This method also prints descriptive messages for the user about what ticket ids are currently
        being displayed, how many tickets in total are being displayed, and when there are no more tickets
        to display. This method validates the presence of tickets in "tickets" data member and restores
        default of None in "search_results" data member when it is called.
        """
        if self._tickets is not None and len(self._tickets) != 0:
            page = self._page_display
            max_width = 70      # ticket display format
            count = 0
            if self._search_results is None:    # give precedence to search_results over tickets
                tickets = self._tickets
            else:
                tickets = self._search_results
            total = len(tickets)                # capture total number of tickets
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
    elif selection.isnumeric() and low <= int(selection) <= high:
        selection = int(selection)
        return selection
    else:
        print("\n", end="")
        print("* Invalid selection. Please try again. *")
        print("\n", end="")
        return display_menu()


if __name__ == "__main__":

    user_engaged = True
    zt = ZendeskTicket()
    zt.get_tickets()
    while user_engaged:
        user_input = display_menu()     # user input is validated by display_menu()
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
        elif user_input == 6:  # search tickets by ticket id number
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
