/** @odoo-module **/

import {Component, proxy, onWillStart, useRef, markup} from "@odoo/owl";
import {_t} from "@web/core/l10n/translation";
import {registry} from "@web/core/registry";
import {useService, useAutofocus} from "@web/core/utils/hooks";
import {rpc} from "@web/core/network/rpc";
import {user} from "@web/core/user";
import {isIosApp} from "@web/core/browser/feature_detection";
import {deserializeDateTime} from "@web/core/l10n/dates";
const {DateTime} = luxon;

export class EmployeeManagement extends Component {
    static template = "nf_employee_dashboard.EmployeeManagement";

    setup() {
        this.orm = useService("orm");
        this.notification = useService("notification");

        this.date_formatter = registry.category("formatters").get("float_time");
        this.searchReadEmployee();
        this.resonInputRef = useRef("input_reson");

        this.state = proxy({
            username: user.name,
            use_img: `/web/image?model=res.users&field=avatar_1920&id=${user.userId}`,
            running: false,
            break: false,
            checkedIn: false,
            startTime: null,
            interval: null,
            attendance_state: "",
            elapsed: 0,
            bye: false,
            timers: {
                timeleft: 0,
                formatted: "00:00:00",
            },
            late_check_in: false,
            late_check_in_readon: "",
            attendance_state:"",
        });

        onWillStart(async () => {
            const result = await rpc(
                "/nf_employee_management/nf_get_employee_data",
            );

            this.state.break = result.nf_break;
            if (result.nf_break === true) {
                const now = new Date();
                this.state.startTime = new Date(result.break_start + "Z");
                const diff = (now - this.state.startTime) / 1000;
                this.startTimer();
            }
        });
    }

    async startTimer() {
        if (this.state.interval) clearInterval(this.state.interval);
        if (this.state.startTime === null) {
            this.state.startTime = new Date();
        }
        this.state.interval = setInterval(() => {
            const now = new Date();
            const diff = (now - this.state.startTime) / 1000;
            this.state.elapsed = diff;
            this.render();
        }, 1000);
    }

    formateTime(timeleft) {
        const hrs = Math.floor(timeleft / 3600);
        const mins = Math.floor((timeleft % 3600) / 60);
        const secs = Math.floor(timeleft % 60);
        return `${hrs.toString().padStart(2, "0")}:${mins.toString().padStart(2, "0")}:${secs.toString().padStart(2, "0")}`;
    }

    async searchReadEmployee() {
        const result = await rpc("/hr_attendance/attendance_user_data");
        this.state.attendance_state = result.attendance_state;

        this.employee = result;

        if (this.employee.id) {
            this.state.attendance_state = this.employee.attendance_state;
            this.hoursToday = this.date_formatter(this.employee.hours_today);
            this.hoursPreviouslyToday = this.date_formatter(
                this.employee.hours_previously_today,
            );
            this.lastAttendanceWorkedHours = this.date_formatter(
                this.employee.last_attendance_worked_hours,
            );
            this.lastCheckIn = deserializeDateTime(
                this.employee.last_check_in,
            ).toLocaleString(DateTime.TIME_SIMPLE);
            this.state.checkedIn =
                this.employee.attendance_state === "checked_in";
            this.isFirstAttendance = this.employee.hours_previously_today === 0;
            this.state.isDisplayed = this.employee.display_systray;
            this.state.break = this.employee.break;
        } else {
            this.state.isDisplayed = false;
        }
    }

