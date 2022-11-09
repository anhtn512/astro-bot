import os
from datetime import datetime, date

import requests
import pandas as pd

time_format = '%Y-%m-%dT%H:%M:%S.%fZ'
DAOs = [
    "news.sputnik-dao.near",
    "nearweek-news-contribution.sputnik-dao.near"
]
DAO = DAOs[1]
PROPOSAL_PREFIX = "https://app.astrodao.com/dao/" + DAO + "/proposals/"
GET_PROPOSALS_URL = 'https://api.app.astrodao.com/api/v1/proposals'
DAO_LINK_PREFIX = "https://api.app.astrodao.com/api/v1/daos/"
PROPOSAL_LINK_PREFIX = "https://api.app.astrodao.com/api/v1/proposals/"
format_date = "%m%d%Y"
FOLDER_RESULT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "results")
if not os.path.isdir(FOLDER_RESULT):
    os.mkdir(FOLDER_RESULT)


def get_day_from_arg(first_day):
    return datetime.strptime(first_day, format_date)


def string_to_datetime(datetime_string):
    datetime_object = datetime.strptime(datetime_string, time_format)
    return datetime_object


def simplify_proposal(proposal):
    proposal_id = proposal['id']
    link_proposal = "{}{}".format(PROPOSAL_PREFIX, proposal["id"])
    proposer = proposal["proposer"]
    content = proposal["description"].split("$$$$")
    description, link = content[0], content[1]
    description = description.replace("\n", "").replace("\b", "").encode("ascii", "ignore").decode().strip()
    return {
        "proposalId": proposal['proposalId'],
        "id": proposal_id,
        "link_proposal": link_proposal,
        "proposer": proposer,
        "description": description,
        "link": link,
        "created_at": proposal["createdAt"],
        "updated_at": proposal["updatedAt"],
        'status': proposal['status'],
        'type': proposal['type']
    }


def get_dao(dao):
    link_dao = DAO_LINK_PREFIX + dao
    res = requests.get(link_dao, allow_redirects=False)
    if res.status_code == 400:
        return None
    return res.json()


def get_proposals_by_offset(offset=0, order_by='updatedAt', order='DESC', dao=DAO, status='Approved', type='Transfer'):
    queries = '?offset={}&orderBy={}&order={}&dao={}&status={}&type={}'.format(offset, order_by, order, DAO, status, type)
    link = '{}{}'.format(GET_PROPOSALS_URL, queries)
    res = requests.get(link)
    res = res.json()
    return res['data']


def get_proposal_by_id(id):
    proposal_id = "{}-{}".format(DAO, id)
    link_proposal = PROPOSAL_LINK_PREFIX + proposal_id
    res = requests.get(link_proposal, allow_redirects=False)
    if res.status_code == 400:
        return None
    proposal = res.json()
    return proposal


def get_proposals_from_id(start_id):
    dao = get_dao(DAO)
    last_proposal_id = dao["lastProposalId"]
    id = start_id
    proposals = []
    while True:
        proposal = get_proposal_by_id(id)
        if id > last_proposal_id:
            break
        if proposal is not None:
            proposals.append(proposal)
        id += 1
    data = []
    for proposal in proposals:
        temp = simplify_proposal(proposal)
        data.append({
            "created_at": temp["created_at"],
            "updated_at": temp["updated_at"],
            "tags": "",
            "title": temp["description"],
            "link": temp["link"],
            "link_proposal": temp['link_proposal'],
            "source": "x",
            "sputnik": temp["proposalId"],
            "collector": temp["proposer"]
        })
    df = pd.DataFrame(data)
    output_filename = "proposals_from_{}_to_{}.xlsx".format(start_id, last_proposal_id)
    output = os.path.join(FOLDER_RESULT, output_filename)
    df.to_excel(output, index=False)
    return output, df


def get_proposals_from_day(end_day):
    offset = 0
    proposals = get_proposals_by_offset()
    while True:
        temp = string_to_datetime(proposals[-1]['updatedAt'])
        if temp > end_day:
            offset += 50
            proposals += get_proposals_by_offset(offset)
        else:
            break
    return proposals


def get_proposals_approved_from_day(start_day):
    start = get_day_from_arg(start_day)
    proposals = get_proposals_from_day(start)
    data = []
    for proposal in proposals:
        update_time = string_to_datetime(proposal['updatedAt'])
        temp = simplify_proposal(proposal)
        if update_time > start and proposal['status'] == 'Approved':
            data.append({
                "created_at": temp["created_at"],
                "updated_at": temp["updated_at"],
                "tags": "",
                "title": temp["description"],
                "link": temp["link"],
                "link_proposal": temp['link_proposal'],
                "source": "x",
                "sputnik": temp["proposalId"],
                "collector": temp["proposer"]
            })
    df = pd.DataFrame(data)
    today = date.today()
    today_str = today.strftime(format_date)
    output_filename = "approved_from_{}_to_{}.xlsx".format(start_day, today_str)
    output = os.path.join(FOLDER_RESULT, output_filename)
    df.to_excel(output, index=False)
    return output, df
