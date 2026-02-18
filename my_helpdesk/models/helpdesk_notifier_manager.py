from odoo import models
class HelpdeskNotifierManager(models.AbstractModel):
    _name="helpdesk.notifier.manager"
    _description="Notification pour le manager"
    def notifier_ticket_taken_care_of(self, ticket):
        MANAGER_GROUP = 'my_helpdesk.group_my_helpdesk_manager'
        group = self.env.ref(MANAGER_GROUP, raise_if_not_found=False)
        if group:
            for user in group.user_ids:
                self.env['bus.bus']._sendone(
                user.partner_id,
                'simple_notification',
                {
                'type': 'info',
                'title': f'🔔 Ticket pris en charge par {ticket.assigned_to_id.name}.',
                'sticky': True,
                }
        )
    def notifier_cancellation_by_tech(self, ticket):
        MANAGER_GROUP = 'my_helpdesk.group_my_helpdesk_manager'
        group = self.env.ref(MANAGER_GROUP, raise_if_not_found=False)
        if group:
            for user in group.user_ids:
                self.env['bus.bus']._sendone(
                user.partner_id,
                'simple_notification',
                {
                'type': 'info',
                'title': f'🔔 Le ticket {ticket.display_name} a été annulé par {self.env.user.name}',
                'sticky': True,
                }
        )