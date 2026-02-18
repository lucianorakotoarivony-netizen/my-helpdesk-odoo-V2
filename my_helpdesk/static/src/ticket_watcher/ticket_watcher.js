/** @odoo-module **/
import { Component, onWillStart, onWillUnmount, useState } from "@odoo/owl";
import { useService } from "@web/core/utils/hooks";
import { registry } from "@web/core/registry";
console.log("🦉 OWL loaded from my_helpdesk");
export class TicketWatcher extends Component {
    static template = "my_helpdesk.TicketWatcherTemplate";

    setup() {
        this.busService = useService("bus_service");
        this.state = useState({
            reason: this.props.record.data.reason_for_cancellation || ""
        });

        onWillStart(() => {
            const channel = `helpdesk.ticket/${this.props.record.resId}`;
            this.busService.addChannel(channel);
            this.busService.addEventListener("notification", this.onNotification.bind(this));
        });

        onWillUnmount(() => {
            this.busService.removeEventListener("notification", this.onNotification);
        });
    }

    onNotification(notification) {
        if (notification.type === "cancellation_request") {
            this.props.record.update({
                'reason_for_cancellation': notification.payload.reason
            });
            this.state.reason = notification.payload.reason;
        }
    }
}
registry.category("fields").add("ticket_watcher", {
    component: TicketWatcher,
});

