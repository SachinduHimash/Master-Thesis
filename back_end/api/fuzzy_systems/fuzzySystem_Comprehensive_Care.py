# Required imports
import skfuzzy as fuzz
from skfuzzy import control as ctrl
import numpy as np

from ..utils.tree_utils import TreeManager
from ..utils.text_evaluate_utils import evaluate_text
from ..utils.membership_functions import sigmoid,bell_shaped

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

def calculate_comprehensive_care(text,tree_id,rank=1):
    # Define fuzzy input variables
    physical_health_care = ctrl.Antecedent(np.arange(0, 100.01, 0.01), 'physical_health_care')
    mental_health_care = ctrl.Antecedent(np.arange(0, 100.01, 0.01), 'mental_health_care')
    basic_needs = ctrl.Antecedent(np.arange(0, 100.01, 0.01), 'basic_needs')

    # Define fuzzy output variable
    comprehensive_care= ctrl.Consequent(np.arange(0, 100.01, 0.01), 'comprehensive_care')

    # Membership functions

    physical_health_care['low'] = sigmoid(physical_health_care.universe, -0.3, 15)
    physical_health_care['medium'] = bell_shaped(physical_health_care.universe,40,10)
    physical_health_care['high'] = sigmoid(physical_health_care.universe, 0.2, 70)

    mental_health_care['low'] = sigmoid(mental_health_care.universe, -0.3, 15)
    mental_health_care['medium'] = bell_shaped(mental_health_care.universe,40,10)
    mental_health_care['high'] = sigmoid(mental_health_care.universe, 0.2, 70)

    basic_needs['low'] = sigmoid(basic_needs.universe, -0.3, 15)
    basic_needs['medium'] = bell_shaped(basic_needs.universe,40,10)
    basic_needs['high'] = sigmoid(basic_needs.universe, 0.2, 70)

    comprehensive_care['low'] = sigmoid(comprehensive_care.universe, -0.2, 30*rank)
    comprehensive_care['medium'] = bell_shaped(comprehensive_care.universe,50*rank,10)
    comprehensive_care['high'] = sigmoid(comprehensive_care.universe, 0.2, 70*rank)

    # Define fuzzy rules
    rules = [
        # High alignment across all factors ensures strong comprehensive care
        ctrl.Rule(physical_health_care['high'] & mental_health_care['high'] & basic_needs['high'], comprehensive_care['high']),
        
        # Strong physical and mental health care, but medium basic needs
        ctrl.Rule(physical_health_care['high'] & mental_health_care['high'] & basic_needs['medium'], comprehensive_care['high']),
        
        # Strong physical health care and basic needs, but medium mental health care
        ctrl.Rule(physical_health_care['high'] & mental_health_care['medium'] & basic_needs['high'], comprehensive_care['high']),
        
        # Medium physical health care but high mental health care and basic needs
        ctrl.Rule(physical_health_care['medium'] & mental_health_care['high'] & basic_needs['high'], comprehensive_care['high']),
        
        # High physical health care but others at medium levels, reducing comprehensiveness
        ctrl.Rule(physical_health_care['high'] & mental_health_care['medium'] & basic_needs['medium'], comprehensive_care['medium']),
        
        # Medium physical health care and mental health care with strong basic needs
        ctrl.Rule(physical_health_care['medium'] & mental_health_care['medium'] & basic_needs['high'], comprehensive_care['medium']),
        
        # Medium physical health care and strong mental health care with medium basic needs
        ctrl.Rule(physical_health_care['medium'] & mental_health_care['high'] & basic_needs['medium'], comprehensive_care['medium']),
        
        # High physical health care with weak mental health care and basic needs weakens comprehensiveness
        ctrl.Rule(physical_health_care['high'] & mental_health_care['low'] & basic_needs['low'], comprehensive_care['medium']),
        
        # Strong mental health care but weak physical health care and basic needs leads to weak comprehensiveness
        ctrl.Rule(physical_health_care['low'] & mental_health_care['high'] & basic_needs['high'], comprehensive_care['medium']),
        
        # Balanced medium values across all inputs give moderate comprehensiveness
        ctrl.Rule(physical_health_care['medium'] & mental_health_care['medium'] & basic_needs['medium'], comprehensive_care['medium']),
        
        # High physical health care with weak mental health care but strong basic needs
        ctrl.Rule(physical_health_care['high'] & mental_health_care['low'] & basic_needs['high'], comprehensive_care['medium']),
        
        # High mental health care but weak physical health care and basic needs
        ctrl.Rule(physical_health_care['low'] & mental_health_care['high'] & basic_needs['medium'], comprehensive_care['medium']),
        
        # Strong basic needs but weak physical and mental health care
        ctrl.Rule(physical_health_care['low'] & mental_health_care['medium'] & basic_needs['high'], comprehensive_care['medium']),
        
        # Weak physical health care but medium mental health care and basic needs
        ctrl.Rule(physical_health_care['low'] & mental_health_care['medium'] & basic_needs['medium'], comprehensive_care['low']),
        
        # Low physical health care with high mental health care but weak basic needs
        ctrl.Rule(physical_health_care['low'] & mental_health_care['high'] & basic_needs['low'], comprehensive_care['low']),
        
        # High physical health care with low mental health care and low basic needs reduces impact
        ctrl.Rule(physical_health_care['high'] & mental_health_care['low'] & basic_needs['medium'], comprehensive_care['medium']),
        
        # Medium physical health care with low mental health care and medium basic needs
        ctrl.Rule(physical_health_care['medium'] & mental_health_care['low'] & basic_needs['medium'], comprehensive_care['low']),
        
        # Medium physical health care with low mental health care and high basic needs
        ctrl.Rule(physical_health_care['medium'] & mental_health_care['low'] & basic_needs['high'], comprehensive_care['medium']),
        
        # Weak mental health care reduces effectiveness despite medium physical health care and basic needs
        ctrl.Rule(physical_health_care['medium'] & mental_health_care['low'] & basic_needs['low'], comprehensive_care['low']),
        
        # Weak basic needs and mental health care with medium physical health care reduces comprehensiveness
        ctrl.Rule(physical_health_care['medium'] & mental_health_care['medium'] & basic_needs['low'], comprehensive_care['low']),
        
        # High mental health care but low physical health care and basic needs lowers effectiveness
        ctrl.Rule(physical_health_care['low'] & mental_health_care['high'] & basic_needs['medium'], comprehensive_care['medium']),
        
        # Low physical health care and low basic needs significantly weaken comprehensiveness despite medium mental health care
        ctrl.Rule(physical_health_care['low'] & mental_health_care['medium'] & basic_needs['low'], comprehensive_care['low']),
        
        # All inputs at low levels indicate weak alignment with comprehensive care
        ctrl.Rule(physical_health_care['low'] & mental_health_care['low'] & basic_needs['low'], comprehensive_care['low']),
        
        # Low physical health care but strong basic needs can still provide moderate comprehensiveness
        ctrl.Rule(physical_health_care['low'] & mental_health_care['low'] & basic_needs['high'], comprehensive_care['medium']),
        
        # Weak mental health care and weak physical health care with medium basic needs
        ctrl.Rule(physical_health_care['low'] & mental_health_care['medium'] & basic_needs['medium'], comprehensive_care['low']),
        
        # High physical health care with low mental health care but strong basic needs can lead to moderate comprehensiveness
        ctrl.Rule(physical_health_care['high'] & mental_health_care['low'] & basic_needs['high'], comprehensive_care['medium']),
        
        # Medium physical health care with high mental health care but weak basic needs results in weak comprehensiveness
        ctrl.Rule(physical_health_care['medium'] & mental_health_care['high'] & basic_needs['low'], comprehensive_care['medium'])
    ]


    # Control system and simulation
    comprehensive_care_ctrl = ctrl.ControlSystem(rules)
    comprehensive_care_simulation = ctrl.ControlSystemSimulation(comprehensive_care_ctrl)


    
    physical_health_care_keywords = [
    "Primary care",
    "Preventative medicine",
    "Chronic disease management",
    "Emergency medicine",
    "Physical therapy",
    "Rehabilitation services",
    "Sports medicine",
    "Nutrition counseling",
    "Immunization",
    "Medical screenings",
    "Health check-ups",
    "Cardiovascular health",
    "Diabetes care",
    "Orthopedic care",
    "Respiratory therapy",
    "Pain management",
    "Oncology treatment",
    "Surgical procedures",
    "Pediatric care",
    "Geriatric care",
    "Women's health services",
    "Men's health services",
    "Neurology care",
    "Infectious disease control",
    "Public health programs",
    "Medical diagnostics",
    "Occupational health",
    "Telemedicine",
    "Dental care",
    "Home health care"
]
    mental_health_care_keywords = [
    "Psychological well-being",
    "Mental health counseling",
    "Therapy sessions",
    "Cognitive behavioral therapy (CBT)",
    "Mindfulness practices",
    "Depression management",
    "Anxiety treatment",
    "Stress reduction",
    "Trauma-informed care",
    "Substance abuse treatment",
    "Crisis intervention",
    "Suicide prevention",
    "Psychiatric care",
    "Emotional resilience",
    "Social support networks",
    "Self-care strategies",
    "Post-traumatic stress disorder (PTSD) support",
    "Mood disorder management",
    "Community mental health services",
    "Workplace mental health programs",
    "Neurodiversity inclusion",
    "Mental health education",
    "Teletherapy services",
    "Holistic mental wellness",
    "Grief counseling",
    "Family therapy",
    "Support groups",
    "Mental health awareness",
    "Behavioral health services",
    "Sleep hygiene"
]
    basic_needs_keywords = [
    "Food security",
    "Clean water access",
    "Safe housing",
    "Healthcare access",
    "Sanitation facilities",
    "Personal hygiene",
    "Clothing",
    "Shelter",
    "Electricity access",
    "Education",
    "Employment opportunities",
    "Financial stability",
    "Transportation access",
    "Affordable healthcare",
    "Mental health support",
    "Social support networks",
    "Legal protection",
    "Environmental safety",
    "Public safety",
    "Nutrition",
    "Emergency aid",
    "Disaster relief",
    "Hygiene products",
    "Internet access",
    "Childcare services",
    "Elderly care",
    "Community resources",
    "Public assistance programs",
    "Livelihood sustainability",
    "Accessibility services"
]
    
    physical_health_care = evaluate_text(text,'physical health care',physical_health_care_keywords)
    mental_health_care = evaluate_text(text,'mental health care',mental_health_care_keywords)
    basic_needs = evaluate_text(text,'basic needs',basic_needs_keywords)
    
    # Apply evaluation functions
    comprehensive_care_simulation.input['physical_health_care'] = physical_health_care
    comprehensive_care_simulation.input['mental_health_care'] = mental_health_care
    comprehensive_care_simulation.input['basic_needs'] = basic_needs
        
    # Compute the fuzzy output
    comprehensive_care_simulation.compute()
    
    TreeManager.update_node_value_by_name(tree_id,"Comprehensive Care",comprehensive_care_simulation.output['comprehensive_care'])
    
    alpha_cut = 30.0

    TreeManager.add_or_update_node(tree_id,'Comprehensive Care','Physical Health Care',physical_health_care,give_prompt('Physical Health Care'),alpha_cut)
    TreeManager.add_or_update_node(tree_id,'Comprehensive Care','Mental Health Care',mental_health_care,give_prompt('Mental Health Care'),alpha_cut)
    TreeManager.add_or_update_node(tree_id,'Comprehensive Care','Basic Needs',basic_needs,give_prompt('Basic Needs'),alpha_cut)

   
    # Output result

    return  comprehensive_care_simulation.output['comprehensive_care']
