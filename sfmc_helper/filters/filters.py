from __future__ import annotations
from datetime import date, datetime
from typing import Literal


SimpleOperator = Literal[
    "beginsWith",
    "between",
    "contains",
    "endsWith",
    "equals",
    "existsInString",
    "existsInStringAsAWord",
    "greaterThan",
    "greaterThanAnniversary",
    "greaterThanOrEqual",
    "IN",
    "isAnniversary",
    "isNotAnniversary",
    "isNotNull",
    "isNull",
    "lessThan",
    "lessThanAnniversary",
    "lessThanOrEqual",
    "like",
    "notContains",
    "notEquals",
    "notExistsInString",
]
LogicalOperator = Literal["AND", "OR"]


class SimpleFilter:  # Renamed for clarity
    def __init__(
        self,
        property: str,
        operator: SimpleOperator,
        value: str | int | date | datetime | None,
        value_type: str | None = None,
    ):
        self.property = property
        self.operator = operator
        self.value = value
        self.value_type = value_type

    def to_xml(self, part_of_complex_filter: bool = False) -> str:
        value_tag = (
            f"<DateValue>{self.value}</DateValue>"
            if self.value_type == "Date"
            else f"<Value>{self.value}</Value>"
        )

        if not part_of_complex_filter:
            return f"""
                <Filter xsi:type="par:SimpleFilterPart" xmlns:par="http://exacttarget.com/wsdl/partnerAPI">
                    <Property>{self.property}</Property>
                    <SimpleOperator>{self.operator}</SimpleOperator>
                    {value_tag} 
                </Filter>
            """
        else:
            return f"""
                <Property>{self.property}</Property>
                <SimpleOperator>{self.operator}</SimpleOperator>
                {value_tag}
                """


class ComplexFilter:  # Renamed for clarity
    def __init__(
        self,
        left_operand: SimpleFilter | ComplexFilter,
        operator: LogicalOperator,
        right_operand: SimpleFilter | ComplexFilter,
    ):
        self.left_operand: SimpleFilter | ComplexFilter = left_operand
        self.operator = operator
        self.right_operand: SimpleFilter | ComplexFilter = right_operand

    def to_xml(self, part_of_complex_filter: bool = False) -> str:
        if not part_of_complex_filter:
            return f"""
            <Filter xsi:type="par:ComplexFilterPart" xmlns:par="http://exacttarget.com/wsdl/partnerAPI">
                <LeftOperand xsi:type="par:{"ComplexFilterPart" if isinstance(self.left_operand, ComplexFilter) else "SimpleFilterPart"}">
                    {self.left_operand.to_xml(True)} 
                </LeftOperand>
                <LogicalOperator>{self.operator}</LogicalOperator>
                <RightOperand xsi:type="par:{"ComplexFilterPart" if isinstance(self.right_operand, ComplexFilter) else "SimpleFilterPart"}">
                    {self.right_operand.to_xml(True)} 
                </RightOperand>
            </Filter>
        """
        else:
            return f"""
                <LeftOperand xsi:type="par:{"ComplexFilterPart" if isinstance(self.left_operand, ComplexFilter) else "SimpleFilterPart"}">
                    {self.left_operand.to_xml(True)} 
                </LeftOperand>
                <LogicalOperator>{self.operator}</LogicalOperator>
                <RightOperand xsi:type="par:{"ComplexFilterPart" if isinstance(self.right_operand, ComplexFilter) else "SimpleFilterPart"}">
                    {self.right_operand.to_xml(True)} 
                </RightOperand>
                """


class FilterHelper:
    @staticmethod
    def from_json(filter_json: dict) -> SimpleFilter | ComplexFilter:
        if "operator" in filter_json and filter_json["operator"] in ["AND", "OR"]:
            return ComplexFilter(
                FilterHelper.from_json(filter_json["leftOperand"]),
                filter_json["operator"],
                FilterHelper.from_json(filter_json["rightOperand"]),
            )
        else:  # SimpleFilter
            value = filter_json.get("value")  # Use .get() to avoid KeyError
            value_type = filter_json.get("valueType")

            # Handle date/datetime value types only if value is present
            if value is not None:
                if value_type == "Date":
                    value = date.fromisoformat(value)
                elif value_type == "DateTime":
                    value = datetime.fromisoformat(value)

            return SimpleFilter(
                filter_json["property"],
                filter_json["simpleOperator"],
                value,  # Pass value (can be None)
                value_type,
            )
