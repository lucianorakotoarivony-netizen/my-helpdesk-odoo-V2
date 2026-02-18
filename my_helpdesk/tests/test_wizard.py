
from odoo.tests import TransactionCase

class TestHelpdeskConfirmWizard(TransactionCase):
    def test_action_in_progress_a_ticket_with_priority_low_when_high_priority_exist(self):#1
        """Le but c'est de tester qu'un pop up s'ouvre bien si le tech tente d'executer un ticket avec une priorité basse alors qu'une priorité haute existe
        Accessoirement, on va également vérifier que l'état du ticket est inchangé"""
        ticket_low=self.env["helpdesk.ticket"].create({"customer_name":"Ticket bas","title":"Pas important", "priority":"0","state":"new"})
        ticket_high=self.env["helpdesk.ticket"].create({"customer_name":"Ticket haut","title":"Pas important", "priority":"2","state":"new"})
        result=ticket_low.action_in_progress_verifying_priority()
        domain=[("priority",">",ticket_low.priority),("state","not in",["done"])]
        higher_priority_count=self.env["helpdesk.ticket"].search_count(domain)
        self.assertIsInstance(result,dict)
        self.assertEqual(ticket_low.state,"new")
        self.assertEqual(result,{
                "name":f"Je dis ça, je dis rien mais, il y a {higher_priority_count} tickets plus urgent parmi les nouveaux",
                "res_model":"helpdesk.confirm.wizard",
                "view_mode":"form",
                "target":"new",
                "type":"ir.actions.act_window",
                "context":{"default_tickets_id":ticket_low.id,
                "step":1,
                "urgent_count":higher_priority_count}
            })
    def test_action_in_progress_a_ticket_with_higher_priority(self):#2
        """Le but c'est de montrer qu'un ticket avec la priorité ne déclenche pas le wizard"""
        ticket_high=self.env["helpdesk.ticket"].create({"customer_name":"Ticket haut","title":"Pas important", "priority":"2","state":"new"})
        result=ticket_high.action_in_progress_verifying_priority()
        self.assertNotIsInstance(result,dict)
        self.assertEqual(ticket_high.state,"in_progress")
    
    def test_three_pop_up(self):#3
        """Ici on suppose que le tech cliquera sur continuer à chaque fois."""
        ticket_low=self.env["helpdesk.ticket"].create({"customer_name":"Ticket bas","title":"Pas important", "priority":"0","state":"new"})
        ticket_high=self.env["helpdesk.ticket"].create({"customer_name":"Ticket haut","title":"Pas important", "priority":"2","state":"new"})
        step_one=ticket_low.action_in_progress_verifying_priority()
        domain=[("priority",">",ticket_low.priority),("state","not in",["done"])]
        higher_priority_count=self.env["helpdesk.ticket"].search_count(domain)
        self.assertIsInstance(step_one,dict)
        self.assertEqual(ticket_low.state,"new")
        self.assertEqual(step_one,{
                "name":f"Je dis ça, je dis rien mais, il y a {higher_priority_count} tickets plus urgent parmi les nouveaux",
                "res_model":"helpdesk.confirm.wizard",
                "view_mode":"form",
                "target":"new",
                "type":"ir.actions.act_window",
                "context":{"default_tickets_id":ticket_low.id,
                "step":1,
                "urgent_count":higher_priority_count}
            })
        wizard=self.env["helpdesk.confirm.wizard"].create({"tickets_id":ticket_low.id})#Ce truc va me permettre d'utiliser la méthode action_next_step sur mon ticket
        step_two=wizard.with_context(step=2).action_next_step()#on est à l'étape 2 mais ici on va retourner le pop up de l'étape 3
        self.assertIsInstance(step_two,dict)#on vérifie que c'est bien un dict
        self.assertEqual(ticket_low.state,"new")
        self.assertEqual(step_two,{
                "name":"Je répète, il y a plus urgent",
                "res_model":"helpdesk.confirm.wizard",
                "view_mode":"form",
                "target":"new",
                "type":"ir.actions.act_window",
                "context":{"default_tickets_id":ticket_low.id, "step":3
                }
            })#Un peu optionnel mais permet de vérifier qu'on a bien le bon dictionnaire
        step_three=wizard.with_context(step=3).action_next_step()#On est à l'étape 3 donc ne devrait plus retourner un dict
        self.assertNotIsInstance(step_three,dict)#On vérifie que c'est pas un dict. Il peut être tout sauf un dict
        self.assertEqual(ticket_low.state,"in_progress")#Normalement, l'état devrait changer en in_progress