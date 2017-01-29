/*jslint browser: true */
(function (g) {
    "use strict";

    var TableFilter;

    TableFilter = function (tableElm) {
        this.tbl = tableElm;
    };

    TableFilter.prototype = {
        constructor: TableFilter,

        clone: function () {
            return this.tbl.tBodies[0].cloneNode(true);
        },

        replace: function (newTBody) {
            return this.tbl.replaceChild(newTBody, this.tbl.tBodies[0]);
        },

        update: function (value) {
            var draft = this.clone(),
                i,
                max,
                r,
                d;

            if (value === undefined) { value = ""; }

            for (i = 0, max = draft.rows.length; i < max; i += 1) {
                r = draft.rows[i];

                if (value.length > 1 && !r.innerHTML.match(new RegExp(value, "i"))) {
                    d = "none";
                } else {
                    d = "";
                }

                r.style.display = d;
            }

            this.replace(draft);
        },

        filter: function (elementId) {
            var regulator = document.getElementById(elementId),
                that = this;

            regulator.onkeyup = function () {
                clearTimeout(that.timer);
                var elm = this;

                that.timer = setTimeout(function () {
                    that.update(elm.value, "filter");
                }, 99);
            };

            if (regulator.value.length) {
                regulator.onkeyup();
            }
        }
    };

    // untested by design
    if (g.tajmme === undefined) {
        throw new Error("global object tajm is missing!");
    }

    g.tajmme.TableFilter = TableFilter;
}(this));