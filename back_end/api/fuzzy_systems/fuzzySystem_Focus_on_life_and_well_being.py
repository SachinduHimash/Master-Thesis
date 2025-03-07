# Required imports
import skfuzzy as fuzz
from skfuzzy import control as ctrl
import numpy as np

from ..utils.tree_utils import TreeManager
from ..utils.text_evaluate_utils import evaluate_text
from ..utils.membership_functions import sigmoid,bell_shaped

import matplotlib.pyplot as plt

def give_prompt(keyword):
        prompt_template = (
        f"Take the following text and subtly align it with the concept of {keyword} "
        "without changing its core meaning. Keep the original structure and intent intact, "
        f"but enhance it by naturally incorporating elements related to {keyword}. "
        "Make the additions seamless and non-intrusive, ensuring the original message "
        "remains clear and authentic. Do not replace entire sentences; instead, enrich "
        "them with small, meaningful adjustments."
        )  
        return prompt_template  

def calculate_life_wellbeing(text,tree_id,rank=1):

    # Define fuzzy input variables
    sustainability_of_well_being = ctrl.Antecedent(np.arange(0, 100.01, 0.01), 'sustainability_of_well_being')
    community_resilience = ctrl.Antecedent(np.arange(0, 100.01, 0.01), 'community_resilience')
    preventative_health_measures = ctrl.Antecedent(np.arange(0, 100.01, 0.01), 'preventative_health_measures')
    social_determinants_of_health = ctrl.Antecedent(np.arange(0, 100.01, 0.01), 'social_determinants_of_health')

    # Define fuzzy output variable
    life_wellbeing = ctrl.Consequent(np.arange(0, 100.01, 0.01), 'life_wellbeing')

    # Membership functions

    sustainability_of_well_being['low'] = sigmoid(sustainability_of_well_being.universe, -0.3, 15)
    sustainability_of_well_being['medium'] = bell_shaped(sustainability_of_well_being.universe,40,10)
    sustainability_of_well_being['high'] = sigmoid(sustainability_of_well_being.universe, 0.2, 70)

    community_resilience['low'] = sigmoid(community_resilience.universe, -0.3, 15)
    community_resilience['medium'] = bell_shaped(community_resilience.universe,40,10)
    community_resilience['high'] = sigmoid(community_resilience.universe, 0.2, 70)

    preventative_health_measures['low'] = sigmoid(preventative_health_measures.universe, -0.3, 15)
    preventative_health_measures['medium'] = bell_shaped(preventative_health_measures.universe,40,10)
    preventative_health_measures['high'] = sigmoid(preventative_health_measures.universe, 0.2, 70)

    social_determinants_of_health['low'] = sigmoid(social_determinants_of_health.universe, -0.3, 15)
    social_determinants_of_health['medium'] = bell_shaped(social_determinants_of_health.universe,40,10)
    social_determinants_of_health['high'] = sigmoid(social_determinants_of_health.universe, 0.2, 70)

    life_wellbeing['low'] = sigmoid(life_wellbeing.universe, -0.2, 30*rank)
    life_wellbeing['medium'] = bell_shaped(life_wellbeing.universe,50*rank,10)
    life_wellbeing['high'] = sigmoid(life_wellbeing.universe, 0.2, 70*rank)



    # Define fuzzy rules

    rules = [
        # When all inputs are low
        ctrl.Rule(sustainability_of_well_being['low'] & community_resilience['low'] & preventative_health_measures['low'] & social_determinants_of_health['low'], life_wellbeing['low']),
        ctrl.Rule(sustainability_of_well_being['low'] & community_resilience['low'] & preventative_health_measures['low'] & social_determinants_of_health['medium'], life_wellbeing['low']),
        ctrl.Rule(sustainability_of_well_being['low'] & community_resilience['low'] & preventative_health_measures['low'] & social_determinants_of_health['high'], life_wellbeing['low']),
        ctrl.Rule(sustainability_of_well_being['low'] & community_resilience['low'] & preventative_health_measures['medium'] & social_determinants_of_health['low'], life_wellbeing['low']),
        ctrl.Rule(sustainability_of_well_being['low'] & community_resilience['low'] & preventative_health_measures['medium'] & social_determinants_of_health['medium'], life_wellbeing['low']),
        ctrl.Rule(sustainability_of_well_being['low'] & community_resilience['low'] & preventative_health_measures['medium'] & social_determinants_of_health['high'], life_wellbeing['low']),
        ctrl.Rule(sustainability_of_well_being['low'] & community_resilience['low'] & preventative_health_measures['high'] & social_determinants_of_health['low'], life_wellbeing['low']),
        ctrl.Rule(sustainability_of_well_being['low'] & community_resilience['low'] & preventative_health_measures['high'] & social_determinants_of_health['medium'], life_wellbeing['low']),
        ctrl.Rule(sustainability_of_well_being['low'] & community_resilience['low'] & preventative_health_measures['high'] & social_determinants_of_health['high'], life_wellbeing['low']),
        
        # When sustainability is low but community resilience and health measures are medium or high
        ctrl.Rule(sustainability_of_well_being['low'] & community_resilience['medium'] & preventative_health_measures['low'] & social_determinants_of_health['low'], life_wellbeing['low']),
        ctrl.Rule(sustainability_of_well_being['low'] & community_resilience['medium'] & preventative_health_measures['low'] & social_determinants_of_health['medium'], life_wellbeing['low']),
        ctrl.Rule(sustainability_of_well_being['low'] & community_resilience['medium'] & preventative_health_measures['low'] & social_determinants_of_health['high'], life_wellbeing['medium']),
        ctrl.Rule(sustainability_of_well_being['low'] & community_resilience['medium'] & preventative_health_measures['medium'] & social_determinants_of_health['low'], life_wellbeing['low']),
        ctrl.Rule(sustainability_of_well_being['low'] & community_resilience['medium'] & preventative_health_measures['medium'] & social_determinants_of_health['medium'], life_wellbeing['medium']),
        ctrl.Rule(sustainability_of_well_being['low'] & community_resilience['medium'] & preventative_health_measures['medium'] & social_determinants_of_health['high'], life_wellbeing['medium']),
        ctrl.Rule(sustainability_of_well_being['low'] & community_resilience['medium'] & preventative_health_measures['high'] & social_determinants_of_health['low'], life_wellbeing['medium']),
        ctrl.Rule(sustainability_of_well_being['low'] & community_resilience['medium'] & preventative_health_measures['high'] & social_determinants_of_health['medium'], life_wellbeing['high']),
        ctrl.Rule(sustainability_of_well_being['low'] & community_resilience['medium'] & preventative_health_measures['high'] & social_determinants_of_health['high'], life_wellbeing['high']),
        
        # When sustainability is low and community resilience is high
        ctrl.Rule(sustainability_of_well_being['low'] & community_resilience['high'] & preventative_health_measures['low'] & social_determinants_of_health['low'], life_wellbeing['low']),
        ctrl.Rule(sustainability_of_well_being['low'] & community_resilience['high'] & preventative_health_measures['low'] & social_determinants_of_health['medium'], life_wellbeing['medium']),
        ctrl.Rule(sustainability_of_well_being['low'] & community_resilience['high'] & preventative_health_measures['low'] & social_determinants_of_health['high'], life_wellbeing['medium']),
        ctrl.Rule(sustainability_of_well_being['low'] & community_resilience['high'] & preventative_health_measures['medium'] & social_determinants_of_health['low'], life_wellbeing['low']),
        ctrl.Rule(sustainability_of_well_being['low'] & community_resilience['high'] & preventative_health_measures['medium'] & social_determinants_of_health['medium'], life_wellbeing['medium']),
        ctrl.Rule(sustainability_of_well_being['low'] & community_resilience['high'] & preventative_health_measures['medium'] & social_determinants_of_health['high'], life_wellbeing['high']),
        ctrl.Rule(sustainability_of_well_being['low'] & community_resilience['high'] & preventative_health_measures['high'] & social_determinants_of_health['low'], life_wellbeing['medium']),
        ctrl.Rule(sustainability_of_well_being['low'] & community_resilience['high'] & preventative_health_measures['high'] & social_determinants_of_health['medium'], life_wellbeing['high']),
        ctrl.Rule(sustainability_of_well_being['low'] & community_resilience['high'] & preventative_health_measures['high'] & social_determinants_of_health['high'], life_wellbeing['high']),
        
        # When sustainability is medium and community resilience is low
        ctrl.Rule(sustainability_of_well_being['medium'] & community_resilience['low'] & preventative_health_measures['low'] & social_determinants_of_health['low'], life_wellbeing['low']),
        ctrl.Rule(sustainability_of_well_being['medium'] & community_resilience['low'] & preventative_health_measures['low'] & social_determinants_of_health['medium'], life_wellbeing['low']),
        ctrl.Rule(sustainability_of_well_being['medium'] & community_resilience['low'] & preventative_health_measures['low'] & social_determinants_of_health['high'], life_wellbeing['medium']),
        ctrl.Rule(sustainability_of_well_being['medium'] & community_resilience['low'] & preventative_health_measures['medium'] & social_determinants_of_health['low'], life_wellbeing['low']),
        ctrl.Rule(sustainability_of_well_being['medium'] & community_resilience['low'] & preventative_health_measures['medium'] & social_determinants_of_health['medium'], life_wellbeing['medium']),
        ctrl.Rule(sustainability_of_well_being['medium'] & community_resilience['low'] & preventative_health_measures['medium'] & social_determinants_of_health['high'], life_wellbeing['medium']),
        ctrl.Rule(sustainability_of_well_being['medium'] & community_resilience['low'] & preventative_health_measures['high'] & social_determinants_of_health['low'], life_wellbeing['medium']),
        ctrl.Rule(sustainability_of_well_being['medium'] & community_resilience['low'] & preventative_health_measures['high'] & social_determinants_of_health['medium'], life_wellbeing['medium']),
        ctrl.Rule(sustainability_of_well_being['medium'] & community_resilience['low'] & preventative_health_measures['high'] & social_determinants_of_health['high'], life_wellbeing['high']),
        
        # When sustainability is medium and community resilience is medium
        ctrl.Rule(sustainability_of_well_being['medium'] & community_resilience['medium'] & preventative_health_measures['low'] & social_determinants_of_health['low'], life_wellbeing['low']),
        ctrl.Rule(sustainability_of_well_being['medium'] & community_resilience['medium'] & preventative_health_measures['low'] & social_determinants_of_health['medium'], life_wellbeing['medium']),
        ctrl.Rule(sustainability_of_well_being['medium'] & community_resilience['medium'] & preventative_health_measures['low'] & social_determinants_of_health['high'], life_wellbeing['medium']),
        ctrl.Rule(sustainability_of_well_being['medium'] & community_resilience['medium'] & preventative_health_measures['medium'] & social_determinants_of_health['low'], life_wellbeing['medium']),
        ctrl.Rule(sustainability_of_well_being['medium'] & community_resilience['medium'] & preventative_health_measures['medium'] & social_determinants_of_health['medium'], life_wellbeing['medium']),
        ctrl.Rule(sustainability_of_well_being['medium'] & community_resilience['medium'] & preventative_health_measures['medium'] & social_determinants_of_health['high'], life_wellbeing['high']),
        ctrl.Rule(sustainability_of_well_being['medium'] & community_resilience['medium'] & preventative_health_measures['high'] & social_determinants_of_health['low'], life_wellbeing['medium']),
        ctrl.Rule(sustainability_of_well_being['medium'] & community_resilience['medium'] & preventative_health_measures['high'] & social_determinants_of_health['medium'], life_wellbeing['high']),
        ctrl.Rule(sustainability_of_well_being['medium'] & community_resilience['medium'] & preventative_health_measures['high'] & social_determinants_of_health['high'], life_wellbeing['high']),
        
        # When sustainability is medium and community resilience is high
        ctrl.Rule(sustainability_of_well_being['medium'] & community_resilience['high'] & preventative_health_measures['low'] & social_determinants_of_health['low'], life_wellbeing['medium']),
        ctrl.Rule(sustainability_of_well_being['medium'] & community_resilience['high'] & preventative_health_measures['low'] & social_determinants_of_health['medium'], life_wellbeing['medium']),
        ctrl.Rule(sustainability_of_well_being['medium'] & community_resilience['high'] & preventative_health_measures['low'] & social_determinants_of_health['high'], life_wellbeing['high']),
        ctrl.Rule(sustainability_of_well_being['medium'] & community_resilience['high'] & preventative_health_measures['medium'] & social_determinants_of_health['low'], life_wellbeing['medium']),
        ctrl.Rule(sustainability_of_well_being['medium'] & community_resilience['high'] & preventative_health_measures['medium'] & social_determinants_of_health['medium'], life_wellbeing['high']),
        ctrl.Rule(sustainability_of_well_being['medium'] & community_resilience['high'] & preventative_health_measures['medium'] & social_determinants_of_health['high'], life_wellbeing['high']),
        ctrl.Rule(sustainability_of_well_being['medium'] & community_resilience['high'] & preventative_health_measures['high'] & social_determinants_of_health['low'], life_wellbeing['high']),
        ctrl.Rule(sustainability_of_well_being['medium'] & community_resilience['high'] & preventative_health_measures['high'] & social_determinants_of_health['medium'], life_wellbeing['high']),
        ctrl.Rule(sustainability_of_well_being['medium'] & community_resilience['high'] & preventative_health_measures['high'] & social_determinants_of_health['high'], life_wellbeing['high']),
        
        # When sustainability is high and community resilience is low
        ctrl.Rule(sustainability_of_well_being['high'] & community_resilience['low'] & preventative_health_measures['low'] & social_determinants_of_health['low'], life_wellbeing['low']),
        ctrl.Rule(sustainability_of_well_being['high'] & community_resilience['low'] & preventative_health_measures['low'] & social_determinants_of_health['medium'], life_wellbeing['medium']),
        ctrl.Rule(sustainability_of_well_being['high'] & community_resilience['low'] & preventative_health_measures['low'] & social_determinants_of_health['high'], life_wellbeing['medium']),
        ctrl.Rule(sustainability_of_well_being['high'] & community_resilience['low'] & preventative_health_measures['medium'] & social_determinants_of_health['low'], life_wellbeing['medium']),
        ctrl.Rule(sustainability_of_well_being['high'] & community_resilience['low'] & preventative_health_measures['medium'] & social_determinants_of_health['medium'], life_wellbeing['medium']),
        ctrl.Rule(sustainability_of_well_being['high'] & community_resilience['low'] & preventative_health_measures['medium'] & social_determinants_of_health['high'], life_wellbeing['high']),
        ctrl.Rule(sustainability_of_well_being['high'] & community_resilience['low'] & preventative_health_measures['high'] & social_determinants_of_health['low'], life_wellbeing['high']),
        ctrl.Rule(sustainability_of_well_being['high'] & community_resilience['low'] & preventative_health_measures['high'] & social_determinants_of_health['medium'], life_wellbeing['high']),
        ctrl.Rule(sustainability_of_well_being['high'] & community_resilience['low'] & preventative_health_measures['high'] & social_determinants_of_health['high'], life_wellbeing['high']),
        
        # When sustainability is high and community resilience is medium
        ctrl.Rule(sustainability_of_well_being['high'] & community_resilience['medium'] & preventative_health_measures['low'] & social_determinants_of_health['low'], life_wellbeing['medium']),
        ctrl.Rule(sustainability_of_well_being['high'] & community_resilience['medium'] & preventative_health_measures['low'] & social_determinants_of_health['medium'], life_wellbeing['medium']),
        ctrl.Rule(sustainability_of_well_being['high'] & community_resilience['medium'] & preventative_health_measures['low'] & social_determinants_of_health['high'], life_wellbeing['high']),
        ctrl.Rule(sustainability_of_well_being['high'] & community_resilience['medium'] & preventative_health_measures['medium'] & social_determinants_of_health['low'], life_wellbeing['medium']),
        ctrl.Rule(sustainability_of_well_being['high'] & community_resilience['medium'] & preventative_health_measures['medium'] & social_determinants_of_health['medium'], life_wellbeing['high']),
        ctrl.Rule(sustainability_of_well_being['high'] & community_resilience['medium'] & preventative_health_measures['medium'] & social_determinants_of_health['high'], life_wellbeing['high']),
        ctrl.Rule(sustainability_of_well_being['high'] & community_resilience['medium'] & preventative_health_measures['high'] & social_determinants_of_health['low'], life_wellbeing['high']),
        ctrl.Rule(sustainability_of_well_being['high'] & community_resilience['medium'] & preventative_health_measures['high'] & social_determinants_of_health['medium'], life_wellbeing['high']),
        ctrl.Rule(sustainability_of_well_being['high'] & community_resilience['medium'] & preventative_health_measures['high'] & social_determinants_of_health['high'], life_wellbeing['high']),
    ]



    # Control system and simulation
    life_wellbeing_ctrl = ctrl.ControlSystem(rules)
    life_wellbeing_simulation = ctrl.ControlSystemSimulation(life_wellbeing_ctrl)


    
    sustainability_of_well_being_keywords = [
    "Sustainable living",
    "Holistic wellness",
    "Health equity",
    "Environmental sustainability",
    "Community resilience",
    "Preventative healthcare",
    "Social well-being",
    "Psychological resilience",
    "Physical health sustainability",
    "Work-life balance",
    "Socio-economic stability",
    "Inclusive growth",
    "Ecological impact",
    "Mental health care",
    "Lifelong learning",
    "Social determinants of health",
    "Well-being policies",
    "Public health systems",
    "Cultural sustainability",
    "Intergenerational equity",
    "Urban sustainability",
    "Accessible healthcare",
    "Quality of life metrics",
    "Happiness indices",
    "Emotional well-being",
    "Financial security",
    "Climate resilience",
    "Green spaces and well-being",
    "Sustainable food systems",
    "Healthy communities"
    ]
    community_resilience_keywords = [
    "Disaster preparedness",
    "Emergency response",
    "Social cohesion",
    "Adaptability",
    "Crisis recovery",
    "Sustainable development",
    "Resource management",
    "Infrastructure resilience",
    "Risk mitigation",
    "Community networks",
    "Volunteer engagement",
    "Local governance",
    "Public health systems",
    "Collective problem-solving",
    "Economic stability",
    "Climate adaptation",
    "Civic engagement",
    "Neighborhood safety",
    "Cultural preservation",
    "Equity and inclusion",
    "Social capital",
    "Environmental stewardship",
    "Mental health support",
    "Collaborative leadership",
    "Food security",
    "Water resource management",
    "Green infrastructure",
    "Energy resilience",
    "Disaster risk reduction",
    "Community partnerships"
]
    preventative_health_measures_keywords = [
    "Vaccination programs",
    "Routine screenings",
    "Health education",
    "Disease prevention",
    "Immunization",
    "Regular check-ups",
    "Lifestyle modification",
    "Nutritional counseling",
    "Exercise programs",
    "Stress management",
    "Smoking cessation",
    "Substance abuse prevention",
    "Hygiene practices",
    "Occupational health and safety",
    "Infection control",
    "Community health campaigns",
    "Preventative medicine",
    "Early detection",
    "Health risk assessments",
    "Wellness programs",
    "Chronic disease management",
    "Healthy diet promotion",
    "Environmental health monitoring",
    "Sleep hygiene education",
    "Mental health awareness",
    "Access to clean water",
    "Public health policies",
    "Healthy aging initiatives",
    "Prenatal care",
    "Oral hygiene education"
]
    social_determinants_of_health_keywords = [
    "Access to healthcare",
    "Education quality",
    "Economic stability",
    "Employment opportunities",
    "Income inequality",
    "Housing quality",
    "Neighborhood safety",
    "Environmental conditions",
    "Social support networks",
    "Transportation access",
    "Food security",
    "Access to nutritious foods",
    "Health literacy",
    "Cultural competence",
    "Public policy",
    "Discrimination and bias",
    "Childhood development",
    "Community engagement",
    "Healthcare accessibility",
    "Affordable housing",
    "Physical activity opportunities",
    "Mental health services",
    "Water sanitation",
    "Workplace conditions",
    "Urban planning",
    "Access to technology",
    "Gender equality",
    "Community resources",
    "Violence prevention",
    "Equity in education"
]
    
    sustainability_of_well_being = evaluate_text(text,'sustainability of well being',sustainability_of_well_being_keywords)
    community_resilience = evaluate_text(text,'community resilience',community_resilience_keywords)
    preventative_health_measures = evaluate_text(text,'preventative health measures',preventative_health_measures_keywords)
    social_determinants_of_health = evaluate_text(text,'social determinants of health',social_determinants_of_health_keywords)
    
    # Apply evaluation functions
    life_wellbeing_simulation.input['sustainability_of_well_being'] = sustainability_of_well_being
    life_wellbeing_simulation.input['community_resilience'] = community_resilience
    life_wellbeing_simulation.input['preventative_health_measures'] = preventative_health_measures
    life_wellbeing_simulation.input['social_determinants_of_health'] = social_determinants_of_health   
        
    # Compute the fuzzy output
    life_wellbeing_simulation.compute()
    
    TreeManager.update_node_value_by_name(tree_id,"Focus on Life and Well-being",life_wellbeing_simulation.output['life_wellbeing'])
    
    alpha_cut = 30.0

    TreeManager.add_or_update_node(tree_id,'Focus on Life and Well-being','Sustainability of Well-being',sustainability_of_well_being,give_prompt('Sustainability of Well-being'),alpha_cut)
    TreeManager.add_or_update_node(tree_id,'Focus on Life and Well-being','Community Resilience',community_resilience,give_prompt('Community Resilience'),alpha_cut)
    TreeManager.add_or_update_node(tree_id,'Focus on Life and Well-being','Preventative Health Measures',preventative_health_measures,give_prompt('Preventative Health Measures'),alpha_cut)
    TreeManager.add_or_update_node(tree_id,'Focus on Life and Well-being','Social Determinants of Health',social_determinants_of_health,give_prompt('Social Determinants of Health'),alpha_cut)

    
    
    # Output result

    return  life_wellbeing_simulation.output['life_wellbeing']
