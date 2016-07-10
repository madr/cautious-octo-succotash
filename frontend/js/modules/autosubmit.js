/*jslint browser: true */
(function (g) {
    "use strict";

    var Autosubmit,
        field,
        form;

    Autosubmit = function (fieldId, formId) {
        form = formId;
        field = fieldId;
    };

    Autosubmit.prototype = {
        constructor: Autosubmit,

        init: function () {
            document.getElementById(field).onchange = this.createSubmit(form);
        },

        createSubmit: function (formId) {
            return function () {
                document.getElementById(formId).submit();
            };
        }
    };

    // untested by design
    if (g.tajmme === undefined) {
        throw new Error("global object tajmme is missing!");
    }

    g.tajmme.Autosubmit = Autosubmit;
}(this));