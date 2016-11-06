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
/*jslint indent: 2, browser: true */
(function (g, document) {
  "use strict";
  var Autocomplete;

  Autocomplete = function (id, values, callback) {
    var that = this;

    this.timer = "";
    this.field = document.getElementById(id);
    this.field.setAttribute("autocomplete", "off");

    this.fieldX = this.field.offsetWidth;
    this.fieldY = this.field.offsetHeight;

    this.values = values;
    this.callback = callback;

    if (window.attachEvent) {
      this.field.attachEvent("onkeydown", function (e) {
        that.keydown(e);
      });
    } else {
      this.field.addEventListener("keydown", function (e) {
        that.keydown(e);
      }, false);
    }

    this.field.onblur = function () {
      that.blur();
    };
  };

  Autocomplete.prototype.prevDef = function (event) {
    event.returnValue = false;
    if (event.preventDefault !== undefined) {
      event.preventDefault();
    }
    return true;
  };

  Autocomplete.prototype.getPosition = function (theElement) {
    var positionX = 0,
      positionY = 0;
    while (theElement !== null) {
      positionX += theElement.offsetLeft;
      positionY += theElement.offsetTop;
      theElement = theElement.offsetParent;
    }
    return [positionX, positionY];
  };

  Autocomplete.prototype.keydown = function (event) {
    if (event === undefined) {
      event = window.event;
    }

    var target = event.target || event.srcElement,
      dropdown,
      childLis,
      selected,
      i,
      max,
      inputRanges,
      that = this;

    dropdown = document.getElementById("autoCompleteDropdown");

    switch (event.keyCode) {
    case 9:     // tab
    case 16:    // shift
    case 17:    // ctrl
    case 18:    // alt
    case 20:    // caps lock
    case 27:    // esc
    case 33:    // page up
    case 34:    // page down
    case 35:    // end
    case 36:    // home
    case 37:    // left arrow
    case 39:    // right arrow
      break;
    case 13:    // enter
      if (dropdown) {
        this.blur();
        this.prevDef(event);
      }
      break;
    case 38:    // up arrow
      if (dropdown !== null) {
        childLis = dropdown.childNodes;
        selected = false;
        for (i = 0, max = childLis.length; i < max; i += 1) {
          if (childLis[i].className === "autocomplete-hover") {
            selected = true;
            if (i > 0) {
              childLis[i].className = "";
              childLis[i - 1].className = "autocomplete-hover";
              target.value = childLis[i - 1].firstChild.nodeValue;
            }
            break;
          }
        }
        if (!selected) {
          childLis[0].className = "autocomplete-hover";
          target.value = childLis[0].firstChild.nodeValue;
        }
      }
      this.prevDef(event);
      break;
    case 40:    // down arrow
      if (dropdown !== null) {
        childLis = dropdown.childNodes;
        selected = false;
        for (i = 0, max = childLis.length; i < max; i += 1) {
          if (childLis[i].className === "autocomplete-hover") {
            selected = true;
            if (i < childLis.length - 1) {
              childLis[i].className = "";
              childLis[i + 1].className = "autocomplete-hover";
              target.value = childLis[i + 1].firstChild.nodeValue;
            }
            break;
          }
        }
        if (!selected) {
          childLis[0].className = "autocomplete-hover";
          target.value = childLis[0].firstChild.nodeValue;
        }
      }
      this.prevDef(event);
      break;
    case 8:     // backspace
    case 46:    // delete
      if (this.timer !== undefined) {
        clearTimeout(this.timer);
      }
      this.timer = setTimeout(function () {
        that.generate(false);
      }, 500);
      break;
    default:
      if (this.timer !== undefined) {
        clearTimeout(this.timer);
      }
      target = event.target || event.srcElement;
      inputRanges = "false";
      if (target.createTextRange !== undefined
          || target.setSelectionRange !== undefined) {
        inputRanges = "true";
      }
      this.timer = setTimeout(function () {
        that.generate(inputRanges);
      }, 500);
    }
    return true;
  };

  Autocomplete.prototype.assign = function (e) {
    var that = this;
    e.onmouseover = function () {
      that.mouseover(this);
    };

    e.onmouseout = function () {
      that.mouseout(this);
    };

    e.onmousedown = function () {
      that.mousedown(this);
    };
  };

  Autocomplete.prototype.generate = function (doAutoComplete) {
    this.close();
    var input = this.field,
      newUl = document.createElement("ul"),
      pos = this.getPosition(input),
      newLi,
      i,
      v,
      max = this.values.length,
      htlm; // inside joke.

    newUl.setAttribute("id", "autoCompleteDropdown");

    newUl.className = "autocomplete";
    newUl.style.position = "absolute";
    newUl.style.left = pos[0] + "px";
    newUl.style.top = pos[1] + this.fieldY - 2 + "px";
    newUl.style.width = this.fieldX - 2 + "px";

    for (i = 0; i < max; i += 1) {
      v = this.values[i];

      if (v instanceof Array) { v = v[0]; }

      if (v.match(new RegExp("^" + input.value, "i"))) {
        newLi = document.createElement("li");
        newLi.className = "autocomplete-suggestion";
        htlm = v;

        newLi.innerHTML = htlm;
        newUl.appendChild(newLi);
        this.assign(newLi);
      }
    }

    if (newUl.firstChild !== null) {
      document.body.appendChild(newUl);
    }

    if (doAutoComplete !== undefined && doAutoComplete) {
      this.autoComplete();
    }
    return true;
  };

  Autocomplete.prototype.autoComplete = function () {
    var input = this.field,
      cursorMidway = false,
      range,
      originalValue,
      dropdown,
      that = this;

    if (document.selection !== undefined) {
      range = document.selection.createRange();

      if (range.move("character", 1) !== 0) {
        cursorMidway = true;
      }
    } else if (input.selectionStart !== undefined
        && input.selectionStart < input.value.length) {
      cursorMidway = true;
    }

    originalValue = input.value;
    dropdown = document.getElementById("autoCompleteDropdown");

    if (dropdown !== null && !cursorMidway) {
      dropdown.firstChild.className = "autocomplete-hover";
      input.value = dropdown.firstChild.firstChild.nodeValue;

      if (input.createTextRange !== undefined) {
        range = input.createTextRange();
        range.moveStart("character", originalValue.length);
        range.select();
      } else if (input.setSelectionRange !== undefined) {
        input.setSelectionRange(originalValue.length, input.value.length);
      }
      if (dropdown.childNodes.length === 1) {
        setTimeout(function () { that.close(); }, 10);
        this.callback(input.value);
      }
    }
    return true;
  };

  Autocomplete.prototype.mouseover = function (target) {
    var childLis, i, max;

    while (target.nodeName !== "LI") {
      target = target.parentNode;
    }

    childLis = target.parentNode.childNodes;
    max = childLis.length;
    for (i = 0; i < max; i += 1) {
      childLis[i].className = "";
    }

    target.className += " autocomplete-hover";

    return true;
  };

  Autocomplete.prototype.mouseout = function (target) {
    while (target.nodeName !== "LI") {
      target = target.parentNode;
    }

    target.className = target.className.replace(" autocomplete-hover", "");
    return true;
  };

  Autocomplete.prototype.mousedown = function (target) {
    while (target.nodeName !== "LI") {
      target = target.parentNode;
    }

    this.field.value = target.firstChild.nodeValue;

    return true;
  };

  Autocomplete.prototype.blur = function () {
    var that = this;

    if (this.timer !== undefined) {
      clearTimeout(this.timer);
    }

    this.callback(this.field.value);
    setTimeout(function () { that.close(); }, 55);
    return true;
  };

  Autocomplete.prototype.close = function () {
    var dropdown = document.getElementById("autoCompleteDropdown");

    if (dropdown !== null) {
      dropdown.parentNode.removeChild(dropdown);
    }

    return true;
  };

  // untested by design
  if (g.tajmme === undefined) {
    throw new Error("global object tajmme is missing!");
  }

  g.tajmme.Autocomplete = Autocomplete;
}(this, document));

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
        throw new Error("global object tajmme is missing!");
    }

    g.tajmme.TableFilter = TableFilter;
}(this));
/*jslint browser:true */
(function (g) {
    "use strict";

    var TableSort,
        bubbleSort;

    TableSort = function (elm) {
        var headings, i, max;

        this.tbl = elm;
        this.lastSortedTh = null;

        if (this.tbl && this.tbl.nodeName === "TABLE") {
            headings = this.tbl.tHead.rows[0].cells;
            max = headings.length;

            for (i = 0; i < max; i += 1) {
                if (headings[i].className.match(/asc|dsc/)) {
                    this.lastSortedTh = headings[i];
                }
            }
        }

        return this;
    };

    TableSort.prototype = {
        constructor: TableSort,

        makeSortable: function () {
            var headings = this.tbl.tHead.rows[0].cells,
                max = headings.length,
                i,
                b,
                c,
                that = this;

            c = function () {
                that.sortCol(this);

                return false;
            };

            for (i = 0; i < max; i += 1) {
                headings[i].cIdx = i;

                b = document.createElement("a");
                b.className = "a";
                b.href = '#';
                b.innerHTML = headings[i].innerHTML;
                b.onclick = c;

                headings[i].innerHTML = "";
                headings[i].appendChild(b);
            }
        },

        sortCol: function (el) {
            var rows = this.tbl.tBodies[0].rows,
                alpha = [],
                numeric = [],
                aIdx = 0,
                nIdx = 0,
                th = el.parentNode,
                cellIndex = th.cIdx,
                max = rows.length,
                col = [],
                i,
                cell,
                content,
                num,
                top,
                bottom,
                tBody;

            for (i = 0; i < max; i += 1) {
                cell = rows[i].cells[cellIndex];
                content = cell.textContent || cell.innerText;
                num = content.replace(/(\$|\,|\%|\s)/g, "");

                if (parseFloat(num, 10) == num) {
                    numeric[nIdx] = {
                        value: Number(num),
                        row: rows[i]
                    };

                    nIdx += 1;
                } else {
                    alpha[aIdx] = {
                        value: content,
                        row: rows[i]
                    };

                    aIdx += 1;
                }
            }

            if (th.className.match(" asc")) {
                top = bubbleSort(alpha, -1);
                bottom = bubbleSort(numeric, -1);

                th.className = th.className.replace(/ asc/, " dsc");
            } else {
                top = bubbleSort(numeric, 1);
                bottom = bubbleSort(alpha, 1);

                if (th.className.match("dsc")) {
                    th.className = th.className.replace(/ dsc/, " asc");
                } else {
                    th.className += " asc";
                }
            }

            if (this.lastSortedTh && th !== this.lastSortedTh) {
                this.lastSortedTh.className = this.lastSortedTh.className.replace(/dsc|asc/g, "");
            }

            this.lastSortedTh = th;

            col = top.concat(bottom);
            tBody = this.tbl.tBodies[0];

            for (i = 0, max = col.length; i < max; i += 1) {
                tBody.appendChild(col[i].row);
            }
        }
    };

    // untested on its own
    bubbleSort = function (arr, dir) {
        var start,
            end,
            a,
            b,
            c,
            i,
            unsorted;

        if (dir === 1) {
            start = 0;
            end = arr.length;
        } else if (dir === -1) {
            start = arr.length - 1;
            end = -1;
        }

        unsorted = true;

        while (unsorted) {
            unsorted = false;

            for (i = start; i !== end; i = i + dir) {
                if (arr[i + dir] && arr[i].value > arr[i + dir].value) {
                    a = arr[i];
                    b = arr[i + dir];
                    c = a;

                    arr[i] = b;
                    arr[i + dir] = c;

                    unsorted = true;
                }
            }
        }

        return arr;
    };

    // untested by design
    if (g.tajmme === undefined) {
        throw new Error("global object tajmme is missing!");
    }

    g.tajmme.TableSort = TableSort;
}(this));

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
        throw new Error("global object tajmme is missing!");
    }

    g.tajmme.ToggableTitle = ToggableTitle;
}(this));
/*jslint browser: true */
(function (g) {
    'use strict';

    g.tajmme.add('datefield:init', function () {
        var datefield;

        datefield = new g.tajmme.DateField(document.getElementById('id_done_at').value,
            document.getElementById('id_done_at_year'),
            document.getElementById('id_done_at_week'),
            document.getElementById('id_done_at_day'));

        datefield.button('plus-1-week', 7);
        datefield.button('plus-1-day', 1);
        datefield.button('minus-1-week', -7);
        datefield.button('minus-1-day', -1);
    });

    g.tajmme.add('limit:init', function () {
        var as = new g.tajmme.Autosubmit('id_limit', 'limit');

        as.init();
    });

    g.tajmme.add('vendor:awesomplete:init', function () {
        var ajax = new XMLHttpRequest();
        ajax.open('GET', '/reporter/projects.js', true);
        ajax.onload = function () {
            var list = JSON.parse(ajax.responseText).map(function (i) {
                return i;
            });
            new Awesomplete(document.querySelector('[data-project-autocomplete]'), {list: list});
        };
        ajax.send();
    });

    g.tajmme.add('progressform:init', function () {
        var timespent;

        timespent = new g.tajmme.TimeSpent('#id_duration');

        timespent.button('[data-plus-15-min]', 15);
        timespent.button('[data-plus-1-hour]', 60);
        timespent.button('[data-minus-15-min]', -15);
        timespent.button('[data-minus-1-hour]', -60);
    });

    g.tajmme.add('projectfilter:init', function () {
        var pf = new g.tajmme.TableFilter(
            document.getElementById('projects')
        );

        pf.filter('id_filter');
    });

    g.tajmme.add('tablesort:init', function () {

        var tables, ti, i, o;

        tables = document.getElementsByTagName('table');
        ti = tables.length;

        for (i = 0; i < ti; i += 1) {
            o = new g.tajmme.TableSort(tables[i]);
            o.makeSortable();
        }
    });

    g.tajmme.add('toggabletitles:init', function () {
        var tts = new g.tajmme.ToggableTitle('[data-tt]');
        return tts;
    });

    g.tajmme.add('userfilter:init', function () {
        var pf = new g.tajmme.TableFilter(
            document.getElementById('users')
        );

        pf.filter('id_filter');
    });

    g.tajmme.add('init', function () {
        g.tajmme.fire('tablesort:init');
    });
}(this));