    async timerStart(ev) {
        if (this.state.break) {
            const hasRunOneHour = this.state.elapsed >= 3600;
            if (hasRunOneHour && this.state.late_check_in_readon == "") {
                this.state.late_check_in = true;
                this.notification.add(
                    markup(
                        _t(
                            "Please specify the reason for coming in late from break.",
                        ),
                    ),
                    {
                        title: _t("Late Break-End Reason"),
                        type: "danger",
                    },
                );
                return false;
            } else {
                this.state.late_check_in = false;
            }
        }
        const employee_id = await this.orm.call(
            "hr.employee",
            "nf_break_start",
            [[this.employee.id]],
        );
        const isOn = ev.target.checked;
        if (
            this.state.attendance_state === "checked_in" &&
            this.state.break == false
        ) {
            if (!isIosApp()) {
                // iOS app lacks permissions to call `getCurrentPosition`

                navigator.geolocation.getCurrentPosition(
                    async ({coords: {latitude, longitude}}) => {
                        await rpc("/hr_attendance/systray_check_in_out", {
                            latitude,
                            longitude,
                        });
                        await this.searchReadEmployee();
                    },
                    async (err) => {
                        await rpc("/hr_attendance/systray_check_in_out");
                        await this.searchReadEmployee();
                    },
                    {
                        enableHighAccuracy: true,
                    },
                );
            } else {
                await rpc("/hr_attendance/systray_check_in_out");
                await this.searchReadEmployee();
            }

            if (isOn === true) {
                this.state.break = true;
                this.state.running = true;
                this.startTimer();
                // this.render();
            }
        } else {
            if (!isIosApp()) {
                // iOS app lacks permissions to call `getCurrentPosition`

                navigator.geolocation.getCurrentPosition(
                    async ({coords: {latitude, longitude}}) => {
                        await rpc("/hr_attendance/systray_check_in_out", {
                            latitude,
                            longitude,
                        });
                        await this.searchReadEmployee();
                    },
                    async (err) => {
                        await rpc("/hr_attendance/systray_check_in_out");
                        await this.searchReadEmployee();
                    },
                    {
                        enableHighAccuracy: true,
                    },
                );
            } else {
                await rpc("/hr_attendance/systray_check_in_out");
                await this.searchReadEmployee();
            }
            clearInterval(this.state.interval);
            this.state.running = false;
        }

    }
    bye(ev) {
        const isOn = ev.target.checked;
        if (isOn === true) {
            this.state.bye = true;
        } else {
            this.state.bye = false;
        }
    }
    async breakActionEnd() {
        const employee_id = await this.orm.call(
            "hr.employee",
            "nf_emp_checkOut",
            [[this.employee.id]],
        );
        clearInterval(this.state.interval);
        this.state.running = false;
    }

    get display_BreakTime() {
        return this.formateTime(this.state.elapsed);
    }

    async checkInOut() {
        const now = new Date();
        if (
            this.lastCheckIn == "Invalid DateTime" &&
            this.state.late_check_in_readon == ""
        ) {
            const isAfter940 = now.getHours() > 9 || (now.getHours() === 9 && now.getMinutes() > 34);
            if (isAfter940 && !this.state.late_check_in) {
                this.state.late_check_in = true;

                this.notification.add(
                    markup(_t("Please specify the reason for coming in late.")),
                    {
                        title: _t("Late Arrival Reason"),
                        type: "danger",
                    },
                );
                return;
            } else {
            }
        } else {
            this.state.late_check_in = false;
        }
        // create today's 5:20 PM
        const targetTime = new Date();
        targetTime.setHours(17, 30, 0, 0); // 17 = 5 PM, 20 minutes

        if (!isIosApp()) {
            navigator.geolocation.getCurrentPosition(
                async ({coords: {latitude, longitude}}) => {
                    await rpc("/hr_attendance/systray_check_in_out", {
                        latitude,
                        longitude,
                    });
                    await this.searchReadEmployee();
                },
                async (err) => {
                    await rpc("/hr_attendance/systray_check_in_out");
                    await this.searchReadEmployee();
                },
                {
                    enableHighAccuracy: true,
                },
            );
        } else {
            await rpc("/hr_attendance/systray_check_in_out");
            await this.searchReadEmployee();
        }
        if (
            this.state.bye === true &&
            this.state.attendance_state === "checked_in"
        ) {
            const employee_id = await this.orm.call(
                "hr.employee",
                "nf_emp_checkOut",
                [[this.employee.id]],
            );
        }
    }
}

registry
    .category("actions")
    .add("nf_employee_attendance_template", EmployeeManagement, {force: true});
