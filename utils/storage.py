import tempfile
import uuid

from storage3.exceptions import StorageApiError

from utils.supabase import get_supabase_client


def get_or_create_bucket_for_user(user_id: uuid.UUID):
    """Get or create a bucket for the given applicant"""
    supabase = get_supabase_client()

    str_id = str(user_id)
    try:
        return supabase.storage.get_bucket(str_id)
    except StorageApiError as e:
        if e.status != "404":
            raise
        supabase.storage.create_bucket(str_id)
        return supabase.storage.get_bucket(str_id)


def delete_file_from_bucket(bucket_name: str, file_name: str) -> None:
    supabase = get_supabase_client()
    supabase.storage.from_(bucket_name).remove([file_name])


def upload_file_to_bucket(file: bytes, bucket_name: str, file_name: str, options=None):
    if options is None:
        options = {"upsert": False, "contentType": "application/pdf"}

    supabase = get_supabase_client()
    with tempfile.NamedTemporaryFile() as temp_file:
        temp_file.write(file)
        temp_file.flush()

        supabase.storage.from_(bucket_name).upload(
            file=temp_file.name, path=file_name, file_options=options
        )
