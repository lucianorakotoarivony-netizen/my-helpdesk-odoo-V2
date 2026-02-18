
from odoo.tests import TransactionCase
from odoo.exceptions import UserError

class TestHelpdeskActionManager(TransactionCase):
    
    def test_creation_ticket(self): #1
        ticket=self.env["helpdesk.ticket"].create({"customer_name":"Luciano","title":"Problème d'argent"})
        self.assertEqual(ticket.customer_name,"Luciano")
        self.assertEqual(ticket.title,"Problème d'argent")
        self.assertEqual(ticket.priority,"1")
        self.assertEqual(ticket.state,"draft")

    def test_action_validate(self):#2
        ticket=self.env["helpdesk.ticket"].create({"customer_name":"Luciano","title":"Problème d'argent"})
        ticket.action_validate()
        self.assertTrue(ticket.is_validated)
        self.assertEqual(ticket.state,"draft")

    def test_action_send_without_action_validate(self):#3
        ticket=self.env["helpdesk.ticket"].create({"customer_name":"Hacker","title":"Forcing"})
        with self.assertRaises(UserError):
            ticket.action_send()
        self.assertEqual(ticket.state,"draft")
        self.assertFalse(ticket.is_validated)

    def test_action_send(self):#4
        ticket=self.env["helpdesk.ticket"].create({"customer_name":"Luciano","title":"Problème d'argent"})
        ticket.action_validate()
        ticket.action_send()
        self.assertEqual(ticket.state,"new")

    def test_action_manager_cancel_ticket_with_state_new(self):#5
        ticket=self.env["helpdesk.ticket"].create({"customer_name":"Luciano","title":"Problème d'argent"})
        ticket.action_validate()
        ticket.action_send()
        ticket.action_manager_cancel()
        self.assertEqual(ticket.state,"draft")

    def test_action_manager_cancel_ticket_with_state_in_progress(self):#6
        ticket=self.env["helpdesk.ticket"].create({"customer_name":"Luciano","title":"Problème d'argent"})
        ticket.action_validate()
        ticket.action_send()
        ticket.action_in_progress()
        with self.assertRaises(UserError):
            ticket.action_manager_cancel()
        self.assertEqual(ticket.state,"in_progress")

    def test_action_manager_cancel_ticket_with_state_done(self):#7
        ticket=self.env["helpdesk.ticket"].create({"customer_name":"Luciano","title":"Problème d'argent"})
        ticket.action_validate()
        ticket.action_send()
        ticket.action_in_progress()
        ticket.action_done()
        with self.assertRaises(UserError):
            ticket.action_manager_cancel()
        self.assertEqual(ticket.state,"done")

    def test_action_modify_without_validate(self):#8
        ticket=self.env["helpdesk.ticket"].create({"customer_name":"Luciano","title":"Problème d'argent"})
        with self.assertRaises(UserError):
            ticket.action_modify()
        self.assertFalse(ticket.is_validated)

    def test_action_send_after_modify_without_validate(self):#9
        ticket=self.env["helpdesk.ticket"].create({"customer_name":"Luciano","title":"Problème d'argent"})
        ticket.action_validate()
        ticket.action_modify()
        with self.assertRaises(UserError):
            ticket.action_send()
        self.assertFalse(ticket.is_validated)

    def test_unlink_ticket_not_draft(self):#10
        ticket=self.env["helpdesk.ticket"].create({"customer_name":"Luciano","title":"Problème d'argent"})
        ticket.action_validate()
        ticket.action_send()
        with self.assertRaises(UserError):
            ticket.unlink()
        self.assertEqual(ticket.state,"new")