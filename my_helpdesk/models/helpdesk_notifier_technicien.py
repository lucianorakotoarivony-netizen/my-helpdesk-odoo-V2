
from odoo import models
class HelpdeskNotifierTechinicien(models.AbstractModel):
    _name="helpdesk.notifier.technicien"
    _description="Notification pour les techs"

    def notifier_new_ticket(self):
        TECH_GROUP = 'my_helpdesk.group_my_helpdesk_technicien'
        group = self.env.ref(TECH_GROUP, raise_if_not_found=False)
        if group:
            for user in group.user_ids:
                self.env['bus.bus']._sendone(
                user.partner_id,
                'simple_notification',
                {
                'type': 'info',
                'title': '🔔 Nouveau ticket disponible',
                'sticky': True,
                }
        )
    def notifier_cancellation_by_manager(self, ticket):
        TECH_GROUP = 'my_helpdesk.group_my_helpdesk_technicien'
        group = self.env.ref(TECH_GROUP, raise_if_not_found=False)
        if group:
            for user in group.user_ids:
                self.env['bus.bus']._sendone(
                user.partner_id,
                'simple_notification',
                {
                'type': 'info',
                'title': f'🔔 Le ticket {ticket.display_name} a été retiré par le manager.',
                'sticky': True,
                }
        )
    def notifier_cancellation_request(self,ticket):
        if ticket.assigned_to_id:
            self.env['bus.bus']._sendone(
            ticket.assigned_to_id.partner_id,
            'simple_notification',
            {
                'type': 'warning',  # ← Warning car c'est une annulation
                'title': "🔔 Demande d'annulation",
                'message': f"Le manager demande d'annuler : {ticket.display_name}",
                'sticky': True,
            }
        )
    def ticket_pending(self):
        """Notification automatique si un ou plusieurs nouveaux tickets sont en attente depuis longtemps."""
        domain=[("state","=","new")]
        ticket_pending=self.env["helpdesk.ticket"].search_count(domain)
        if ticket_pending>0:
            message=f"🔔 Ne vous battez surtout pas. Il n'y a que {ticket_pending} en attente."
            TECH_GROUP = 'my_helpdesk.group_my_helpdesk_technicien'
            group = self.env.ref(TECH_GROUP, raise_if_not_found=False)
            if group:
                for user in group.user_ids:
                    self.env['bus.bus']._sendone(
                    user.partner_id,
                        'simple_notification',
                        {
                        'type': 'info',
                        'title': message,
                        'sticky': True,
                        })
