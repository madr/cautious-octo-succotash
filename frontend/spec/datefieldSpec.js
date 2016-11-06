describe("DateField", function () {
    var fixtures = {
        date: "2014-02-12",
        y: 2014,
        w: 7,
        d: 3
    }

    function id (id) {
        return document.getElementById(id);
    }

    beforeEach(function () {
        var existing = document.getElementById("a");

        if (existing) {
            existing.parentNode.removeChild(existing);
        }

        document.body.innerHTML += "<div id=df>\
            <input id=d>\
            <input id=w>\
            <input id=y>\
            <button id=minus>+</button>\
            <button id=plus>+</button>\
            </div>";
    });

    it("has all code present", function () {
        expect(tajmme).not.toBe(undefined);
        expect(tajmme.DateField).not.toBe(undefined);
    });

    it("adds getWeek() to Date.prototype", function () {
        expect(typeof Date.prototype.getWeek).not.toBe(undefined);
    });

    it("initates using a date and 3 fields", function () {
        var df = new tajmme.DateField(fixtures.date, 
            id("y"),
            id("w"),
            id("d")
        );

        expect(df.currentDate).not.toBe(undefined);
        expect(df.currentDate.getDate()).toBe(12);
        expect(df.currentDate.getMonth()).toBe(1);
        expect(df.currentDate.getFullYear()).toBe(2014);

        expect(df.fields).not.toBe(undefined)
        
        expect(df.fields.year.nodeName).toBe("INPUT")
        expect(df.fields.week.nodeName).toBe("INPUT")
        expect(df.fields.day.nodeName).toBe("INPUT")
        
        expect(df.fields.year.id).toBe("y")
        expect(df.fields.week.id).toBe("w")
        expect(df.fields.day.id).toBe("d")
    });
    
    it("can transform a date to Year, Week and Weekday", function () {
        var df = new tajmme.DateField(fixtures.date, 
            id("y"),
            id("w"),
            id("d")
        );

        var values = df.dateToValues(df.currentDate);

        expect(values.year).toBe(fixtures.y)
        expect(values.week).toBe(fixtures.w)
        expect(values.day).toBe(fixtures.d)
    });

    it("transformation make Sundays to 7, not 0", function () {
        var df = new tajmme.DateField(fixtures.date, 
            id("y"),
            id("w"),
            id("d")
        );

        var sundayBefore = new Date(df.currentDate.getTime() - (3 * 24 * 60 * 60 * 1000));

        var values = df.dateToValues(sundayBefore);

        expect(values.day).toBe(7)
    });
    
    it("sets values to the 3 fields", function () {
        var df = new tajmme.DateField(fixtures.date, 
            id("y"),
            id("w"),
            id("d")
        );

        df.setFieldValues({year: fixtures.y, week: fixtures.w, day: fixtures.d})

        expect(parseInt(id("y").value, 10)).toBe(fixtures.y)
        expect(parseInt(id("w").value, 10)).toBe(fixtures.w)
        expect(parseInt(id("d").value, 10)).toBe(fixtures.d)

        expect(parseInt(df.fields.year.value, 10)).toBe(fixtures.y)
        expect(parseInt(df.fields.week.value, 10)).toBe(fixtures.w)
        expect(parseInt(df.fields.day.value, 10)).toBe(fixtures.d)
    });

    it("increases or decreases the date using days", function () {
        var df = new tajmme.DateField(fixtures.date, 
            id("y"),
            id("w"),
            id("d")
        );

        df.increase(1);
        expect(df.currentDate.getDay()).toBe(fixtures.d + 1)        
        expect(df.currentDate.getWeek()).toBe(fixtures.w)        
        expect(df.currentDate.getFullYear()).toBe(fixtures.y)       

        df.increase(-1);
        expect(df.currentDate.getDay()).toBe(fixtures.d)        
        expect(df.currentDate.getWeek()).toBe(fixtures.w)        
        expect(df.currentDate.getFullYear()).toBe(fixtures.y)

        df.increase(7);
        expect(df.currentDate.getDay()).toBe(fixtures.d)        
        expect(df.currentDate.getWeek()).toBe(fixtures.w + 1)        
        expect(df.currentDate.getFullYear()).toBe(fixtures.y)

        df.increase(-7);
        expect(df.currentDate.getDay()).toBe(fixtures.d)        
        expect(df.currentDate.getWeek()).toBe(fixtures.w)        
        expect(df.currentDate.getFullYear()).toBe(fixtures.y)

        df.increase(360);
        expect(df.currentDate.getFullYear()).toBe(fixtures.y + 1)

        df.increase(-360);
        expect(df.currentDate.getFullYear()).toBe(fixtures.y)
    });

    it("can attach buttons which increases or decreases the date on click", function () {
        var df = new tajmme.DateField(fixtures.date, 
            id("y"),
            id("w"),
            id("d")
        );

        df.button("#plus", 2);
        df.button("#minus", -1);

        id("plus").onclick();
        expect(df.currentDate.getDay()).toBe(fixtures.d + 2)        
        expect(df.currentDate.getWeek()).toBe(fixtures.w)        
        expect(df.currentDate.getFullYear()).toBe(fixtures.y)

        id("minus").onclick();
        expect(df.currentDate.getDay()).toBe(fixtures.d + 1)        
        expect(df.currentDate.getWeek()).toBe(fixtures.w)        
        expect(df.currentDate.getFullYear()).toBe(fixtures.y)
    });
});