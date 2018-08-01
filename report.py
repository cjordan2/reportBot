import datetime
import random

header = """
RUN DATE:     {0}                                                                                                                                       Page  1
transum.lis                                                      PAYCHEX DIRECT DEPOSIT SYSTEM
                                                                          READYCHEX          
                                                                DIRECT PAY Transaction Summary
                                                              For Period {1} To {2}

  {3}-{4} {5}
8385975

TRANS    CHECK    POST     EFF      BANK CHECK  POSPAY     CLIENT         CLIENT     PR Run  File   TRANS            Prod   AMOUNT     COMMENTS
DATE     DATE     DATE     DATE     CODE ID     FILE ID    ACCT           R/T         No     Bypass TYPE             Code


BEGINNING BALANCE                                                                                                              0.00

"""

line_item = "{0} {1} {2}           {3:>2}       0      1         XXXXXX9589  2131310-3                 Man Chck Iss           -154.15 Refund CCK # 18631 for BINGHAMTON CAROUSEL RESTAUR"

footer = """
BALANCE                                                                                                                     -154.15


TOTAL PENDING                                                                                                                  0.00


ADJUSTED BALANCE                                                                                                            -154.15
"""

def get_random_line_item():
    return line_item.format(
        datetime.datetime.now().strftime('%m/%d/%y'),
        datetime.datetime.now().strftime('%m/%d/%y'),
        datetime.datetime.now().strftime('%m/%d/%y'),
        random.randrange(0, 100)
    )

def get_report(start_date, end_date, branch, client, name):
    formatted_header = header.format(
        datetime.datetime.now().strftime('%m-%b-%y %H:%M').upper(),
        start_date,
        end_date,
        branch,
        client,
        name
    )

    formatted_line_items = [
        get_random_line_item() for x in range(100)
    ]

    return formatted_header + '\n'.join(formatted_line_items) + footer
