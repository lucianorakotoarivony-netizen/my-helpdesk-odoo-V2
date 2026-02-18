
from odoo.tests import TransactionCase
from odoo.tests.common import users
from odoo.exceptions import AccessError
class HelpdeskSecurity(TransactionCase):
    def setUp(self):
        super().setUp()
        group_tech = self.env.ref('my_helpdesk.group_my_helpdesk_technicien')
        self.tech_user_jean = self.env['res.users'].create({
        'name': 'Jean Tech',
        'login': 'jean_tech',
        'group_ids': [(6, 0, [group_tech.id])]
    })
        self.tech_user_casper = self.env['res.users'].create({
        'name': 'Casper le gentil fantôme',
        'login': 'Casper',
        'group_ids': [(6, 0, [group_tech.id])]
    })
        self.ticket_draft=self.env["helpdesk.ticket"].create({"customer_name":"Luciano","title":"Problème d'argent"})

        self.ticket_validate=self.env["helpdesk.ticket"].create(
            {"customer_name":"Luciano","title":"Problème d'argent","is_validated":True})
        
        self.ticket_send=self.env["helpdesk.ticket"].create(
            {"customer_name":"Luciano","title":"Problème d'argent","is_validated":True, "state":"new"})
        
        self.ticket_in_progress_assigned_to_casper=self.env["helpdesk.ticket"].create(
            {"customer_name":"Luciano","title":"Problème d'argent",
             "is_validated":True, "state":"in_progress", "assigned_to_id":self.tech_user_casper.id})
        
    @users("jean_tech")
    def test_tech_create_ticket(self):#1
        """Vérifie que le tech ne peut pas créer de ticket"""
        with self.assertRaises(AccessError):
            ticket=self.env["helpdesk.ticket"].create({"customer_name":"Luciano","title":"Problème d'argent"})

    @users("jean_tech")
    def test_blind_tech_for_draft_ticket(self):#2
        """Verifie que le tech ne voit pas les brouillons"""
        ticket_draft_not_validated=self.env["helpdesk.ticket"].browse(self.ticket_draft.id)
        ticket_draft_validated=self.env["helpdesk.ticket"].browse(self.ticket_validate.id)
        with self.assertRaises(AccessError):
            self.assertEqual(ticket_draft_not_validated.state,"draft")
            self.assertEqual(ticket_draft_validated.state,"draft")

    @users("jean_tech")
    def test_can_read_new_ticket(self):#3
        """On vérifie quand même que le tech peut voir les nouveaux"""
        ticket_new=self.env["helpdesk.ticket"].browse(self.ticket_send.id)
        self.assertEqual(ticket_new.state,"new")
    
    @users("jean_tech")
    def test_tech_can_only_read_his_ticket(self):#4
        ticket_in_progress=self.env["helpdesk.ticket"].browse(self.ticket_in_progress_assigned_to_casper.id)
        # Je tente de comparer des valeurs, j'ai besoin de lire le ticket.
        # Normalement, je devrais être bloqué car je n'ai pas le droit de lecture
        # en tant que tech sur un ticket brouillon.
        with self.assertRaises(AccessError):
            self.assertEqual(ticket_in_progress.state,"in_progress")
    
    @users("Casper")
    def test_can_read_his_ticket(self):#5
        ticket_in_progress=self.env["helpdesk.ticket"].browse(self.ticket_in_progress_assigned_to_casper.id)
        self.assertEqual(ticket_in_progress.state,"in_progress")
    