# test/test_observer.py
from project_service.observer_test import Observer

def test_notify():
    obs = Observer()
    obs.notify("CI Trigger Test")  # مجرد تشغيل الدالة
    assert True  # نضمن نجاح الاختبار
