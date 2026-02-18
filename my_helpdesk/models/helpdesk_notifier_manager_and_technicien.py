
from odoo import models
class HelpDeskNotifierManagerAndTechnicien(models.AbstractModel):
    _name="helpdesk.notifier.manager.and.technicien"
    _description="Notitication pour les deux"

    def notifier_ticket_done(self,ticket):
        """Cette méthode n'enverra pas nécessairement une notification pour les deux.
            Pour éviter les mauvaises surprises, je préfère laisser comme ça."""
        MANAGER_GROUP = 'my_helpdesk.group_my_helpdesk_manager'
        group = self.env.ref(MANAGER_GROUP, raise_if_not_found=False)
        if group:
            if ticket.reason_for_cancellation:
                for user in group.user_ids:
                    self.env['bus.bus']._sendone(
                    user.partner_id,
                'simple_notification',
                {
                'type': 'info',
                'title': f"🔔 Le ticket {ticket.display_name} a été résolu par {self.env.user.name}. Visiblement, il n'a pas peur de toi. Muscle-toi un peu.",
                'sticky': True,
                }
        )
                self.env['bus.bus']._sendone(
                self.env.user.partner_id,
                'simple_notification',
                {
                'type': 'info',
                'title': f"🔔 Alors toi, tu devras t'expliquer auprès du manager. Fais gaffe, je lui ai conseillé de se muscler un peu.",
                'sticky': True,
                }
        )
            else:
                for user in group.user_ids:
                    self.env['bus.bus']._sendone(
                    user.partner_id,
                'simple_notification',
                {
                'type': 'info',
                'title': f'🔔 Le ticket {ticket.display_name} a été résolu par {self.env.user.name}',
                'sticky': True,
                }
        )
                    
    def notifier_ticket_in_progress(self):
        """Un doux rappel au tech et manager qu'un ticket met du temps à être résolu."""
        domain=[("state","=","in_progress")]
        ticket_in_progress=self.env["helpdesk.ticket"].search_count(domain)
        if ticket_in_progress>0:
            tickets_list= self.env['helpdesk.ticket'].search([
        ('state', '=', 'in_progress')])
            for ticket in tickets_list:
                self.env['bus.bus']._sendone(
                    ticket.assigned_to_id.partner_id,
                'simple_notification',
                {
                'type': 'info',
                'title': f'🔔 Ne te presse surtout pas {ticket.customer_name} est sur le point de battre son record sur Candy Crush.',
                'sticky': True,
                })

                self.env['bus.bus']._sendone(
                    ticket.validated_by_id.partner_id,
                'simple_notification',
                {
                'type': 'info',
                'title': f"🔔 Et si on allait encourager {ticket.customer_name} dans sa partie de Candy Crush. {ticket.assigned_to_id.name} à l'air de prendre tout son temps.",
                'sticky': True,
                })