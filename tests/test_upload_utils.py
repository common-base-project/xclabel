import os
import sys
import types
import pytest

cv2_stub = types.SimpleNamespace(
    imread=lambda *a, **k: None,
    imwrite=lambda *a, **k: True,
    VideoCapture=lambda *a, **k: types.SimpleNamespace(
        get=lambda *a, **k: 1,
        read=lambda: (False, None),
        release=lambda: None,
    ),
)
sys.modules['cv2'] = cv2_stub

sys.path.append(os.path.dirname(os.path.dirname(__file__)))
from app.utils.UploadUtils import UploadUtils

class DummyFile:
    def __init__(self, name, content_type='image/jpeg', content=b'data'):
        self.name = name
        self.content_type = content_type
        self._content = content
        self.size = len(content)

    def read(self):
        return self._content

def test_upload_model_test_image_valid(tmp_path):
    upload = UploadUtils()
    file = DummyFile('valid.jpg')
    ret, msg, info = upload.upload_model_test_image(str(tmp_path), file)
    assert ret is True
    assert info['file_name'] == 'valid.jpg'
    assert (tmp_path / 'valid.jpg').exists()

def test_upload_model_test_image_invalid_path(tmp_path):
    upload = UploadUtils()
    file = DummyFile('../bad.jpg')
    ret, msg, info = upload.upload_model_test_image(str(tmp_path), file)
    assert ret is False
    assert 'Invalid file name' in msg

def test_upload_model_test_image_invalid_chars(tmp_path):
    upload = UploadUtils()
    file = DummyFile('bad|name.jpg')
    ret, msg, info = upload.upload_model_test_image(str(tmp_path), file)
    assert ret is False
    assert 'Invalid file name' in msg

def test_upload_model_test_image_write_error(tmp_path, monkeypatch):
    upload = UploadUtils()
    file = DummyFile('valid.jpg')
    def fake_write_file(path, data):
        raise IOError('fail')
    monkeypatch.setattr(upload, '_write_file', fake_write_file)
    ret, msg, info = upload.upload_model_test_image(str(tmp_path), file)
    assert ret is False
    assert 'fail' in msg
