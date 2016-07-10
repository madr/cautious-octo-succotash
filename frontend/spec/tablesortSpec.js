describe("tablesort", function () {
    function createTable () {
        var existing = document.getElementById("members");
        if (existing) {
            existing.parentNode.removeChild(existing);
        }
        document.body.innerHTML += "<table id='members'>\
                                        <thead><tr><th>Dude</th><th>Instrument</th></tr></thead>\
                                        <tbody>\
                                            <tr><td>Hansi</td><td>Sång</td></tr>\
                                            <tr><td>Andre</td><td>Lead</td></tr>\
                                            <tr><td>Marcus</td><td>Rhythm</td></tr>\
                                            <tr><td>Thomen</td><td>Trummor</td></tr>\
                                        </tbody>\
                                    </table>";
    }

    it("has all code present", function () {
        expect(tajmme).not.toBe(undefined);
        expect(tajmme.TableSort).not.toBe(undefined);
    });

    it("makes table headings clickable", function () {
        createTable();
        var e = document.getElementById("members"),
            ts = new tajmme.TableSort(e);
        
        expect(e.querySelectorAll("thead button").length).toBe(0);
        ts.makeSortable();

        expect(e.querySelectorAll("thead button").length).toBe(2);
        expect(e.querySelectorAll("thead button")[0].onclick).not.toBe(undefined);
        expect(e.querySelectorAll("thead button")[1].onclick).not.toBe(undefined);
    });
    
    it("resort cols", function () {
        createTable();
        var buttons,
            e = document.getElementById("members"),
            ts = new tajmme.TableSort(e);
        
        ts.makeSortable();

        buttons = e.getElementsByTagName("button");
        ts.sortCol(buttons[0]);

        expect(e.tBodies[0].rows[0].cells[0].textContent).toBe("Andre");
        expect(e.tBodies[0].rows[1].cells[0].textContent).toBe("Hansi");
        expect(e.tBodies[0].rows[2].cells[0].textContent).toBe("Marcus");
        expect(e.tBodies[0].rows[3].cells[0].textContent).toBe("Thomen");

        ts.sortCol(buttons[1]);

        expect(e.tBodies[0].rows[0].cells[1].textContent).toBe("Lead");
        expect(e.tBodies[0].rows[1].cells[1].textContent).toBe("Rhythm");
        expect(e.tBodies[0].rows[2].cells[1].textContent).toBe("Sång");
        expect(e.tBodies[0].rows[3].cells[1].textContent).toBe("Trummor");
    });

    it("only has asc/dsc classes on current col", function () {
        createTable();
        var buttons,
            e = document.getElementById("members"),
            ts = new tajmme.TableSort(e);
        
        ts.makeSortable();

        buttons = e.getElementsByTagName("button");
        ts.sortCol(buttons[0]);

        expect(buttons[0].parentNode.className.match(/asc|dsc/) instanceof Array).toBe(true);
        expect(buttons[1].parentNode.className.match(/asc|dsc/) instanceof Array).toBe(false);
        
        ts.sortCol(buttons[1]);

        expect(buttons[0].parentNode.className.match(/asc|dsc/) instanceof Array).toBe(false);
        expect(buttons[1].parentNode.className.match(/asc|dsc/) instanceof Array).toBe(true);
    });

    it("switch between ascending and descending order", function () {
        createTable();
        var buttons,
            e = document.getElementById("members"),
            ts = new tajmme.TableSort(e);
        
        ts.makeSortable();

        buttons = e.getElementsByTagName("button");
        ts.sortCol(buttons[0]);

        expect(buttons[0].parentNode.className.match(/asc/) instanceof Array).toBe(true);
        expect(e.tBodies[0].rows[0].cells[0].textContent).toBe("Andre");
        expect(e.tBodies[0].rows[1].cells[0].textContent).toBe("Hansi");
        expect(e.tBodies[0].rows[2].cells[0].textContent).toBe("Marcus");
        expect(e.tBodies[0].rows[3].cells[0].textContent).toBe("Thomen");

        ts.sortCol(buttons[0]);

        expect(buttons[0].parentNode.className.match(/dsc/) instanceof Array).toBe(true);
        expect(e.tBodies[0].rows[0].cells[0].textContent).toBe("Thomen");
        expect(e.tBodies[0].rows[1].cells[0].textContent).toBe("Marcus");
        expect(e.tBodies[0].rows[2].cells[0].textContent).toBe("Hansi");
        expect(e.tBodies[0].rows[3].cells[0].textContent).toBe("Andre");

        ts.sortCol(buttons[0]);

        expect(buttons[0].parentNode.className.match(/asc/) instanceof Array).toBe(true);
        expect(e.tBodies[0].rows[0].cells[0].textContent).toBe("Andre");
        expect(e.tBodies[0].rows[1].cells[0].textContent).toBe("Hansi");
        expect(e.tBodies[0].rows[2].cells[0].textContent).toBe("Marcus");
        expect(e.tBodies[0].rows[3].cells[0].textContent).toBe("Thomen");
    });
});