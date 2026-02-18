from odoo import fields, models, api
from odoo.exceptions import UserError

class HelpDeskTickets(models.Model): 
    _USER_ERROR_MSG="Tu pourrais pas être sérieux deux secondes et utiliser uniquement les boutons que je te donnes? Par contre, cela peut être une désynchronisation donc sorry. My bad"
    _name="helpdesk.ticket"
    _inherit=["helpdesk.action.tech.mixin","helpdesk.action.manager.mixin","mail.thread","mail.activity.mixin"]
    _description="Ticket Helpdesk" 
    customer_name=fields.Char(string="Nom",required=True, help="Nom de celui qui a un problème") 
    title=fields.Char(string="Sujet", required=True, help="Exemple : Problème clavier") 
    description=fields.Text(string="Description", help="Faut vraiment un help?") 
    priority=fields.Selection(selection=[("0", 'Basse'), ("1", 'Moyenne'), ("2", 'Haute')], string="Priorité", default="1")
    state=fields.Selection(selection=[ ('draft', 'brouillon'), ('new', 'Nouveau'), ('in_progress', 'En cours'), ('done', 'Résolu'),('cancelled','Annuler') ], string="Etat", default='draft', readonly=True) 
    is_validated=fields.Boolean(string="Validé", default=False, copy=False) 
    validated_by_id=fields.Many2one("res.users", string="Validé par : ", store=True, readonly=True) 
    validation_date=fields.Datetime(string="Validé le : ", readonly=True)
    assigned_to_id=fields.Many2one("res.users", string="Pris en charge par : ", store=True, readonly=True)
    reason_for_cancellation=fields.Text(string="Motif d'annulation", readonly=True)
    
    @api.depends("customer_name","title") 
    def _compute_display_name(self): 
        for ticket in self: 
            id_part=ticket.id 
            client_part=ticket.customer_name 
            title_part=ticket.title 
            if not ticket.id: 
                """Je vide display_name pour ne pas avoir un truc moche lors de la création. Logique, pas de ticket crée, pas d'ID."""
                ticket.display_name="" 
            else: 
                ticket.display_name=f"Ticket / {id_part} / {client_part} / {title_part}"

    def unlink(self):
        """Ceci est un choix de design. On ne peut que supprimer les brouillons. Seul l'état done ne peut revenir en arrière."""
        for record in self:
            if record.state != "draft":
                raise UserError("Tu ne peux supprimer que les brouillons. Donc si tu veux le supprimer ... Repasse le brouillon si tu ne peux pas, vas en toucher deux mots au dev.")
        return super().unlink()

