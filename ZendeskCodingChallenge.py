# from credentials import creds
from creds import creds
from zenpy import Zenpy
from textwrap import wrap
from datetime import datetime
from time import sleep


class ZendeskTicket:
    """
    This class creates a Zendesk ticket object with four
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
        tickets on the user's account. The key is the ticket ID number
        and the value is a ticket dictionary object (including all possible
        data fields with their default values). Search_results and tags are initialized
        as None, and the page_display is set to a default value of 25 tickets
        per page.
        """
        self._tickets = None
        self._search_results = None
        self._tags = None
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
            self._tags = None   # prevents incorrect tags references in local data
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

    def get_search_results(self):
        """
        This method allows access to the private data member "search_results"
        from outside the ZendeskTicket class. Returns a dictionary of tickets
        or None.
        """
        return self._search_results

    def get_tags_info(self):
        """
        This method reviews available ticket data in the ZendeskTicket object and
        creates a set of all tags used, along with a count of frequency of use of each tag.
        The 'tags" data member is updated with the tags dictionary that this method creates.
        This method displays the total number of unique tags, followed by a
        formatted column display of tags, with the frequency count appearing after each tag
        in parentheses. If there are no tags associated with the tickets, this method
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
            self._tags = tags_dict          # updates tags data member
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
        This method displays all tickets associated with the Zendesk ticket object's "tickets"
        or "search_results" data member. This method is modular and gives precedence to the "search_results"
        data member over the "tickets" data member if the "search_results" data member is not None.
        This method uses the "page_display" data member to determine tickets displayed per page.
        This method also prints descriptive messages for the user about what ticket ids are currently
        being displayed, how many tickets in total are being displayed, and when it is the end of the display.
        This method validates the presence of tickets in "tickets" data member and restores
        the default of None in "search_results" data member when it is called.
        """
        if self._tickets is not None and len(self._tickets) != 0:
            page = self._page_display
            max_width = 70      # ticket display format for page width; default = 70
            count = 0
            if self._search_results is None:    # give precedence to search_results over display of all tickets
                tickets = self._tickets
            else:
                tickets = self._search_results
            total = len(tickets)                # capture total number of tickets
            desired_fields = ["requester_id", "assignee_id", "subject", "description", "tags"]
            # This list of desired_fields could be used to create another feature where the user adds
            # fields to their ticket display. Given the tickets.json file for this challenge, I selected
            # only those fields for the ticket display that were populated with (non-default) data.
            ticket_break = max_width * "_"      # dynamically updates line break to match max_width
            print(ticket_break)
            for id in tickets:
                print(f"[Ticket ID #{id}]")     # key value for python ticket dictionary
                count += 1
                for key in desired_fields:
                    key_text = format_key_display(key)      # format presentation of each key for pretty printing
                    print(f"{key_text}", end="")
                    if type(tickets[id][key]) is str:
                        if key == "description":            # handle the large text block of description
                            print("\n", end="")             # by inserting a new line to preserve maxwidth
                        text = wrap(tickets[id][key], width=max_width)
                        for line in text:
                            print(line)
                        print("\n", end="")
                    elif type(tickets[id][key]) is list:    # formats data that is received as a list; Ex. Tags
                        for item in tickets[id][key]:
                            if item == list(tickets[id][key])[-1]:  # formats printing of list as comma separated values
                                print(f"{item} ", end="")           # prevents comma placement at end of list
                            else:
                                print(f"{item}, ", end="")
                    else:                                   # not a string or a list, print the integer
                        print(tickets[id][key])
                print("\n", "\n", end="")
                print(self.add_API_timestamp(id))           # add timestamp of every API call to the ticket display
                print(ticket_break)
                id_list = list(tickets)                     # used to index ticket id numbers for descriptive user messages
                if count % page == 0:                       # tracks the pagination of ticket displays
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
                if total < page and total == count:     # if fewer tickets are being displayed than the pagination value
                    if total == 1:                      # and the last ticket has been printed, display message
                        print(f"There is {total} ticket displayed.")
                        print("\n", end="")
                    else:
                        print(f"There are {total} tickets displayed.")
                        print("\n", end="")
            self._search_results = None                 # restore search_results data member to None

    def search_subject(self, search_term):
        """
        This method accepts a search_term as a parameter and searches
        all ticket subject fields for the search term. This method updates
        the "search_results" data member with the search_results, if there are any,
        otherwise it displays a descriptive message for the user and returns.
        Given search_results, this method displays the number of tickets that
        contain the search term in the subject field.
        """
        search_results = {}
        for ticket in self._tickets:    # the search methods could be made to be modular by passing a parameter with a string
            if search_term in self._tickets[ticket]["subject"].lower():  # for the desired search field
                search_results[ticket] = self._tickets[ticket]           # given more time, that would be my choice
        total = len(search_results)                                      # in addition to offering multiple field searches
        if total == 0:
            print(f"There are no results that match your subject search for: {search_term}")
        else:
            print(f"There are {total} tickets that match your subject search for: {search_term}")
            sleep(2)
            self._search_results = search_results   # search_results have precedence so, only update data member if

    def search_description(self, search_term):
        """
        This method accepts a search_term as a parameter and searches
        all ticket description fields for the search term. This method updates
        the "search_results" data member with the search_results, if there are any,
        otherwise it displays a descriptive message for the user and returns.
        Given search_results, this method displays the number of tickets that
        contain the search term in the description field.
        """
        search_results = {}             # clone of search_subject for description field
        for ticket in self._tickets:
            if search_term in self._tickets[ticket]["description"].lower():
                search_results[ticket] = self._tickets[ticket]
        total = len(search_results)
        if total == 0:
            print(f"There are no results that match your description search for: {search_term}")
        else:
            print(f"There are {total} tickets that match your description search for: {search_term}")
            sleep(2)
            self._search_results = search_results   # only update data member if search_results exist

    def search_tags(self, search_term):
        """This method accepts a search_term as a parameter and searches
        all ticket tags for the search term. This method updates
        the "search_results" data member with the search_results, if there are any,
        otherwise it displays a descriptive message for the user and returns.
        Given search_results, this method displays the number of tickets that
        contain the search term in the tags field."""
        search_results = {}
        for ticket in self._tickets:
            if search_term in self._tickets[ticket]["tags"]:
                search_results[ticket] = self._tickets[ticket]      # construct dictionary output to fit parameters
        total = len(search_results)                                 # of display_tickets()
        if total == 0:
            print(f"There are no results that match your tag search for: {search_term}")
        else:
            print(f"There are {total} tickets that match your tag search for: {search_term}")
            sleep(2)
            self._search_results = search_results   # only update data member if search_results exist

    def search_ticket_id(self, id_number):
        """
        This method accepts an ID number as a parameter and searches
        all tickets for the ID number. This method updates
        the "search_results" data member with the search_results, if there are any,
        otherwise it displays a descriptive message for the user and returns.
        The id_number is validated in main() to fall in the range of available ticket IDs.
        This choice of external validation allows for re-prompting of the user for valid input.
        Given search_results, this method displays when the ticket has been found.
        """
        search_results = {}
        try:
            search_results[id_number] = self._tickets[id_number]
        except KeyError:        # should an id number be passed that triggers a dictionary KeyError
            print(f"Ticket #{id_number} cannot be found.")
        total = len(search_results)
        if total == 0:
            print(f"There are no results that match your ticket ID search for #{id_number}.")
        else:
            print(f"Ticket #{id_number} has been retrieved.")
            sleep(2)
            self._search_results = search_results       # only update data member if search_results exist


