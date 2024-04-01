odoo.define("custom_report_field.ReportActionManager", function (require) {
    "use strict";

    var ActionManager = require("web.ActionManager");

    ActionManager.include({
        _handleAction: function (action, options) {
            var self = this;
            if (action.type === "ir.actions.report"
                && action.validate_custom_report_field
                && !action.context.report_values_validated) {
                return new Promise(function (resolve, reject) {
                    self.do_action({
                        type: "ir.actions.act_window",
                        view_mode: "form",
                        views: [[false, "form"]],
                        res_model: "custom.report.field.values.wizard",
                        target: "new",
                        context: Object.assign(
                            { "default_ir_actions_report_id": action.id }, 
                            action.context
                        ),
                    }).then(function() {
                        resolve();
                    }).catch(function() {
                        reject();
                    });
                });
            }
            else if (action.type === "ir.actions.report"
                    && action.validate_custom_report_field
                    && action.context.report_values_validated) {
                this.do_action({"type": "ir.actions.act_window_close"});
            }
            return this._super.apply(this, arguments);
        },
    });
});
