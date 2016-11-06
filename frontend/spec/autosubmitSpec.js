describe("Autosubmit", function () {
    it("has all code present", function () {
        expect(tajmme).not.toBe(undefined);
        expect(tajmme.Autosubmit).not.toBe(undefined);
    });

    it("can initiate itself", function () {
        document.body.innerHTML += "\
        <form id='limit'>\
        <input id='id_limit'>\
        </form>";

        var as = new tajmme.Autosubmit(
            "id_limit",
            "limit"
        );

        as.init();

        expect(document.getElementById("id_limit").onchange).not.toBe(undefined);
    });

    it("submit parent form on change", function () {
        var existing = document.getElementById("limit");
        if (existing) { existing.parentNode.removeChild(existing); }

        document.body.innerHTML += "\
        <form id='limit'>\
        <input id='id_limit'>\
        </form>";

        var as = new tajmme.Autosubmit(
            "id_limit",
            "limit"
        );

        as.init();
        
        window.QWEASD = false;

        document.getElementById("limit").submit = function () {
            window.QWEASD = true;
        };

        document.getElementById("id_limit").onchange(); 

        expect(window.QWEASD).toBe(true);
    });
});