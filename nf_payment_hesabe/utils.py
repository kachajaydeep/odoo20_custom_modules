# -*- coding: utf-8 -*-
# Copyright (C) 2021-Today: Part of NextFlowIT.
# @author:  Part of NextFlowIT.

import http.client
import logging

_logger = logging.getLogger(__name__)


def checkout(encencryptedText, url, access_code, env):
    url = url.replace("https://", "").replace("http://", "")

    if env != 'production':
        _logger.info('Hesabe: Payment URL:' + url)
        _logger.info('Hesabe: Access Code:' + access_code)
        _logger.info('Hesabe: Encrypted:' + encencryptedText)

    boundary = 'wL36Yn8afVp8Ag7AmP8qZ0SA4n1v9T'

    headers = {
        'accesscode': access_code,
        'Cookie': 'api_20_hesabe_payment_collection_company_session=eyJpdiI6IjFxVDc3YWJ1MFNZcUFrNnVzbkdUMnc9PSIsInZhbHVlIjoiWEtwcDVrSmY0MlQvK255ZDBIZEdUWXE5ZHFvMWNzcVJYc0NyZStQVFQvS3hqRGJBZkF4aThGWWEvR1dSbytUWklicEdqdnB4dXJ6bmJkUlZ6WmlwSjh4dElHcGZTaElDb1UvR3ZVT0V3VGcvQlBmQ205ZCs4VkRtUEM4Vi9kK2oiLCJtYWMiOiI1MGYzYjk3MWMwMjYzZjE5Mzg3M2IyMzRmMWM4YzcwY2JiN2NiODc1MThjOWI0YzFmNmM5OTg0ZDAxNTc1ZWU2IiwidGFnIjoiIn0%3D',
        'Content-type': 'multipart/form-data; boundary={}'.format(boundary)
    }

    payload = '\r\n'.join([
        '--' + boundary,
        'Content-Disposition: form-data; name=data;',
        'Content-Type: {}'.format('text/plain'),
        '',
        encencryptedText,
        '--' + boundary + '--',
        '',
    ]).encode('utf-8')
    connection = http.client.HTTPSConnection(url)
    connection.request("POST", "/checkout", payload, headers)
    response = connection.getresponse()
    response_data = response.read()

    if env != 'production':
        _logger.info('Hesabe: Response: ' + response_data.decode("utf-8"))

    return response_data.decode("utf-8").strip()
