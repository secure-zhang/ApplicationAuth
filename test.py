import uuid

uuid_str = uuid.uuid4()
tmp_file_name = 'img-%s.png' % uuid_str
print(tmp_file_name)