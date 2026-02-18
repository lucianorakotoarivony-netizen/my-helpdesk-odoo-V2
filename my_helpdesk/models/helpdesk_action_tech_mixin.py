from odoo import models
from odoo.exceptions import UserError

class HelpdeskActionTechMixin(models.AbstractModel):
    _name="helpdesk.action.tech.mixin"
    _description="action des techniciens"

    def action_in_progress(self) -> None:
        """Permet de débuter la tâche. Seuls les tickets qui auront pour état nouveau pourront être exécutés.""" 
        self.ensure_one() 
        if self.state!="new":
            raise UserError(self._USER_ERROR_MSG) 
        self.write({"state":"in_progress","assigned_to_id":self.env.user.id})
        self.env["helpdesk.notifier.manager"].notifier_ticket_taken_care_of(self)

    def action_in_progress_verifying_priority(self): 
        """Méthode qui va vérifier s'il y a un ticket plus urgent que celui qui est sélectionné. S'il y en a un pop-up devra apparaître sinon on appelle la méthode qui marquera le ticket comme en cours."""
        #Première étape voir si il y a plus urgent dans la db 
        self.ensure_one()
        domain=[("priority",">",self.priority),("state","not in",["done"])] 
        higher_priority_count=self.env["helpdesk.ticket"].search_count(domain) 
        # Ensuite, si il y a plus urgent, un pop up s'ouvre sinon on execute
        if higher_priority_count>0:
            return {
                    "name":f"Je dis ça, je dis rien mais, il y a {higher_priority_count} tickets plus urgent parmi les nouveaux",
                    "res_model":"helpdesk.confirm.wizard",
                    "view_mode":"form",
                    "target":"new",
                    "type":"ir.actions.act_window",
                    "context":{"default_tickets_id":self.id, "step":1, "urgent_count":higher_priority_count} }
        else:
            return self.action_in_progress()
        
    def action_progress_verifying_higher_priority_assigned(self):
        self.ensure_one()
        domain=[("priority",">",self.priority),("state","=","in_progress"), ("assigned_to_id","=",self.env.user.id)]
        higher_priority_assigned_count=self.env["helpdesk.ticket"].search_count(domain)
        if higher_priority_assigned_count>0:
            return{
                    "name":f"T'as pas déjà un ticket plus urgent à résoudre?",
                    "res_model":"helpdesk.confirm.wizard",
                    "view_mode":"form",
                    "target":"new",
                    "type":"ir.actions.act_window",
                    "context":{"default_tickets_id":self.id, "step":1, "urgent_count":higher_priority_assigned_count} }
        else:
            return self.action_in_progress_verifying_priority()
    
    def action_tech_cancel(self): 
        self.ensure_one()
        if self.state!="in_progress":
            raise UserError(self._USER_ERROR_MSG)
        if self.reason_for_cancellation:
            """Pour que les autres sachent que ce ticket a été annulé à la demande du manager donc personne ne peut plus le prendre."""
            self.write({"state":"cancelled","assigned_to_id":False})
        else:
            """Le tech annule, mais les autres peuvent le prendre."""
            self.write({"state":"new","assigned_to_id":False})
        self.env["helpdesk.notifier.manager"].notifier_cancellation_by_tech(self)
        
    def action_done(self) -> None: 
        """Marquer la tâche comme résolu. Seuls les tickets qui ont pour état in_progress pourront être marqué comme résolu.""" 
        self.ensure_one() 
        if self.state!="in_progress":
            raise UserError(self._USER_ERROR_MSG)
        acknowledged=self.env.context.get('acknowledged_cancellation', False)
        if  self.reason_for_cancellation and not acknowledged :
            """CCe raise, c'est pour la désynchronisation entre l'UI et la DB. Cas, qui pourrait ne pas arriver souvent, mais sait on jamais."""
            raise UserError("🚧 Le dev ne sait pas gérer ce cas précis. Rafraîchis stp, ce ticket fait l'objet d'une demande d'annulation. Et rassure-moi, t'as pas ignoré la notification hein ? 🙏🙏🙏")
        self.write({"state":"done"})
        self.env["helpdesk.notifier.manager.and.technicien"].notifier_ticket_done(self)