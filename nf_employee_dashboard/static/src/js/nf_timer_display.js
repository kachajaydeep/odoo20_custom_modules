/** @odoo-module **/
import { Component, proxy, onMounted, onWillUnmount, onWillUpdateProps } from "@odoo/owl";

export class NfTimerDisplay extends Component {
    static template = "nf_employee_dashboard.NfTimerDisplay";
    static props = {
        startTime: { type: Number }, // epoch ms
    };

    setup() {
        this.state = proxy({ elapsed: 0 });
        this._interval = null;

        onMounted(() => this._startInterval());

        // If parent passes a new startTime (e.g. after extend), restart interval
        onWillUpdateProps((nextProps) => {
            if (nextProps.startTime !== this.props.startTime) {
                this._stopInterval();
                this._startInterval(nextProps.startTime);
            }
        });

        onWillUnmount(() => this._stopInterval());
    }

    _startInterval(startTime = this.props.startTime) {
        if (!startTime) return;  // guard against null
        this._stopInterval();
        this._interval = setInterval(() => {
            this.state.elapsed = (Date.now() - startTime) / 1000;
        }, 1000);
    }

    _stopInterval() {
        if (this._interval) {
            clearInterval(this._interval);
            this._interval = null;
        }
    }

    get displayTime() {
        const total = Math.floor(this.state.elapsed);
        const h = Math.floor(total / 3600).toString().padStart(2, "0");
        const m = Math.floor((total % 3600) / 60).toString().padStart(2, "0");
        const s = (total % 60).toString().padStart(2, "0");
        return `${h}:${m}:${s}`;
    }
}