import logging

import requests
import logging


def download_scorecards(logger=logging.getLogger()):
    logger.info(f'Try to download scorecards')
    try:
        cookies = {}
        login_info = {
            'username': 'arina@pafnuteva.ru',
            'password': 'yuhv82kd',
            'cookieYes': 0
        }
        try_login = requests.post('https://my.spotonlearning.eu/ehio/site/user.cfc?method=doLogin',
                                  data=login_info)
        cookies['JSESSIONID'] = try_login.headers.get('JSESSIONID')
        cookies['CFID'] = try_login.headers.get('CFID')
        cookies['CFTOKEN'] = try_login.headers.get('CFTOKEN')

        check = requests.get('https://my.spotonlearning.eu/manage/courses/download.cfm?&courseId=0',
                             cookies=cookies)
        logger.info(f'Status of check: {check.status_code}')
        try_request_participants = requests.get('https://my.spotonlearning.eu/manage/excel/output/participants.xls',
                                                cookies=cookies)
        with open('participants.xls', 'wb') as f:
            f.write(try_request_participants.content)
        logger.info(f'Downloading and saving finished successful')
        return True
    except Exception as e:
        logger.info(f'Downloading and saving was failed')
        logger.error(str(e))
        return False
