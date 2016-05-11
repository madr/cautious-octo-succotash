# -*- coding: utf-8 -*-
from datetime import datetime

from xlsx import Workbook

from .lib.random import names, projects

in_file = '/Users/ay/Dropbox/tajmme-shared/all-tid-201506-201509.xlsx'


def import_from_xlsx():
    book = Workbook(in_file)

    for sheet in book:
        for i, row in sheet.rowsIter():
            if i == 1:
                continue

            description = '(left blank)'

            if len(row) == 21:
                description = row[20].value

            done_at = datetime.strptime(str(row[5].value), '(%Y, %m, %d, 0, 0, 0)')

            project = row[1].value

            # p = Progress(
            #     project=projects[project],
            #     done_at=done_at.strftime('%Y-%m-%d'),
            #     user=names[int(row[2].value)],
            #     duration=int(float(row[15].value) * 60),
            #     description=description,
            #     billable=float(row[16].value) == 0
            # )

            # p.save()

    print(len(Progress.objects))


if __name__ == '__main__':
    import_from_xlsx()
