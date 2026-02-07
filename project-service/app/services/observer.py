# observer_test.py


class Observer:
    def notify(self, message):
        print(f"[Observer] {message}")


# --------- TEST / CHANGE ---------
observer = Observer()
observer.notify(
    "Testing CI trigger!"
)  # ✅ هذا السطر الجديد رح يعتبر تغيير ويشغل الـ CI