def format_key_display(key):
    """
    This function accepts a string as a parameter and formats
    the string for pretty printing by the display_tickets() method
    in the ZendeskTicket class. Formatting includes adding spacing offsets,
    removing underscores, and adding a colon to the output.
    Returns formatted string.
    """
    offset = 15         # offset value determines the indentation of all data following the printing
    length = len(key)   # of category fields in the display_tickets() method; does not apply to "description"
    diff = offset - length
    space_string = diff * " "
    key = key.replace("_", " ")
    key = key.title()
    key += ":"
    key += space_string
    return key


def display_menu():
    """
    This function displays a menu of choices that are methods of the
    ZendeskTicket class. This function is called by main().
    This function validates the user_input, and reprompts the user for alternate
    input if it cannot validate it. Returns the validated input to main()
    or an additional call of display_menu() to reprompt the user.
    """
    low = 1         # values allow easy updating of int validation
    high = 8
    print("\n", end="")
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
    for key in menu:                        # input validation could also be as a menu dictionary call
        print(f"{key} : {menu[key]}")       # in the form of a Try: / Except KeyError:
    selection = input().strip()             # where the KeyError causes a reprompt of the user
    if selection.lower() == "q":
        return selection
    elif selection.isnumeric() and low <= int(selection) <= high:
        selection = int(selection)
        return selection
    else:
        print("\n", end="")
        print("* Invalid selection. Please try again. *")
        return display_menu()


if __name__ == "__main__":

    user_engaged = True
    zt = ZendeskTicket()    # create ZendeskTicket object
    zt.get_tickets()        # populate "tickets" data member with python dictionary of tickets
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
            if zt.get_search_results() is not None:
                zt.display_tickets()
        elif user_input == 4:  # search tickets by description
            print("Please enter the * DESCRIPTION * search term.")
            search_term = input().strip().lower()
            zt.search_description(search_term)
            if zt.get_search_results() is not None:
                zt.display_tickets()
        elif user_input == 5:  # search tickets by tag identifier
            zt.get_tags_info()  # display the tags for reference
            print("Please enter the * TAGS * search term.")
            search_term = input().strip().lower()
            zt.search_tags(search_term)
            if zt.get_search_results() is not None:
                zt.display_tickets()
        elif user_input == 6:  # search tickets by ticket id number
            ticket_ids = list(zt.get_ticket_data())
            first_ticket = ticket_ids[0]    # used to validate ticket id number
            last_ticket = ticket_ids[-1]
            searching = True
            while searching:
                print(f"You have Ticket IDs in the range of #{first_ticket} to #{last_ticket}.")
                print(f"Please enter the * TICKET ID * number.")
                id_number = input().strip()
                if id_number.isnumeric() and first_ticket <= int(id_number) <= last_ticket:
                    searching = False       # if ticket id number is valid, retrieve ticket
                    zt.search_ticket_id(int(id_number)) # this method calls display_tickets()
                elif id_number.lower() == "q":
                    searching = False
                else:
                    print("\n", end="")
                    print("Invalid entry. Please try again or enter 'Q' to quit.")  # reprompt user
        elif user_input == 7:  # update local tickets from zendesk api
            zt.get_tickets()
            print("* Your Zendesk API call was successful! *")
        elif user_input == 8:  # change number of tickets displayed per page scroll
            print(f"You are currently seeing {zt.get_page_display()} ticket(s) per page.")
            print("Please enter a number in the range of 1 to 25 -or- press any key to keep the default value.")
            page_input = input().strip()
            if page_input.isnumeric() and 0 < int(page_input) < 26:
                zt.set_page_display(int(page_input))
            print("\n", end="")
            print(f"* You will see {zt.get_page_display()} ticket(s) per page. *")
        else:  # quit program; display_menu() validates data so this is the user selecting q or Q
            user_engaged = False
            print("Thank you for using the Zendesk Ticket Viewer. Goodbye!")
