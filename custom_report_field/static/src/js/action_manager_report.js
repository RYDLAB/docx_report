/** @odoo-module **/

import { registry } from "@web/core/registry";


/**
 * Adds new handler for showing wizard with custom fields values for report.
 *
 * @returns {Promise<*>}
 */
async function customReportFieldWizardHandler(action, options, env) {
    if (action.type === "ir.actions.report"
        && action.validate_custom_report_field
        && !action.context.report_values_validated) {
        await env.services.action.doAction({
            type: "ir.actions.act_window",
            view_mode: "form",
            views: [[false, "form"]],
            res_model: "custom.report.field.values.wizard",
            target: "new",
            context: Object.assign(
                { "default_ir_actions_report_id": action.id },
                action.context
            ),
        });
        return Promise.resolve(true);
    }
    else if (action.type === "ir.actions.report"
            && action.validate_custom_report_field
            && action.context.report_values_validated) {
        return env.services.action.doAction({"type": "ir.actions.act_window_close"});
    }
    return Promise.resolve(false);
}

registry.category("ir.actions.report handlers").add(
    "custom_report_field_wizard_handler",
    customReportFieldWizardHandler,
    {sequence: 10},
);
