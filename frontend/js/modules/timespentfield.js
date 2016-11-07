/*jslint browser: true */
(function (g) {
    "use strict";

    var TimeSpent,
        reReadable = /(\d+)\s?[h|m]/gi,
        reHhMm = /^(\d+):(\d+)$/i;

    TimeSpent = function (f) {
        var that = this;

        if (typeof f === "string") {
            this.field = document.querySelector(f);
        } else {
            this.field = f;
        }

        this.field.onblur = function () {
            if (that.field.value !== "") {
                var m = that.toMinutes(that.field.value);
                that.field.value = that.correct(m);
            }
        };
    };

    TimeSpent.prototype = {
        constructor: TimeSpent,

        toMinutes: function (any) {
            var sum = 0,
                values,
                i,
                vX;

            values = any.match(reHhMm);

            if (values) {
                if (parseInt(values[1], 10) !== 0) {
                    sum += parseInt(values[1], 10) * 60;
                }

                if (parseInt(values[2], 10) !== 0) {
                    sum += parseInt(values[2], 10);
                }

                return parseInt(sum, 10);
            }

            // in the most cases we should not need to go this far,
            // but IF we do, try to find "1h", "1 hours" et cetera 
            // instead.

            values = any.match(reReadable);

            if (values) {
                i = values.length;

                while (i) {
                    i = i - 1;
                    vX = values[i];

                    if (vX.match(/h/)) {
                        sum += parseInt(vX, 10) * 60;
                    } else {
                        sum += parseInt(vX, 10);
                    }
                }

                return parseInt(sum, 10);
            }

            sum = parseInt(vX, 10);

            if (sum < 9) {
                sum = sum * 60;
            }

            return sum;
        },

        increase: function (addition) {
            var current, added;

            current = this.toMinutes(this.field.value);

            if (current) {
                added = current + addition;
            } else {
                added = addition;
            }

            this.field.value = this.correct(added);
        },

        correct: function (minutes) {
            var hh, mm;

            if (minutes === true || minutes === false
                    || isNaN(minutes)) {
                minutes = 15;
            }

            if (minutes < 0 || minutes === 0) {
                return "00:00";
            }

            minutes = parseInt(minutes, 10);

            if (minutes % 15) {
                minutes += 15 - minutes % 15;
            }

            hh = (minutes - (minutes % 60)) / 60;
            mm = minutes - hh * 60;

            if (hh < 10) { hh = "0" + hh; }
            if (mm < 10) { mm = "0" + mm; }

            return hh + ":" + mm;
        },

        button: function (id, addition) {
            var that = this,
                elm = document.querySelector(id);

            elm.onclick = function () {
                that.increase(addition);
            };
        }
    };

    // untested by design
    if (g.tajmme === undefined) {
        throw new Error("global object tajmme is missing!");
    }

    g.tajmme.TimeSpent = TimeSpent;
}(this));
