/** @odoo-module **/

import { registry } from "@web/core/registry";
import { download } from "@web/core/network/download";

async function docxHandler(action, options, env) {
    let reportType = null;
    if (action.report_type === "docx-docx") {
        reportType = "docx";
    } else if (action.report_type === "docx-pdf") {
        reportType = "pdf";
    }
    if (reportType) {
        // Make URL
        let url = `/report/${reportType}/${action.report_name}`;
        const actionContext = action.context || {};
        if (action.data && JSON.stringify(action.data) !== "{}") {
            // build a query string with `action.data` (it's the place where reports
            // using a wizard to customize the output traditionally put their options)
            const options = encodeURIComponent(JSON.stringify(action.data));
            const context = encodeURIComponent(JSON.stringify(actionContext));
            url += `?options=${options}&context=${context}`;
        } else {
            if (actionContext.active_ids) {
                url += `/${actionContext.active_ids.join(",")}`;
            }
        }
        // Download report
        env.services.ui.block();
        try {
            const template_type = (action.report_type && action.report_type.split("-")[0]) || "docx";
            const type = template_type + "-" + url.split("/")[2];
            await download({
                url: "/report/download",
                data: {
                    data: JSON.stringify([url, type]),
                    context: JSON.stringify(Object.assign({}, action.context, env.services.user.context)),
                },
            });
        } finally {
            env.services.ui.unblock();
        }
        const onClose = options.onClose;
        if (action.close_on_report_download) {
            return env.services.action.doAction({type: "ir.actions.act_window_close"}, {onClose});
        } else if (onClose) {
            onClose();
        }
        return Promise.resolve(true);
    }
    return Promise.resolve(false);
}

registry.category("ir.actions.report handlers").add("docx_handler", docxHandler);
