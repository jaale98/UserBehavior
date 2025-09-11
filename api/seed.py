from api.db import SessionLocal
from api.models import UIElement, UIType, User
from werkzeug.security import generate_password_hash

def main():
    db = SessionLocal()
    try:
        if not db.query(User).filter_by(username="demo").first():
            u = User(username="demo", password_hash=generate_password_hash("demo123"))
            db.add(u)
        
        defaults = [
            dict(type=UIType.button,     label="Blue Button",  key="btn_blue"),
            dict(type=UIType.button,     label="Red Button",   key="btn_red"),
            dict(type=UIType.text_input, label="Note Box",     key="txt_note"),
            dict(type=UIType.text_input, label="Idea Box",     key="txt_idea"),
        ]
        for d in defaults:
            if not db.query(UIElement).filter_by(key=d["key"]).first():
                db.add(UIElement(**d))

        db.commit()
        print("Seed complete.")
    finally:
        db.close()

if __name__ == "__main__":
    main()            