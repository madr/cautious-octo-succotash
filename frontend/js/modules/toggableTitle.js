/*jslint browser: true */
(function (g) {
    "use strict";

    var ToggableTitle = function (elmOrSelector) {
        var i, max, elms;

        if (elmOrSelector.nodeName) {
            this.install(elmOrSelector);
            elms = [elmOrSelector];
        } else {
            elms = document.querySelectorAll(elmOrSelector);

            for (i = 0, max = elms.length; i < max; i += 1) {
                this.install(elms[i]);
            }
        }

        this.elms = elms;
    };

    ToggableTitle.prototype = {
        constructor: ToggableTitle,

        install: function (elm) {
            var that = this;

            elm.onclick = function () {
                that.toggle(elm);
            };
        },

        toggle: function (elm) {
            var o = elm.getAttribute('title');
            elm.setAttribute('title', elm.innerHTML);
            elm.innerHTML = o;
        }
    };

    // untested by design
    if (g.tajmme === undefined) {
        throw new Error("global object tajm is missing!");
    }

    g.tajmme.ToggableTitle = ToggableTitle;
}(this));