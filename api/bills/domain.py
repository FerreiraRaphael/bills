import csv
from datetime import datetime

from libsql_client import Transaction

from api.bills._m.insert_bill import insert_bill
from api.bills._m.update_bills import update_main_tag
from api.bills.model import Bill
from api.bills.tags._m.insert_bills_tags import insert_bills_tags
from api.bills.tags._m.insert_tag import insert_tag
from api.bills.tags._q.check_tag import check_tag
from api.bills.tags.model import BillTag, Tag
from api.logger import RequestLogger


def treat_csv_row_data(row: dict):
    tags_list = row["tags"].split(",")
    tags_list = [tag.lstrip() for tag in tags_list]
    str_date_time = row["date"] + "T" + row["time"] + ":00Z"
    date = datetime.strptime(str_date_time, "%Y-%m-%dT%H:%M:%SZ")
    number_float_to_int = int(round(float(row["number"]) * 100))
    main_tag = row["main_tag"]
    return tags_list, date, number_float_to_int, main_tag


async def create_new_bills_from_csv(t: Transaction, log: RequestLogger, text: str):
    reader = csv.DictReader(text.splitlines())
    for row in reader:
        tags_list, date, number_float_to_int, main_tag = treat_csv_row_data(row)
        new_bill = Bill(name=row["name"], value=number_float_to_int, date=date)
        new_bill_db_result = await insert_bill(t, log, new_bill)
        bill_dict = new_bill_db_result[0].dict()
        main_tag_id = await check_tag(t, log, main_tag)

        if len(main_tag_id) != 0:
            main_tag_dict = main_tag_id[0]
            await update_main_tag(
                t, log, main_tag_id=main_tag_dict["id"], bill_id=bill_dict["id"]
            )
        else:
            new_tag = await insert_tag(t, log, Tag(name=main_tag))
            main_tag_dict = new_tag[0].dict()
            await update_main_tag(
                t, log, main_tag_id=main_tag_dict["id"], bill_id=bill_dict["id"]
            )

        for tag in tags_list:
            tag_id = await check_tag(t, log, name=tag)
            if len(tag_id) != 0:
                tag_dict = tag_id[0]
                bill_tag_ids = BillTag(
                    bill_id=int(bill_dict["id"]), tag_id=int(tag_dict["id"])
                )
                await insert_bills_tags(t, log, bill_tag_ids)
            else:
                new_tag = await insert_tag(t, log, Tag(name=tag))
                tag_dict = new_tag[0].dict()
                bill_tag_ids = BillTag(
                    bill_id=int(bill_dict["id"]), tag_id=int(tag_dict["id"])
                )
                await insert_bills_tags(t, log, bill_tag_ids)
