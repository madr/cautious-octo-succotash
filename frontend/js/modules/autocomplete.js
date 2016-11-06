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
