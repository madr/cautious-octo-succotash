describe("TimeSpent", function () {
  it("has all code present", function () {
    expect(tajmme).not.toBe(undefined);
    expect(tajmme.TimeSpent).not.toBe(undefined);
  });

  it("takes an id or element reference", function () {
    var f, tsf;
    f = document.createElement("input");
    f.id = "something";
    document.body.appendChild(f);
    
    tsf = new tajmme.TimeSpent("#something");
    expect(tsf.field.id).toBe("something");

    document.body.removeChild(f);
    tsf = '';

    tsf = new tajmme.TimeSpent(f);
    expect(tsf.field.id).toBe("something");

    tsf = '';
  });

  it("increases and decreases value", function () {
    var f, tsf;
    f = document.createElement("input");
    f.id = "something";
    f.value = "00:15";
    document.body.appendChild(f);
    
    tsf = new tajmme.TimeSpent("#something");
  
  tsf.increase(15);
    expect(tsf.field.value).toBe("00:30");

  tsf.increase(60);
    expect(tsf.field.value).toBe("01:30");

  tsf.increase(-15);
    expect(tsf.field.value).toBe("01:15");

  tsf.increase(-30);
    expect(tsf.field.value).toBe("00:45");

    document.body.removeChild(f);
    tsf = '';
  });

  it("makes sure padding is correct in hh:mm", function () {
    var f, tsf;
    f = document.createElement("input");
    f.id = "something";
    f.value = "00:15";
    document.body.appendChild(f);
    
    tsf = new tajmme.TimeSpent("#something");
  
    expect(tsf.correct(15)).toBe("00:15");
    expect(tsf.correct(60)).toBe("01:00");

    document.body.removeChild(f);
    tsf = '';
  });

  it("defaults bogus values to 00:15", function () {
    var f, tsf;
    f = document.createElement("input");
    f.id = "something";
    document.body.appendChild(f);
    
    tsf = new tajmme.TimeSpent("#something");
  
    expect(tsf.correct("bajs")).toBe("00:15");
    expect(tsf.correct(true)).toBe("00:15");
    expect(isNaN(true)).toBe(false);
    expect(tsf.correct(false)).toBe("00:15");

    document.body.removeChild(f);
    tsf = '';
  });

  it("defaults negative values to 00:00", function () {
    var f, tsf;
    f = document.createElement("input");
    f.id = "something";
    document.body.appendChild(f);
    
    tsf = new tajmme.TimeSpent("#something");
  
    expect(tsf.correct(-1)).toBe("00:00");
    expect(tsf.correct(0)).toBe("00:00");

    document.body.removeChild(f);
    tsf = '';
  });

  it("transforms minutes to hh:mm", function () {
    var f, tsf;
    f = document.createElement("input");
    f.id = "something";
    document.body.appendChild(f);
    
    tsf = new tajmme.TimeSpent("#something");
  
    expect(tsf.correct(90)).toBe("01:30");
    expect(tsf.correct(30)).toBe("00:30");
    expect(tsf.correct(120)).toBe("02:00");
    expect(tsf.correct(1215)).toBe("20:15");

    document.body.removeChild(f);
    tsf = '';
  });

  it("round minutes to closest upper quarter", function () {
    var f, tsf;
    f = document.createElement("input");
    f.id = "something";
    document.body.appendChild(f);
    
    tsf = new tajmme.TimeSpent("#something");
  
    expect(tsf.correct(87)).toBe("01:30");
    expect(tsf.correct(26)).toBe("00:30");
    expect(tsf.correct(106)).toBe("02:00");
    expect(tsf.correct(1201)).toBe("20:15");

    document.body.removeChild(f);
    tsf = '';
  });

  it("transform timestamp to minutes", function () {
    var f, tsf;
    f = document.createElement("input");
    f.id = "something";
    document.body.appendChild(f);
    
    tsf = new tajmme.TimeSpent("#something");
  
    expect(tsf.toMinutes("00:15")).toBe(15);
    expect(tsf.toMinutes("10:00")).toBe(600);
    expect(tsf.toMinutes("02:45")).toBe(165);

    document.body.removeChild(f);
    tsf = '';
  });

  it("transform 'Xh', 'X h', 'X hour', 'X hours' to X*60 minutes (including singular)", function () {
    var f, tsf;
    f = document.createElement("input");
    f.id = "something";
    document.body.appendChild(f);
    
    tsf = new tajmme.TimeSpent("#something");
  
    expect(tsf.toMinutes("8h")).toBe(60*8);
    expect(tsf.toMinutes("1hour")).toBe(1*60);
    expect(tsf.toMinutes("2hours")).toBe(2*60);
    expect(tsf.toMinutes("16 h")).toBe(60*16);
    expect(tsf.toMinutes("1 hour")).toBe(1*60);
    expect(tsf.toMinutes("2 hours")).toBe(2*60);
    
    document.body.removeChild(f);
    tsf = '';
  });

  it("transform 'Xm' or 'X m' to X minutes (including singular)", function () {
    var f, tsf;
    f = document.createElement("input");
    f.id = "something";
    document.body.appendChild(f);
    
    tsf = new tajmme.TimeSpent("#something");
  
    expect(tsf.toMinutes("8m")).toBe(8);
    expect(tsf.toMinutes("234m")).toBe(234);
    expect(tsf.toMinutes("8 m")).toBe(8);
    expect(tsf.toMinutes("234 m")).toBe(234);
    expect(tsf.toMinutes("8minutes")).toBe(8);
    expect(tsf.toMinutes("234minutes")).toBe(234);
    expect(tsf.toMinutes("8 minutes")).toBe(8);
    expect(tsf.toMinutes("234 minutes")).toBe(234);

    document.body.removeChild(f);
    tsf = '';
  });

  it("transforms '1h 30m' to minutes (in all variations)", function () {
    var f, tsf;
    f = document.createElement("input");
    f.id = "something";
    document.body.appendChild(f);
    
    tsf = new tajmme.TimeSpent("#something");
  
    expect(tsf.toMinutes("2h8m")).toBe(128);
    expect(tsf.toMinutes("2 h8m")).toBe(128);
    expect(tsf.toMinutes("2h 8m")).toBe(128);
    expect(tsf.toMinutes("2 h 8m")).toBe(128);
    expect(tsf.toMinutes("2h8 m")).toBe(128);
    expect(tsf.toMinutes("2 h8 m")).toBe(128);
    expect(tsf.toMinutes("2h 8 m")).toBe(128);
    expect(tsf.toMinutes("2 h 8 m")).toBe(128);

    document.body.removeChild(f);
    tsf = '';
  });

  it("register button clicks", function () {
    var b1, b2, f, tsf;
    f = document.createElement("input");
    f.id = "something";
    document.body.appendChild(f);

    b1 = document.createElement("button");
    b1.id = "increase";
    b2 = document.createElement("button");
    b2.id = "decrease";
    document.body.appendChild(b1);
    document.body.appendChild(b2);
    
    tsf = new tajmme.TimeSpent("#something");
    tsf.button("#increase", 30);
    tsf.button("#decrease", -15);

    b1.onclick();
  
    expect(tsf.field.value).toBe("00:30");

    b2.onclick();

    expect(tsf.field.value).toBe("00:15");

    document.body.removeChild(f);
    document.body.removeChild(b1);
    document.body.removeChild(b2);
    tsf = '';
  });

  it("handles frequent decreasion (button spam)", function () {
    var f, tsf;
    f = document.createElement("input");
    f.id = "something";
    f.value = "01:00";
    document.body.appendChild(f);
    
    tsf = new tajmme.TimeSpent("#something");
  
    tsf.increase(-30);
    expect(tsf.field.value).toBe("00:30");

    tsf.increase(-30);
    expect(tsf.field.value).toBe("00:00");

    tsf.increase(-30);
    expect(tsf.field.value).toBe("00:00");

    tsf.increase(-30);
    expect(tsf.field.value).toBe("00:00");

    tsf.increase(-30);
    expect(tsf.field.value).toBe("00:00");

    tsf.increase(-30);
    expect(tsf.field.value).toBe("00:00");
  });
});