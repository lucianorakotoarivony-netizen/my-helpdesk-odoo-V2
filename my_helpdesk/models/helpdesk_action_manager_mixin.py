from odoo import models, fields
from odoo.exceptions import UserError

class HelpdeskActionManagerMixin(models.AbstractModel):
    _name="helpdesk.action.manager.mixin"
    _description="actions des managers"

    """Le manager créer le ticket, le valide puis l'envoi. C'est au moment de l'envoi que l'état sera mis en nouveau.""" 
    def action_validate(self) -> None: 
        """Va servir à valider le ticket. Met tous les champs en readonly.
La validation est différente de l'envoie donc on ne change pas l'état du ticket.""" 
        self.ensure_one() 
        if self.is_validated:
            raise UserError(self._USER_ERROR_MSG) 
        self.write({"is_validated":True})

    def action_manager_cancel(self): 
        """Permettra au manager de retirer un ticket, par exemple le problème, c'est résolu tout seul.""" 
        self.ensure_one() 
        if not self.state in ["new","cancelled"]: 
            raise UserError(self._USER_ERROR_MSG) 
        """On repasse le ticket en draft pour le supprimer de la vue du tech. Le manager pourra ensuite supprimer le ticket sans soucis."""
        self.write({"state":"draft", "reason_for_cancellation":False })
        self.env["helpdesk.notifier.technicien"].notifier_cancellation_by_manager(self)

    def action_modify(self) -> None: 
        """Une fois le ticket validé, on pourra modifier avant de l'envoyer. Remets is_validated en False.""" 
        self.ensure_one() 
        if not self.is_validated: 
            raise UserError(self._USER_ERROR_MSG) 
        self.write({"is_validated":False})

    def action_send(self) -> None:
        """Envoie le ticket pour le rendre disponible dans la vue tech."""
        self.ensure_one()
        if not self.is_validated:
            raise UserError(self._USER_ERROR_MSG)
        self.write({
            "state": "new",
            "validated_by_id": self.env.user.id,
            "validation_date": fields.Datetime.now()
        })
        self.env["helpdesk.notifier.technicien"].notifier_new_ticket()
    
    def action_cancellation_request(self):
        """Permettra au manager de demander une annulation d'un ticket en cours. Exemple le problème, c'est résolu seul."""
        self.ensure_one()
        if self.state != "in_progress":
            raise UserError(self._USER_ERROR_MSG)
        return{
            "name":"Demande d'annulation du ticket en cours",
            "res_model":"helpdesk.cancellation.request.wizard",
            "type":"ir.actions.act_window",
            "view_mode":"form",
            "target":"new",
            "context":{"default_tickets_id":self.id}
        }
    