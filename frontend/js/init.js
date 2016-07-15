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

    g.tajmme.add('vendor:chart:barchart', function () {
        Chart.defaults.global.animation.duration = 0;
        var ajax = new XMLHttpRequest(),
            cvs = document.querySelector('[data-bar-chart-time]'),
            from_date = cvs.dataset.startdate,
            to_date = cvs.dataset.enddate;

        ajax.open('GET', '/chartsjs/week_chart.js?from=' + from_date + '&to=' + to_date, true);
        ajax.onload = function () {
            var data = JSON.parse(ajax.responseText),
                myBarChart = new Chart(cvs, {
                type: 'bar',
                data: data,
                options: {
                    responsive: false
                }
            });
        };
        ajax.send();
    });

    g.tajmme.add('vendor:chart:hbarchart', function () {
        Chart.defaults.global.animation.duration = 0;
        var ajax = new XMLHttpRequest(),
            cvs = document.querySelector('[data-bar-chart-projects]'),
            from_date = cvs.dataset.startdate,
            to_date = cvs.dataset.enddate;

        ajax.open('GET', '/chartsjs/projects_chart.js?from=' + from_date + '&to=' + to_date, true);
        ajax.onload = function () {
            var data = JSON.parse(ajax.responseText),
                myBarChart = new Chart(cvs, {
                type: 'horizontalBar',
                data: data,
                options: {
                    responsive: false
                }
            });
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