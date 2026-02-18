
from odoo.tests import TransactionCase
from odoo.exceptions import UserError

class TestHelpdeskActionTech(TransactionCase):

    def test_action_in_progress(self):#1
        """Le tech ne voit que les tickets new donc le test doit passer"""
        ticket=self.env["helpdesk.ticket"].create({"customer_name":"Luciano","title":"Problème d'argent"})
        ticket.action_validate()
        ticket.action_send()
        ticket.action_in_progress()
        self.assertEqual(ticket.state,"in_progress")
    
    def test_action_done_after_in_progress(self):#2
        ticket=self.env["helpdesk.ticket"].create({"customer_name":"Luciano","title":"Problème d'argent"})
        ticket.action_validate()
        ticket.action_send()
        ticket.action_in_progress()
        ticket.action_done()
        self.assertEqual(ticket.state,"done")

    def test_action_done_without_action_in_progress(self):#3
        ticket=self.env["helpdesk.ticket"].create({"customer_name":"Luciano","title":"Problème d'argent"})
        ticket.action_validate()
        ticket.action_send()
        with self.assertRaises(UserError):
            ticket.action_done()
        self.assertEqual(ticket.state,"new")
    
    def test_action_tech_cancel_without_reason_for_cancellation(self):#4
        ticket=self.env["helpdesk.ticket"].create({"customer_name":"Luciano","title":"Problème d'argent"})
        ticket.action_validate()
        ticket.action_send()
        ticket.action_in_progress()
        ticket.action_tech_cancel()
        self.assertEqual(ticket.state,"new")
        self.assertFalse(ticket.assigned_to_id)

    def test_action_tech_cancel_when_state_not_in_progress(self):#5
        ticket=self.env["helpdesk.ticket"].create({"customer_name":"Luciano","title":"Problème d'argent"})
        ticket.action_validate()
        ticket.action_send()
        with self.assertRaises(UserError):
            ticket.action_tech_cancel()
        self.assertEqual(ticket.state,"new")

    def test_action_tech_cancel_with_reason_for_cancellation(self):#6
        ticket=self.env["helpdesk.ticket"].create({"customer_name":"Luciano","title":"Problème d'argent"})
        ticket.action_validate()
        ticket.action_send()
        ticket.action_in_progress()
        ticket.write({
        "reason_for_cancellation": "Problème résolu tout seul"
    })
        ticket.action_tech_cancel()
        self.assertEqual(ticket.state,"cancelled")
        self.assertFalse(ticket.assigned_to_id)


