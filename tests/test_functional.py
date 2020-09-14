import pytest


@pytest.mark.parametrize(
    "method,path",
    [
        ('get_html', '/'),
        ('get_html', '/contributions'),
        ('get_html', '/contributions/5'),
        ('get_html', '/units'),
        ('get_html', '/units/9'),
    ])
def test_pages(app, method, path):
    getattr(app, method)(path)
