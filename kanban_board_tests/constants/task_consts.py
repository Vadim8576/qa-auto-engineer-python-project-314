STATUS_TO_ID = {
    'Draft': '1',
    'To Review': '2',
    'To Be Fixed': '3',
    'To Publish': '4',
    'Published': '5'
}

ID_TO_STATUS = {v: k for k, v in STATUS_TO_ID.items()}