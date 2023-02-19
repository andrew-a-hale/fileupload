import uuid
from pydantic import BaseModel, PydanticValueError, root_validator, Field


class PayloadBase(BaseModel):
    guid: uuid.UUID = Field(default_factory=uuid.uuid4)
    manifest_guid: uuid.UUID
    bucket_guid: uuid.UUID
    filename: str
    content_type: str
    md5: str


class PayloadCreate(PayloadBase):
    guid: uuid.UUID = Field(default_factory=uuid.uuid4)
    manifest_filename: str
    manifest_md5: str

    @root_validator(pre=True)
    def compare_manifest_and_payload(cls, values):
        if values['manifest_filename'] != values['filename']:
            raise ManifestPayloadFilenameNotEqualError(
                manifest_filename=values['manifest_filename'],
                file_filename=values['filename'])
        if values['manifest_md5'] != values['md5']:
            raise ManifestPayloadMd5NotEqualError(
                manifest_md5=values['manifest_md5'], file_md5=values['md5'])
        return values

class PayloadRead(PayloadBase):
    pass

class Payload(PayloadBase):
    id: int


class ManifestPayloadFilenameNotEqualError(PydanticValueError):
    code = 'manifest_payload_filename_not_equal'
    msg_template = 'Manifest Filename and File Filename must match, got Filename MD5: {manifest_filename} and File MD5: {file_filename}'


class ManifestPayloadMd5NotEqualError(PydanticValueError):
    code = 'manifest_payload_filename_not_equal'
    msg_template = 'Manifest MD5 and File MD5 must match, got Manifest MD5: {manifest_md5} and File MD5: {file_md5}'
