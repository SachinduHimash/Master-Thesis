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
        "them with small, meaningful adjustments.""Return only the modified text without any additional commentary."
        )  
        return prompt_template  


def calculate_targeting_vulnerable(text,tree_id,rank=1):

    # Define fuzzy input variables
    vulnerability = ctrl.Antecedent(np.arange(0, 100.01, 0.01), 'vulnerability')
    demographic_groups = ctrl.Antecedent(np.arange(0, 100.01, 0.01), 'demographic_groups')
    aid_focus = ctrl.Antecedent(np.arange(0, 100.01, 0.01), 'aid_focus')

    # Define fuzzy output variable
    targeting_vulnerable= ctrl.Consequent(np.arange(0, 100.01, 0.01), 'targeting_vulnerable')

    # Membership functions

    vulnerability['low'] = sigmoid(vulnerability.universe, -0.3, 15)
    vulnerability['medium'] = bell_shaped(vulnerability.universe,40,10)
    vulnerability['high'] = sigmoid(vulnerability.universe, 0.2, 70)

    demographic_groups['low'] = sigmoid(demographic_groups.universe, -0.3, 15)
    demographic_groups['medium'] = bell_shaped(demographic_groups.universe,40,10)
    demographic_groups['high'] = sigmoid(demographic_groups.universe, 0.2, 70)

    aid_focus['low'] = sigmoid(aid_focus.universe, -0.3, 15)
    aid_focus['medium'] = bell_shaped(aid_focus.universe,40,10)
    aid_focus['high'] = sigmoid(aid_focus.universe, 0.2, 70)

    targeting_vulnerable['low'] = sigmoid(targeting_vulnerable.universe, -0.2, 30*rank)
    targeting_vulnerable['medium'] = bell_shaped(targeting_vulnerable.universe,50*rank,10)
    targeting_vulnerable['high'] = sigmoid(targeting_vulnerable.universe, 0.2, 70*rank)
    


    # Define fuzzy rules

    rules = [
        # High alignment across all factors ensures strong targeting of vulnerable populations
        ctrl.Rule(vulnerability['high'] & demographic_groups['high'] & aid_focus['high'], targeting_vulnerable['high']),
        
        # Strong vulnerability and aid focus, but medium demographic alignment
        ctrl.Rule(vulnerability['high'] & demographic_groups['medium'] & aid_focus['high'], targeting_vulnerable['high']),
        
        # Strong vulnerability and demographic alignment, but medium aid focus
        ctrl.Rule(vulnerability['high'] & demographic_groups['high'] & aid_focus['medium'], targeting_vulnerable['high']),
        
        # Medium vulnerability but high demographic alignment and aid focus
        ctrl.Rule(vulnerability['medium'] & demographic_groups['high'] & aid_focus['high'], targeting_vulnerable['high']),
        
        # High vulnerability but others at medium levels, reducing targeting precision
        ctrl.Rule(vulnerability['high'] & demographic_groups['medium'] & aid_focus['medium'], targeting_vulnerable['medium']),
        
        # Medium vulnerability and demographic alignment with strong aid focus
        ctrl.Rule(vulnerability['medium'] & demographic_groups['medium'] & aid_focus['high'], targeting_vulnerable['medium']),
        
        # Medium vulnerability and strong demographic alignment with medium aid focus
        ctrl.Rule(vulnerability['medium'] & demographic_groups['high'] & aid_focus['medium'], targeting_vulnerable['medium']),
        
        # High vulnerability with weak demographic alignment and aid focus weakens targeting
        ctrl.Rule(vulnerability['high'] & demographic_groups['low'] & aid_focus['low'], targeting_vulnerable['medium']),
        
        # Strong demographic alignment but weak vulnerability and aid focus leads to weak targeting
        ctrl.Rule(vulnerability['low'] & demographic_groups['high'] & aid_focus['high'], targeting_vulnerable['medium']),
        
        # Balanced medium values across all inputs give moderate targeting
        ctrl.Rule(vulnerability['medium'] & demographic_groups['medium'] & aid_focus['medium'], targeting_vulnerable['medium']),
        
        # High vulnerability with weak demographic alignment but strong aid focus
        ctrl.Rule(vulnerability['high'] & demographic_groups['low'] & aid_focus['high'], targeting_vulnerable['medium']),
        
        # High demographic alignment but weak vulnerability and aid focus
        ctrl.Rule(vulnerability['low'] & demographic_groups['high'] & aid_focus['medium'], targeting_vulnerable['medium']),
        
        # Strong aid focus but weak vulnerability and demographic alignment
        ctrl.Rule(vulnerability['low'] & demographic_groups['medium'] & aid_focus['high'], targeting_vulnerable['medium']),
        
        # Weak vulnerability but medium demographic alignment and aid focus
        ctrl.Rule(vulnerability['low'] & demographic_groups['medium'] & aid_focus['medium'], targeting_vulnerable['low']),
        
        # Low vulnerability with high demographic alignment but weak aid focus
        ctrl.Rule(vulnerability['low'] & demographic_groups['high'] & aid_focus['low'], targeting_vulnerable['low']),
        
        # High vulnerability with low demographic alignment and low aid focus reduces impact
        ctrl.Rule(vulnerability['high'] & demographic_groups['low'] & aid_focus['medium'], targeting_vulnerable['medium']),
        
        # Medium vulnerability with low demographic alignment and medium aid focus
        ctrl.Rule(vulnerability['medium'] & demographic_groups['low'] & aid_focus['medium'], targeting_vulnerable['low']),
        
        # Medium vulnerability with low demographic alignment and high aid focus
        ctrl.Rule(vulnerability['medium'] & demographic_groups['low'] & aid_focus['high'], targeting_vulnerable['medium']),
        
        # Weak demographic alignment reduces effectiveness despite medium vulnerability and aid focus
        ctrl.Rule(vulnerability['medium'] & demographic_groups['low'] & aid_focus['low'], targeting_vulnerable['low']),
        
        # Weak aid focus and demographic alignment with medium vulnerability reduces targeting
        ctrl.Rule(vulnerability['medium'] & demographic_groups['medium'] & aid_focus['low'], targeting_vulnerable['low']),
        
        # High demographic alignment but low vulnerability and aid focus lowers effectiveness
        ctrl.Rule(vulnerability['low'] & demographic_groups['high'] & aid_focus['medium'], targeting_vulnerable['medium']),
        
        # Low vulnerability and low aid focus significantly weaken targeting despite medium demographics
        ctrl.Rule(vulnerability['low'] & demographic_groups['medium'] & aid_focus['low'], targeting_vulnerable['low']),
        
        # All inputs at low levels indicate weak alignment with targeting vulnerable populations
        ctrl.Rule(vulnerability['low'] & demographic_groups['low'] & aid_focus['low'], targeting_vulnerable['low']),
        
        # Low vulnerability but strong aid focus can still provide moderate targeting
        ctrl.Rule(vulnerability['low'] & demographic_groups['low'] & aid_focus['high'], targeting_vulnerable['medium']),
        
        # Weak demographic alignment and weak vulnerability with medium aid focus
        ctrl.Rule(vulnerability['low'] & demographic_groups['medium'] & aid_focus['medium'], targeting_vulnerable['low']),
        
        # High vulnerability with low demographic alignment but strong aid focus can lead to moderate targeting
        ctrl.Rule(vulnerability['high'] & demographic_groups['low'] & aid_focus['high'], targeting_vulnerable['medium']),
        
        # Medium vulnerability with high demographic alignment but weak aid focus results in weak targeting
        ctrl.Rule(vulnerability['medium'] & demographic_groups['high'] & aid_focus['low'], targeting_vulnerable['medium'])
    ]


    # Control system and simulation
    targeting_vulnerable_ctrl = ctrl.ControlSystem(rules)
    targeting_vulnerable_simulation = ctrl.ControlSystemSimulation(targeting_vulnerable_ctrl)


    
    vulnerability_keywords = [
    "Risk exposure",
    "Social exclusion",
    "Economic instability",
    "Food insecurity",
    "Healthcare access barriers",
    "Marginalization",
    "Climate vulnerability",
    "Mental health risks",
    "Disaster susceptibility",
    "Financial insecurity",
    "Social isolation",
    "Chronic illness",
    "Displacement",
    "Aging population",
    "Discrimination",
    "Gender-based violence",
    "Poverty",
    "Homelessness",
    "Environmental hazards",
    "Community fragility",
    "Digital divide",
    "Limited education opportunities",
    "Health disparities",
    "Lack of social support",
    "Unemployment",
    "Addiction vulnerability",
    "Economic dependency",
    "Victimization",
    "Psychosocial stress",
    "Political instability"
]
    demographic_groups_keywords = [
    "Children",
    "Adolescents",
    "Young adults",
    "Middle-aged adults",
    "Elderly population",
    "Infants",
    "Teenagers",
    "Working professionals",
    "Retirees",
    "Ethnic minorities",
    "Indigenous communities",
    "Immigrants",
    "Refugees",
    "Low-income groups",
    "Wealthy individuals",
    "Single parents",
    "Nuclear families",
    "Extended families",
    "People with disabilities",
    "LGBTQ+ community",
    "Veterans",
    "Migrant workers",
    "Rural populations",
    "Urban dwellers",
    "Suburban residents",
    "Students",
    "Unemployed individuals",
    "Gig economy workers",
    "Religious groups",
    "Political affiliations"
]
    aid_focus_keywords = [
    "Humanitarian assistance",
    "Disaster relief",
    "Emergency response",
    "Food aid",
    "Shelter provision",
    "Medical aid",
    "Education support",
    "Water, sanitation, and hygiene (WASH)",
    "Poverty alleviation",
    "Refugee support",
    "Crisis intervention",
    "Cash assistance",
    "Mental health support",
    "Community resilience",
    "Livelihood programs",
    "Development aid",
    "Economic empowerment",
    "Capacity building",
    "Social protection",
    "Climate adaptation aid",
    "Sustainable development",
    "Healthcare access",
    "Maternal and child health aid",
    "Nutrition programs",
    "Conflict resolution",
    "Housing assistance",
    "Public health campaigns",
    "Gender equality programs",
    "Legal aid",
    "Technology for aid"
]
    
    vulnerability = evaluate_text(text,'vulnerability',vulnerability_keywords)
    demographic_groups = evaluate_text(text,'demographic groups',demographic_groups_keywords)
    aid_focus = evaluate_text(text,'aid focus',aid_focus_keywords)
    
    # Apply evaluation functions
    targeting_vulnerable_simulation.input['vulnerability'] = vulnerability
    targeting_vulnerable_simulation.input['demographic_groups'] = demographic_groups
    targeting_vulnerable_simulation.input['aid_focus'] = aid_focus
        
    # Compute the fuzzy output
    targeting_vulnerable_simulation.compute()
    
    TreeManager.update_node_value_by_name(tree_id,"Targeting Vulnerable Populations",targeting_vulnerable_simulation.output['targeting_vulnerable'])

    alpha_cut = 30.0
    
     
    TreeManager.add_or_update_node(tree_id,'Targeting Vulnerable Populations','Vulnerability',vulnerability,give_prompt('Vulnerability'),alpha_cut)
    TreeManager.add_or_update_node(tree_id,'Targeting Vulnerable Populations','Demographic Groups',demographic_groups,give_prompt('Demographic Groups'),alpha_cut)
    TreeManager.add_or_update_node(tree_id,'Targeting Vulnerable Populations','Aid Focus',aid_focus,give_prompt('Aid Focus'),alpha_cut)
    


    # Output result

    return  targeting_vulnerable_simulation.output['targeting_vulnerable']
