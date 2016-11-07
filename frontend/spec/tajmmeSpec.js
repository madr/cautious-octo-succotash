describe("tajmme", function () {
    function ex1 (evt) {
        document.body.innerHTML += "bajs";
    }

    function ex2 (evt) {
        document.body.innerHTML += evt.word;
    }

    function ex3 (evt) {
        document.body.innerHTML += (evt.word + "boogie");
    }

    it("has all code present", function () {
        expect(tajmme).not.toBe(undefined);
        expect(tajmme.TimeSpent).not.toBe(undefined);
    });

    it("can add events", function () {
        tajmme.add("bajs", ex1);
        tajmme.add("bajs", ex2);

        expect(tajmme.listeners()["bajs"] instanceof Array).toBe(true);
        expect(tajmme.listeners()["bajs"].length).toBe(2);
    });

    it("can remove events", function () {
        tajmme.remove("bajs", ex1);
        tajmme.remove("bajs", ex2);

        expect(tajmme.listeners()["bajs"] instanceof Array).toBe(true);
        expect(tajmme.listeners()["bajs"].length).toBe(0); 
    });

    it("can add events of different types", function () {
        tajmme.add("bajs", ex1);
        tajmme.add("bajs2", ex2);

        expect(tajmme.listeners()["bajs"] instanceof Array).toBe(true);
        expect(tajmme.listeners()["bajs"].length).toBe(1);
        expect(tajmme.listeners()["bajs2"] instanceof Array).toBe(true);
        expect(tajmme.listeners()["bajs2"].length).toBe(1);

        tajmme.remove("bajs", ex1);
        tajmme.remove("bajs2", ex2);
    });

    it("can fire events using event name", function () {
        tajmme.add("bajs", ex1);
        tajmme.fire("bajs");

        expect(document.body.innerHTML.match("bajs")).not.toBe(null);

        tajmme.remove("bajs", ex1);
    });

    it("can fire events using an event object with custom properties", function () {
        tajmme.add("bajs", ex2);
        tajmme.fire( {type: "bajs", word: "skinka"});

        expect(document.body.innerHTML.match("skinka")).not.toBe(null);

        tajmme.remove("bajs", ex2);
    });

    it("preserves order of events", function () {
        tajmme.add("bajs", ex2);
        tajmme.add("bajs", ex3);
        tajmme.fire( {type: "bajs", word: "korv"});

        expect(document.body.innerHTML.match("korvkorvboogie")).not.toBe(null);

        tajmme.remove("bajs", ex2);
        tajmme.remove("bajs", ex3);
    });
});