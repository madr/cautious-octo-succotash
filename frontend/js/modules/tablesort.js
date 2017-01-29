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
        throw new Error("global object tajm is missing!");
    }

    g.tajmme.TableSort = TableSort;
}(this));
