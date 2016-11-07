describe("TableFilter", function () {
    function createTable () {
        var fr = document.createElement("div");
        
        fr.innerHTML = "<table id=ett2tre>\
            <tbody>\
                <tr><td>Ettan</td></tr>\
                <tr><td>Tvåan</td></tr>\
                <tr><td>Trean</td></tr>\
            </tbody>\
        </table>";

        return fr.getElementsByTagName("table")[0];
    }

    it("has all code present", function () {
        expect(tajmme).not.toBe(undefined);
        expect(tajmme.TableFilter).not.toBe(undefined);
    });

    it("initiates using a table element", function () {
        var t = createTable();
        var tf = new tajmme.TableFilter(t);

        expect(tf.tbl).not.toBe(undefined);
        expect(tf.tbl.id).toBe("ett2tre");
    });

    it("clones the tbody and leaving the original intact", function () {
        var t = createTable();
        var tf = new tajmme.TableFilter(t);

        var draft = tf.clone();
        draft.rows[1].cells[0].innerHTML = "inteTvåan";

        expect(t.tBodies[0].rows[1].cells[0].innerHTML).toBe("Tvåan");
    });

    it("replaces the original table with another tbody", function () {
        var t = createTable();

        var fr = document.createElement("div");
        
        fr.innerHTML = "<table><tbody>\
                <tr><td>Hansi</td></tr>\
                <tr><td>Andre</td></tr>\
            </tbody></table>";

        var newContent = fr.getElementsByTagName("table")[0].tBodies[0];

        var tf = new tajmme.TableFilter(t);

        tf.replace(newContent);

        expect(t.tBodies[0].rows.length).toBe(2);
        expect(t.tBodies[0].rows[0].cells[0].innerHTML).toBe("Hansi");
        expect(t.tBodies[0].rows[1].cells[0].innerHTML).toBe("Andre");
    });

    it("hide table rows not matching a string pattern", function () {
        var t = createTable();
        
        var tf = new tajmme.TableFilter(t);

        tf.update("Ett");

        expect(t.tBodies[0].rows.length).toBe(3);
        expect(t.tBodies[0].rows[1].style.display).toBe("none");
        expect(t.tBodies[0].rows[2].style.display).toBe("none");
    });

    it("restores table when string pattern is blank", function () {
        var t = createTable();
        
        var tf = new tajmme.TableFilter(t);

        tf.update("Ett");
        expect(t.tBodies[0].rows[1].style.display).toBe("none");
        expect(t.tBodies[0].rows[2].style.display).toBe("none");
        tf.update("");
        expect(t.tBodies[0].rows[1].style.display).not.toBe("none");
        expect(t.tBodies[0].rows[2].style.display).not.toBe("none");

        tf.update("Ett");
        expect(t.tBodies[0].rows[1].style.display).toBe("none");
        expect(t.tBodies[0].rows[2].style.display).toBe("none");
        tf.update(false);
        expect(t.tBodies[0].rows[1].style.display).not.toBe("none");
        expect(t.tBodies[0].rows[2].style.display).not.toBe("none");

        tf.update("Ett");
        expect(t.tBodies[0].rows[1].style.display).toBe("none");
        expect(t.tBodies[0].rows[2].style.display).toBe("none");
        tf.update("");
        expect(t.tBodies[0].rows[1].style.display).not.toBe("none");
        expect(t.tBodies[0].rows[2].style.display).not.toBe("none");

        tf.update("Ett");
        expect(t.tBodies[0].rows[1].style.display).toBe("none");
        expect(t.tBodies[0].rows[2].style.display).toBe("none");
        tf.update(undefined);
        expect(t.tBodies[0].rows[1].style.display).not.toBe("none");
        expect(t.tBodies[0].rows[2].style.display).not.toBe("none");
    });

    it("is case insensitive", function () {
        var t = createTable();
        
        var tf = new tajmme.TableFilter(t);

        tf.update("Ett");
        expect(t.tBodies[0].rows[1].style.display).toBe("none");
        expect(t.tBodies[0].rows[2].style.display).toBe("none");
        tf.update("");
        expect(t.tBodies[0].rows[1].style.display).not.toBe("none");
        expect(t.tBodies[0].rows[2].style.display).not.toBe("none");

        tf.update("eTt");
        expect(t.tBodies[0].rows[1].style.display).toBe("none");
        expect(t.tBodies[0].rows[2].style.display).toBe("none");
    });

    it("does not search until 2 chars are written", function () {
        var t = createTable();
        
        var tf = new tajmme.TableFilter(t);

        tf.update("E");
        expect(t.tBodies[0].rows[1].style.display).not.toBe("none");
        expect(t.tBodies[0].rows[2].style.display).not.toBe("none");

        tf.update("eT");
        expect(t.tBodies[0].rows[1].style.display).toBe("none");
        expect(t.tBodies[0].rows[2].style.display).toBe("none");
    });

    it("attach an input which updates table on keyup", function () {
        var t = createTable();

        var i = document.createElement("input");
        i.id = "filter-input";
        document.body.appendChild(i);
        
        var tf = new tajmme.TableFilter(t);
        tf.filter("filter-input");

        i.value = "ett";
        i.onkeyup();
        expect(t.tBodies[0].rows[1].style.display).not.toBe("none");
        expect(t.tBodies[0].rows[2].style.display).not.toBe("none");
    });

    it("immidiately filters table when input has value set", function () {
        var t = createTable();

        var i = document.createElement("input");
        i.id = "filter-input2";
        i.value = "ett";
        document.body.appendChild(i);
        
        var tf = new tajmme.TableFilter(t);
        tf.filter("filter-input2");

        expect(t.tBodies[0].rows[1].style.display).not.toBe("none");
        expect(t.tBodies[0].rows[2].style.display).not.toBe("none");
    });
});