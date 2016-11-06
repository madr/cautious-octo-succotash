describe("ToggableTitle", function () {
    beforeEach(function () {
        var existing = document.getElementById("a");

        if (existing) {
            existing.parentNode.removeChild(existing);
        }

        document.body.innerHTML += "<div id='a'>\
            <div title='titel' id='abc123'>321cba</div>\
            <div title='1' data-toggable-title>one</div>\
            <div title='2' data-toggable-title>two</div>\
            <div title='fu' data-toggable-title>fuckyou</div>\
            </div>";
    });

    it("has all code present", function () {
        expect(tajmme).not.toBe(undefined);
        expect(tajmme.ToggableTitle).not.toBe(undefined);
    });

    it("can install by an element reference", function () {
        var tt = new tajmme.ToggableTitle(document.getElementById('abc123'));
        expect(tt.elms.length).toBe(1);
    });

    it("can install by an css selector string", function () {
        var tt = new tajmme.ToggableTitle('[data-toggable-title]');
        expect(tt.elms.length).toBe(3);
    });

    it("attach onclick event upon install", function () {
        var elm = document.querySelector('[data-toggable-title]');

        expect(elm.onclick).toBe(null);

        var tt = new tajmme.ToggableTitle('[data-toggable-title]');

        expect(elm.onclick).not.toBe(null);
        expect(typeof elm.onclick).toBe('function');
    });

    it("toggles title attribute and inner html when clicked", function () {
        var elms = document.querySelectorAll('[data-toggable-title]');

        var tt = new tajmme.ToggableTitle('[data-toggable-title]');

        elms[0].onclick();
        expect(elms[0].getAttribute('title')).toBe('one');
        expect(elms[0].innerHTML).toBe('1');
        elms[0].onclick();
        expect(elms[0].getAttribute('title')).toBe('1');
        expect(elms[0].innerHTML).toBe('one');

        elms[1].onclick();
        expect(elms[1].getAttribute('title')).toBe('two');
        expect(elms[1].innerHTML).toBe('2');
        elms[1].onclick();
        expect(elms[1].getAttribute('title')).toBe('2');
        expect(elms[1].innerHTML).toBe('two');

        elms[2].onclick();
        expect(elms[2].getAttribute('title')).toBe('fuckyou');
        expect(elms[2].innerHTML).toBe('fu');
        elms[2].onclick();
        expect(elms[2].getAttribute('title')).toBe('fu');
        expect(elms[2].innerHTML).toBe('fuckyou');
    });
});