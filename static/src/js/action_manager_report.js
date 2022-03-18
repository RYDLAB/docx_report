odoo.define("docx_report.ReportActionManager", function (require) {
    "use strict";

    var ActionManager = require("web.ActionManager");
    var framework = require("web.framework");
    var session = require("web.session");

    ActionManager.include({
        /**
        * Запрос на скачивание сгенерированного файла отчета
        */
        _downloadReport: function (url, action) {
            var self = this;
            var template_type = (action.report_type && action.report_type.split("-")[0]) || "qweb";
            framework.blockUI();
            return new Promise(function (resolve, reject) {
                var type = template_type + "-" + url.split("/")[2];
                var blocked = !session.get_file({
                    url: "/report/download",
                    data: {
                        data: JSON.stringify([url, type]),
                        context: JSON.stringify(Object.assign({}, action.context, session.user_context)),
                    },
                    success: resolve,
                    error: (error) => {
                        self.call("crash_manager", "rpc_error", error);
                        reject();
                    },
                    complete: framework.unblockUI,
                });
                if (blocked) {
                    // AAB: this check should be done in get_file service directly,
                    // should not be the concern of the caller (and that way, get_file
                    // could return a promise)
                    var message = _t("A popup window with your report was blocked. You " +
                                     "may need to change your browser settings to allow " +
                                     "popup windows for this page.");
                    self.do_warn(_t("Warning"), message, true);
                }
            });
        },

        /**
        * Этот метод вызывается при нажатии на пункт меню для печати отчета.
        *
        * Вызывает _triggerDownload с различными аргументами.
        * Расширяется новыми вариантами.
        * В оригинальном методе есть и другой функционал.
        */
        _executeReportAction: function (action, options) {
            if (action.report_type === "docx-docx") {
                return this._triggerDownload(action, options, "docx");
            } else if (action.report_type === "docx-pdf") {
                return this._triggerDownload(action, options, "pdf");
            } else {
                return this._super.apply(this, arguments);
            }
        },

        /**
        * Запускает скачивание файла отчета
        */
        _triggerDownload: function (action, options, type){
            var self = this;
            var reportUrls = this._makeReportUrls(action);
            return this._downloadReport(reportUrls[type], action).then(function () {
                if (action.close_on_report_download) {
                    var closeAction = { type: "ir.actions.act_window_close" };
                    return self.doAction(closeAction, _.pick(options, "on_close"));
                } else {
                    return options.on_close();
                }
            });
        },

        /**
        * Генерирует URL для запроса отчета
        */
        _makeReportUrls: function (action) {
            var reportUrls = this._super.apply(this, arguments);
            reportUrls.docx = "/report/docx/" + action.report_name;
            if (_.isUndefined(action.data) || _.isNull(action.data) ||
                (_.isObject(action.data) && _.isEmpty(action.data))) {
                if (action.context.active_ids) {
                    var activeIDsPath = "/" + action.context.active_ids.join(",");
                    reportUrls.docx += activeIDsPath
                }
            } else {
                var serializedOptionsPath = "?options=" + encodeURIComponent(JSON.stringify(action.data));
                serializedOptionsPath += "&context=" + encodeURIComponent(JSON.stringify(action.context));
                reportUrls.docx += serializedOptionsPath
            }
            return reportUrls;
        },
    });
});
