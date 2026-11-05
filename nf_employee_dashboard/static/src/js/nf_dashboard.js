/** @odoo-module **/

import { registry } from "@web/core/registry";
import { useService } from "@web/core/utils/hooks";
import { Component, proxy, onWillStart, onMounted } from "@odoo/owl";

class NfEmployeeDashboard extends Component {
    static template = "nf_employee_dashboard.Dashboard";

    setup() {

        this.orm = useService("orm");
        this.action = useService("action");

        this.state = proxy({
            employee: {},
            leave: 0,
            attendance: 0,
            expense: 0,
            leave_list: [],
            attendance_list: [],
            expense_list: [],
            birthdays: [],
            announcements: [],
            anniversary: [],
            today_date: new Date().toLocaleDateString('en-US', { weekday: 'long', year: 'numeric', month: 'long', day: 'numeric'}),
        });

        onWillStart(async () => {

            const result = await this.orm.call(
                "nf.employee.dashboard",
                "get_dashboard_data",
                []
            );

            if (result) {

                this.state.employee = result.employee || {};
                this.state.leave = result.leave || 0;
                this.state.attendance = result.attendance || 0;
                this.state.expense = result.expense || 0;

                this.state.birthdays = result.birthdays || [];
                this.state.announcements = result.announcements || [];
                this.state.anniversary = result.anniversary || [];

                this.state.leave_list = result.leave_list || [];
                this.state.attendance_list = result.attendance_list || [];
                this.state.expense_list = result.expense_list || [];

            }

        });

    }

    async openAction(action_xmlid) {

        this.action.doAction(action_xmlid);

    }

}

registry
    .category("actions")
    .add("employee_dashboard", NfEmployeeDashboard);

export { NfEmployeeDashboard };
