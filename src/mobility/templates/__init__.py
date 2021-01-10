from src.mobility.templates.simple_template import SimpleTemplate
from src.mobility.templates.basic_template import BasicTemplate
from src.mobility.templates.intermediate_template import IntermediateTemplate
from src.mobility.templates.advanced_template import AdvancedTemplate

exercise_templates = {
    SimpleTemplate.name: SimpleTemplate,
    BasicTemplate.name: BasicTemplate,
    IntermediateTemplate.name: IntermediateTemplate,
    AdvancedTemplate.name: AdvancedTemplate
}