from abc import ABC, abstractmethod
from base64 import b64decode
import binascii
import json
from dataclasses import asdict, dataclass, field
from typing import Any, Dict, List, Optional, cast
from service.server import (
    Options,
    RawListResponse,
    RawTransformDocumentPipeRequest,
    RawTransformDocumentRequest,
    RawTransformDocumentResponse,
    RawTransformDocumentPipeResponse,
)

# its models raw responses

# TODO: remove boilerplate code
# TODO: consider to create a warning if the document is empty

# TODO: consider to use a normal class here insteat of dataclasses because of the weird issure with intellisense
# TODO: consider to use a dataclasses if the problem is solved with having a dataclass and properties


class BaseModel(ABC):
    @abstractmethod
    def as_dict(self) -> Any:
        pass

    def as_json(self, indent: Optional[int] = None) -> str:
        """Creates a serialized json string from the object instance.

        Returns:
            str: A json string.
        """
        return json.dumps(self.as_dict(), indent=indent)


class TransformDocumentRequest(BaseModel):
    def __init__(
        self,
        document: str,
        service_name: str,
        file_name: Optional[str] = None,
        options: Optional[Options] = None,
    ) -> None:
        self._document = ""
        self.document = document
        self.service_name = service_name
        self.file_name = file_name
        self.options = options

    @property
    def document(self) -> str:
        return self._document

    @document.setter
    def document(self, document: str):
        # validate base64
        try:
            b64decode(document, validate=True)
            self._document = document
        except binascii.Error:
            # TODO: log this error
            raise binascii.Error(
                "Please make sure your document string is base64 encoded!"
            )

    def as_dict(self) -> RawTransformDocumentRequest:
        """Creates a dict of the object instance.

        Returns:
            RawTransformDocumentResponse: TransformDocumentResponse as dict.
        """
        return RawTransformDocumentRequest(
            document=self.document,
            service_name=self.service_name,
            file_name=self.file_name,
            options=self.options,
        )


class TransformDocumentResponse(BaseModel):
    def __init__(
        self,
        trans_document: str,
        trans_output: Optional[List[str]] = None,
        error: Optional[List[str]] = None,
    ) -> None:
        self._trans_document = ""
        self.trans_document = trans_document
        self.trans_output = trans_output
        self.error = error

    @property
    def trans_document(self) -> str:
        return self._trans_document

    @trans_document.setter
    def trans_document(self, trans_document: str) -> None:
        # validate base64
        try:
            b64decode(trans_document, validate=True)
            self._trans_document = trans_document
        except binascii.Error:
            # TODO: log this error
            raise binascii.Error(
                "Please make sure your document string is base64 encoded!"
            )

    def as_dict(self) -> RawTransformDocumentResponse:
        """Creates a dict of the object instance.

        Returns:
            RawTransformDocumentResponse: TransformDocumentResponse as dict.
        """
        return RawTransformDocumentResponse(
            trans_document=self.trans_document,
            trans_output=self.trans_output,
            error=self.error,
        )


@dataclass
class ListServicesResponse(BaseModel):
    services: List[str]

    def as_dict(self) -> RawListResponse:
        """Creates a dict of the object instance.

        Returns:
            RawListResponse: ListServicesResponse as dict.
        """
        return RawListResponse(services=self.services)


class TransformDocumentPipeRequest(TransformDocumentRequest):
    def __init__(
        self,
        document: str,
        service_name: str,
        services: List[Dict[str, Any]],
        file_name: Optional[str] = None,
        options: Optional[Options] = None,
    ) -> None:
        super().__init__(
            document=document,
            service_name=service_name,
            file_name=file_name,
            options=options,
        )
        self.services = services

    def as_dict(self) -> RawTransformDocumentPipeRequest:
        return RawTransformDocumentPipeRequest(
            document=self.document,
            service_name=self.service_name,
            file_name=self.file_name,
            options=self.options,
            services=self.services,
        )


class TransformDocumentPipeResponse(TransformDocumentResponse):
    def __init__(
        self,
        trans_document: str,
        sender: str,
        trans_output: Optional[List[str]] = None,
        error: Optional[List[str]] = None,
    ):
        super().__init__(
            trans_document=trans_document, trans_output=trans_output, error=error
        )
        self.sender = sender

    def as_dict(self) -> RawTransformDocumentPipeResponse:
        return RawTransformDocumentPipeResponse(
            trans_document=self.trans_document,
            sender=self.sender,
            trans_output=self.trans_output,
            error=self.error,
        )
