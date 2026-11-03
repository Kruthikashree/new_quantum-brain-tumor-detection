from database.mongodb import reports
import shutil
import os

confirm = input("This will permanently delete ALL reports. Type 'yes' to continue: ")
if confirm.strip().lower() == "yes":
    count = reports.count_documents({})
    reports.delete_many({})
    print(f"Deleted {count} report(s).")

    upload_dir = os.path.join(os.path.dirname(__file__), "uploads", "reports")
    if os.path.isdir(upload_dir):
        shutil.rmtree(upload_dir)
        os.makedirs(upload_dir, exist_ok=True)
        print("Cleared uploaded MRI image files.")
else:
    print("Cancelled.")