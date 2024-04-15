import csv
from datetime import datetime
from decimal import Decimal

from libsql_client import Transaction
from pydash import map_

from api.bills._m.insert_bill import insert_bill
from api.bills._m.update_bills import update_main_tag
from api.bills.model import Bill
from api.bills.tags._m.insert_bills_tags import insert_bills_tags
from api.bills.tags._m.insert_tag import insert_tag
from api.bills.tags._q.check_tag import check_tag
from api.bills.tags.model import BillTag, Tag
from api.logger import RequestLogger


def __treat_csv_row_data(row: dict):
    tags_list = row["tags"].split(",")
    tags_list = [tag.lstrip() for tag in tags_list]
    str_date_time = row["date"] + "T" + row["time"] + ":00Z"
    date = datetime.strptime(str_date_time, "%Y-%m-%dT%H:%M:%SZ")
    bill_value_float_to_int = int(Decimal(row["number"]) * 100)
    main_tag = row["main_tag"]
    return tags_list, date, bill_value_float_to_int, main_tag


async def create_new_bills_from_csv(t: Transaction, logger: RequestLogger, text: str):
    log = logger.getChild(__name__, __file__)
    try:
        log.debug(f"create_new_bills_from_csv {text}")
        reader = csv.DictReader(text.splitlines())
        for row in reader:
            tagnames_list, date, bill_value_float_to_int, main_tag_name = __treat_csv_row_data(row)
            new_bill = Bill(name=row["name"], value=bill_value_float_to_int, date=date)
            [new_bill_db_result] = await insert_bill(t, log, new_bill)

            main_tag = await check_tag(t, log, main_tag_name)
            main_tag = main_tag[0] if len(main_tag) != 0 else None
            if not main_tag:
                [new_tag] = await insert_tag(t, log, Tag(name=main_tag_name))
                main_tag = new_tag
            await update_main_tag(
                    t, log, main_tag_id=main_tag.id, bill_id=new_bill_db_result.id
                )
            
            bill_tag_ids = []
            new_tags = []
            for tagname in tagnames_list:
                tag = await check_tag(t, log, name=tagname)
                tag = tag[0] if len(tag) != 0 else None
                if tag:
                    bill_tag_ids.append(BillTag(
                        bill_id=new_bill_db_result.id, tag_id=tag.id)
                    )
                else:
                    new_tags.append(Tag(name=tagname))
            
            created_tags = await insert_tag(t, log, *new_tags)
            bill_tag_ids.extend(map_(created_tags, lambda x: BillTag(bill_id = new_bill_db_result.id, tag_id = x.id)))
            await insert_bills_tags(t, log, *bill_tag_ids)
            log.debug(f"create_new_bills_from_csv success")
    except Exception as e:
        log.exception("failed in create_new_bills_from_csv", exc_info=e)
        raise e
