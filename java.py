from enum import Enum


class AccessModifier(Enum):
    PUBLIC = "public"
    PRIVATE = "private"
    PROTECTED = "protected"
    PACKAGE_PRIVATE = "package-private"