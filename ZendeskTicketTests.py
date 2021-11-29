import unittest
from ZendeskCodingChallenge import ZendeskTicket
from TestTickets import tickets


class UnitTests(unittest.TestCase):

    def test_init_tickets(self):
        """
        This test confirms the "tickets" data member is initialized as None.
        """
        zt = ZendeskTicket()
        self.assertIsNone(zt._tickets)

    def test_init_search_results(self):
        """
        This test confirms the "search_results" data member is initialized as None.
        """
        zt = ZendeskTicket()
        self.assertIsNone(zt._search_results)

    def test_get_tickets(self):
        """
        This test confirms that the "tickets" data member populates via an API
         call with the 100 tickets loaded to the Zendesk account from the tickets.json file.
         This test will fail if the tickets.json data is not first posted to the user's account.
         """
        zt = ZendeskTicket()
        zt.get_tickets()
        number_of_tickets = len(zt._tickets)
        self.assertIsNotNone(zt._tickets)
        self.assertEqual(number_of_tickets, 100)

    def test_get_ticket_data(self):
        """
        This test confirms that the "tickets" data member and the
        "tickets" get method produce the same result.
        """
        zt = ZendeskTicket()
        zt.get_tickets()
        self.assertIs(zt._tickets, zt.get_ticket_data())

    def test_get_page_display(self):
        """
        This test confirms that the get_page_display method
        returns the default page_display value of 25.
        """
        zt = ZendeskTicket()
        self.assertEqual(zt.get_page_display(), 25)

    def test_set_page_display(self):
        """
        This test confirms that the set_page display method
        updates the "page_display" data member.
        """
        zt = ZendeskTicket()
        zt.set_page_display(17)
        self.assertEqual(zt.get_page_display(), 17)

    def test_get_tags_info(self):
        """
        This test confirms that given a small ticket dictionary (attached)
        the get_tags_info method populates the "tags" data member with accurate results.
        """
        zt = ZendeskTicket()
        self.assertIsNone(zt._tags)
        zt._tickets = tickets
        zt.get_tags_info()
        self.assertEqual(zt._tags, {'a': 1, 'b': 1, 'c': 1, 'gazelle': 1, 'giraffe': 3, 'hippo': 1, 'rhino': 1})

    def test_search_subject(self):
        """
        This test confirms that given a sample ticket dictionary (attached),
        and the search term "zen", the search_subject method only finds and populates
        the "search_results" data member with one ticket.
        """
        zt = ZendeskTicket()
        zt._tickets = tickets
        zt.search_subject("zen")
        num = len(zt._search_results)
        self.assertEqual(num, 1)
        for key in zt._search_results:
            ticket = zt._search_results[key]
        self.assertEqual(ticket["subject"], "z is for zen")

    def test_search_description(self):
        """
        This test confirms that given a sample ticket dictionary (attached),
        and the search term "stellar", the search_description method only finds and populates
        the "search_results" data member with one ticket.
        """
        zt = ZendeskTicket()
        zt._tickets = tickets
        zt.search_description("stellar")
        num = len(zt._search_results)
        self.assertEqual(num, 1)
        for key in zt._search_results:
            ticket = zt._search_results[key]
        self.assertEqual(ticket["subject"], "m is for michelle")

    def test_search_tags(self):
        """
        This test confirms that given a sample ticket dictionary (attached),
        and the search term "hippo", the search_tags method only finds and populates
        the "search_results" data member with one ticket.
        """
        zt = ZendeskTicket()
        zt._tickets = tickets
        zt.search_tags("hippo")
        num = len(zt._search_results)
        self.assertEqual(num, 1)
        for key in zt._search_results:
            ticket = zt._search_results[key]
        self.assertEqual(ticket["subject"], "a is for apple")

    def test_search_ticket_id(self):
        """
        This test confirms that given a sample ticket dictionary (attached),
        and the ticket id #1, the search_ticket_id method only finds and populates
        the "search_results" data member with one ticket.
        """
        zt = ZendeskTicket()
        zt._tickets = tickets
        zt.search_ticket_id(1)
        num = len(zt._search_results)
        self.assertEqual(num, 1)
        for key in zt._search_results:
            ticket = zt._search_results[key]
        self.assertEqual(ticket["description"], "Watch this fruit fall to discover the laws of gravity.")
