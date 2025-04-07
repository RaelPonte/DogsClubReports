from enum import Enum, auto


class EmailContentType(Enum):
    TEXT = "text"
    HTML = "html"
    BOTH = "both"


class EmailPriority(Enum):
    HIGH = "1"
    NORMAL = "3"
    LOW = "5"


class EntityStatus(Enum):
    ACTIVE = "active"
    INACTIVE = "inactive"
    DELETED = "deleted"


class FilterOperator(Enum):
    EQ = "eq"
    NE = "ne"
    LT = "lt"
    LE = "le"
    GT = "gt"
    GE = "ge"
    BETWEEN = "between"
    BEGINS_WITH = "begins_with"
    CONTAINS = "contains"
