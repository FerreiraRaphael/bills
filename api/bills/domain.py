# import aiofiles
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


async def create_new_bills_from_csv(t: Transaction, text: str):
    reader = csv.DictReader(text.splitlines())
    first_row = next(reader)
    tags_list = first_row["tags"].split(",")
    str_date_time = first_row["date"] + "T" + first_row["time"] + "Z"
    date = datetime.strptime(str_date_time, "%Y-%m-%dT%H:%M:%SZ")
    new_bill = Bill(name=first_row["name"], value=float(first_row["number"]), date=date)
    new_bill_db_result = await insert_bill(t, new_bill)
    bill_dict = new_bill_db_result[0].dict()
    main_tag = first_row["main_tag"]

    for tag in tags_list:
        tag_id = await check_tag(t, name=tag)
        if len(tag_id) != 0:
            tag_dict = tag_id[0]
            bill_tag_ids = BillTag(
                bill_id=int(bill_dict["id"]), tag_id=int(tag_dict["id"])
            )
            await insert_bills_tags(t, bill_tag_ids)
        else:
            new_tag = await insert_tag(t, Tag(name=tag))
            tag_dict = new_tag[0].dict()
            bill_tag_ids = BillTag(
                bill_id=int(bill_dict["id"]), tag_id=int(tag_dict["id"])
            )
            await insert_bills_tags(t, bill_tag_ids)

    main_tag_id = await check_tag(t, main_tag)

    if len(main_tag_id) != 0:
        main_tag_dict = main_tag_id[0]
        update_main_tag(t, int(main_tag_dict["id"]), int(bill_dict["id"]))
    else:
        new_tag = await insert_tag(t, Tag(name=main_tag))
        tag_dict = new_tag[0].dict()
        update_main_tag(t, int(tag_dict["id"]), int(bill_dict["id"]))
