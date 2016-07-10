(function (g) {
    "use strict";

    var TajmMe, listeners = {};

    TajmMe = {
        listeners: function () {
            return listeners;
        },

        add: function (type, listener) {
            if (listeners[type] === undefined) {
                listeners[type] = [];
            }

            listeners[type].push(listener);
        },

        fire: function (event) {
            var todo, len, i = 0;

            if (typeof event === "string") {
                event = { type: event };
            }

            if (!event.target) {
                event.target = this;
            }

            if (listeners[event.type] instanceof Array) {
                todo = listeners[event.type];

                for (len = todo.length; i < len; i += 1) {
                    todo[i].call(this, event);
                }
            }
        },

        remove: function (type, listener) {
            var todo, len, i = 0;

            if (listeners[type] instanceof Array) {
                todo = listeners[type];

                for (len = todo.length; i < len; i += 1) {
                    if (todo[i] === listener) {
                        todo.splice(i, 1);
                        break;
                    }
                }
            }
        }
    };

    g.tajmme = TajmMe;
}(this));