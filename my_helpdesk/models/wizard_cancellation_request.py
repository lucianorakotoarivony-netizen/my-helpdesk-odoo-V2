from odoo import models, fields

class HelpdeskCancellationRequestWizard(models.TransientModel):
    _name="helpdesk.cancellation.request.wizard"
    _description="Fenêtre pour envoyer une demande d'annulation d'un ticket en cours."
    reason_for_cancellation=fields.Text(string="Motif d'annulation", required=True)
    tickets_id=fields.Many2one("helpdesk.ticket", string="Ticket concerné")
    def action_send_cancellation_request(self):
        self.tickets_id.write({"reason_for_cancellation":self.reason_for_cancellation})
        # 2. Envoi du signal au Bus pour la réactivité OWL
        channel = f"helpdesk.ticket/{self.tickets_id.id}"
        # On envoie le type 'cancellation_request' attendu par le JS
        self.env['bus.bus']._sendone(channel, 'cancellation_request', {
            'reason': self.tickets_id.reason_for_cancellation
        })
        
        self.env["helpdesk.notifier.technicien"].notifier_cancellation_request(self.tickets_id)
        # Optionnel : Fermer le wizard après validation
        return {'type': 'ir.actions.act_window_close'}