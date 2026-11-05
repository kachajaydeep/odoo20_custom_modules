import { Component, proxy } from "@odoo/owl";
import { useService } from "@web/core/utils/hooks";
import { Dialog } from "@web/core/dialog/dialog";
import { formatCurrency } from "@web/core/currency";
import { _t } from "@web/core/l10n/translation";
import { formatDate } from "@web/core/l10n/dates";

export class ReturnOrderDialog extends Component {
    static template = "nf_pos_barcode_return_exchange.ReturnOrderDialog";
    static components = { Dialog };
    static props = {
        title: { type: String },
        order: { type: Object },
        lines: { type: Array },
        confirm: { type: Function },
        cancel: { type: Function },
        close: { type: Function },
    };

    setup() {
        this.notification = useService("notification");
        this.onLineSelect = this.onLineSelect.bind(this);
        this.onRefundQtyChange = this.onRefundQtyChange.bind(this);
        this.onExchangeQtyChange = this.onExchangeQtyChange.bind(this);
        this.onNoteChange = this.onNoteChange.bind(this);

        this.state = proxy({
            mode: "refund",
            exchangeType: "same",

            lines: this.props.lines.map((line) => ({
                id: line.id,
                product_id: line.product_id,
                qty: line.qty,
                refunded_qty: line.refunded_qty || 0,
                price_unit: line.price_unit,
                discount: line.discount || 0,
                tax_ids: line.tax_ids,
                attribute_value_ids: line.attribute_value_ids,
                lineSelected: false,
                refund_qty: 0,
                exchange_qty: 0,
                note: "",
                _originalLine: line,
            })),
        });
    }

    onModeChange(lines, mode) {
        lines.state.mode = mode;

        for (const line of lines.state.lines) {
            line.lineSelected = false;
            line.refund_qty = 0;
            line.exchange_qty = 0;
        }
    }

    onExchangeTypeChange(line, type) {
        line.state.exchangeType = type;
    }

    onLineSelect(line, event) {
        line.lineSelected = event.target.checked;
    }

    onRefundQtyChange(line, event) {
        let value = parseFloat(event.target.value);
        const max = line.qty - line.refunded_qty;

        if (isNaN(value) || value <= 0) value = 1;
        if (value > max) {
            value = max;
            this.notification.add(
                _t(`Refund quantity cannot exceed ${max}`),
                { type: "warning" }
            );
        }

        line.refund_qty = value;
        event.target.value = value;
    }

    onExchangeQtyChange(line, event) {
        let value = parseFloat(event.target.value);
        const max = line.qty - line.refunded_qty;

        if (isNaN(value) || value <= 0) value = 1;
        if (value > max) {
            value = max;
            if (!this.props.cancel) {
                this.notification.add(
                    _t(`Exchange quantity cannot exceed ${max}`),
                    { type: "warning" }
                );
            }
            else {
                this.notification.add(
                    _t("Exchange Cancelled!!"),
                    { type: "warning" }
                );
            }
        }

        line.exchange_qty = value;
        event.target.value = value;
    }

    get currencyId() {
        const currency = this.props.order.currency_id;
        return Array.isArray(currency) ? currency[0] : currency?.id;
    }

    onNoteChange(event) {
        this.state.note = event.target.value;
    }

    formatCurrency(amount) {
        return formatCurrency(amount, this.currencyId);
    }

    formatDate(date) {
        return formatDate(date);
    }

    get totalAmount() {
        return this.state.lines
            .filter((l) => l.lineSelected)
            .reduce((sum, l) => {
                const qty = this.state.mode === "refund"
                    ? l.refund_qty
                    : l.exchange_qty;
                return sum + qty * l.price_unit * (1 - (l.discount || 0) / 100);
            }, 0);
    }

    onConfirm() {
        const refundLines = this.state.mode === "refund"
            ? this.state.lines.filter((l) => l.lineSelected && l.refund_qty > 0)
            : [];

        const exchangeLines = this.state.mode === "exchange"
            ? this.state.lines.filter((l) => l.lineSelected && l.exchange_qty > 0)
            : [];

        if (!refundLines.length && !exchangeLines.length) {
            this.notification.add(
                _t("Please select at least one product."),
                { type: "warning" }
            );
            return;
        }

        this.props.confirm({
            refundLines,
            exchangeLines,
            exchangeType: this.state.exchangeType,
            note: this.state.note,
        });
        console.log("Before Closing Popup",this);
        
        this.props.close();
    }

    onCancel() {
        this.props.cancel();
        this.props.close();
    }
}