import secrets
from pymongo.errors import DuplicateKeyError


def insert_with_unique_code(reports, doc, attempts=10):
    """
    Inserts the report with a random 6-digit code. The database's unique
    index guarantees no two reports share a code; on a clash we retry.
    The code is random, so it reveals nothing about the patient.
    """
    for _ in range(attempts):
        doc["referral_code"] = str(secrets.randbelow(900000) + 100000)
        try:
            return reports.insert_one(doc).inserted_id
        except DuplicateKeyError:
            doc.pop("_id", None)
    raise RuntimeError("Could not generate a unique referral code")