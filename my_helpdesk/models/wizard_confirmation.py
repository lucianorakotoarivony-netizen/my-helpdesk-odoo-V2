from odoo import models, api, fields

class HelpdeskConfirmWizard(models.TransientModel): 
    _name="helpdesk.confirm.wizard"
    _description="Pop up de confirmation"
    tickets_id=fields.Many2one("helpdesk.ticket", string="Ticket concerné") 
    message=fields.Text(compute="_compute_message") 

    @api.depends("tickets_id") 
    def _compute_message(self):
        """Pourquoi 3 messages? Juste parce que ça m'amuse de faire 3 pop up d'affilé"""
        messages: dict[int, str]={1:"T'es sûr, il y a plus urgent à faire.",
                                     2:"Why? Je t'avais dit qu'il y avait plus urgent.",
                                     3:"Sûr de chez sûr? Au fond, je m'en fiche, tu fais ce que tu veux."} 
        step=self.env.context.get("step",1) 
        for record in self:
            record.message=messages.get(step,"Confirmation")
            
    def action_next_step(self):
        """Ici on va donc faire en sorte que le pop up apparaisse 3 fois.""" 
        current_step=self.env.context.get("step",1)
        if current_step<3: 
            return{ "name":"Je répète, il y a plus urgent",
                    "res_model":"helpdesk.confirm.wizard",
                    "view_mode":"form",
                    "target":"new",
                    "type":"ir.actions.act_window", 
                    "context":{"default_tickets_id":self.tickets_id.id, "step":current_step+1 } } 
        else: 
            return self.tickets_id.action_in_progress()