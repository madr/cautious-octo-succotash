/*jslint browser: true */
(function (g) {
    "use strict";

    var DateField;

    Date.prototype.getWeek = function () {
        var week1, date = new Date(this.getTime());

        date.setHours(0, 0, 0, 0);
        date.setDate(date.getDate() + 3 - (date.getDay() + 6) % 7);

        week1 = new Date(date.getFullYear(), 0, 4);

        return 1 + Math.round(((date.getTime() - week1.getTime()) /
            86400000 - 3 + (week1.getDay() + 6) % 7) / 7);
    };

    DateField = function (currentDate, yearField, weekField, dayField) {
        var values = currentDate.split("-"),
            y = parseInt(values[0], 10),
            m = parseInt(values[1], 10) - 1,
            d = parseInt(values[2], 10);

        this.currentDate = new Date(y, m, d);

        this.fields = {
            year: yearField,
            week: weekField,
            day: dayField
        };
    };

    DateField.prototype = {
        constructor: DateField,

        increase: function (daysToAdd) {
            var addition = daysToAdd * 1000 * 60 * 60 * 24,
                newDate = new Date(this.currentDate.getTime() + addition);

            this.currentDate = newDate;
            this.setFieldValues(this.dateToValues(newDate));
        },

        button: function (id, addition) {
            var that = this,
                elm = document.querySelector(id);

            elm.onclick = function () {
                that.increase(addition);
            };
        },

        dateToValues: function (date) {
            var d = date.getDay();

            if (d === 0) { d = 7; }

            return {
                year: date.getFullYear(),
                week: date.getWeek(),
                day: d
            };
        },

        setFieldValues: function (ywd) {
            this.fields.year.value = ywd.year;
            this.fields.week.value = ywd.week;
            this.fields.day.value = ywd.day;
        }
    };

    // untested by design
    if (g.tajmme === undefined) {
        throw new Error("global object tajmme is missing!");
    }

    g.tajmme.DateField = DateField;
}(this));
