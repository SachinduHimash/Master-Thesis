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

def calculate_preserving_dignity(text,tree_id,rank=1):

    # Define fuzzy input variables
    respect_for_human_rights = ctrl.Antecedent(np.arange(0, 100.01, 0.01), 'respect_for_human_rights')
    cultural_sensitivity_and_identity = ctrl.Antecedent(np.arange(0, 100.01, 0.01), 'cultural_sensitivity_and_identity')
    non_discrimination_and_equity = ctrl.Antecedent(np.arange(0, 100.01, 0.01), 'non_discrimination_and_equity')
    avoiding_humiliation_and_dehumanization = ctrl.Antecedent(np.arange(0, 100.01, 0.01), 'avoiding_humiliation_and_dehumanization')

    # Define fuzzy output variable
    preserving_dignity= ctrl.Consequent(np.arange(0, 100.01, 0.01), 'preserving_dignity')

    # Membership functions

    respect_for_human_rights['low'] = sigmoid(respect_for_human_rights.universe, -0.3, 15)
    respect_for_human_rights['medium'] = bell_shaped(respect_for_human_rights.universe,40,10)
    respect_for_human_rights['high'] = sigmoid(respect_for_human_rights.universe, 0.2, 70)

    cultural_sensitivity_and_identity['low'] = sigmoid(cultural_sensitivity_and_identity.universe, -0.3, 15)
    cultural_sensitivity_and_identity['medium'] = bell_shaped(cultural_sensitivity_and_identity.universe,40,10)
    cultural_sensitivity_and_identity['high'] = sigmoid(cultural_sensitivity_and_identity.universe, 0.2, 70)

    non_discrimination_and_equity['low'] = sigmoid(non_discrimination_and_equity.universe, -0.3, 15)
    non_discrimination_and_equity['medium'] = bell_shaped(non_discrimination_and_equity.universe,40,10)
    non_discrimination_and_equity['high'] = sigmoid(non_discrimination_and_equity.universe, 0.2, 70)

    avoiding_humiliation_and_dehumanization['low'] = sigmoid(avoiding_humiliation_and_dehumanization.universe, -0.3, 15)
    avoiding_humiliation_and_dehumanization['medium'] = bell_shaped(avoiding_humiliation_and_dehumanization.universe,40,10)
    avoiding_humiliation_and_dehumanization['high'] = sigmoid(avoiding_humiliation_and_dehumanization.universe, 0.2, 70)

    preserving_dignity['low'] = sigmoid(preserving_dignity.universe, -0.2, 30*rank)
    preserving_dignity['medium'] = bell_shaped(preserving_dignity.universe,50*rank,10)
    preserving_dignity['high'] = sigmoid(preserving_dignity.universe, 0.2, 70*rank)

    # Define fuzzy rules

    rules = [
        # Low Cases
        ctrl.Rule(respect_for_human_rights['low'] & cultural_sensitivity_and_identity['low'] & 
                non_discrimination_and_equity['low'] & avoiding_humiliation_and_dehumanization['low'], 
                preserving_dignity['low']),
        
        ctrl.Rule(respect_for_human_rights['low'] & cultural_sensitivity_and_identity['low'] & 
                non_discrimination_and_equity['low'] & avoiding_humiliation_and_dehumanization['medium'], 
                preserving_dignity['low']),
        
        ctrl.Rule(respect_for_human_rights['low'] & cultural_sensitivity_and_identity['low'] & 
                non_discrimination_and_equity['low'] & avoiding_humiliation_and_dehumanization['high'], 
                preserving_dignity['low']),
        
        ctrl.Rule(respect_for_human_rights['low'] & cultural_sensitivity_and_identity['low'] & 
                non_discrimination_and_equity['medium'] & avoiding_humiliation_and_dehumanization['low'], 
                preserving_dignity['low']),
        
        ctrl.Rule(respect_for_human_rights['low'] & cultural_sensitivity_and_identity['low'] & 
                non_discrimination_and_equity['medium'] & avoiding_humiliation_and_dehumanization['medium'], 
                preserving_dignity['low']),
        
        ctrl.Rule(respect_for_human_rights['low'] & cultural_sensitivity_and_identity['low'] & 
                non_discrimination_and_equity['medium'] & avoiding_humiliation_and_dehumanization['high'], 
                preserving_dignity['medium']),
        
        ctrl.Rule(respect_for_human_rights['low'] & cultural_sensitivity_and_identity['low'] & 
                non_discrimination_and_equity['high'] & avoiding_humiliation_and_dehumanization['low'], 
                preserving_dignity['low']),
        
        ctrl.Rule(respect_for_human_rights['low'] & cultural_sensitivity_and_identity['low'] & 
                non_discrimination_and_equity['high'] & avoiding_humiliation_and_dehumanization['medium'], 
                preserving_dignity['medium']),
        
        ctrl.Rule(respect_for_human_rights['low'] & cultural_sensitivity_and_identity['low'] & 
                non_discrimination_and_equity['high'] & avoiding_humiliation_and_dehumanization['high'], 
                preserving_dignity['medium']),
        
        ctrl.Rule(respect_for_human_rights['low'] & cultural_sensitivity_and_identity['medium'] & 
                non_discrimination_and_equity['low'] & avoiding_humiliation_and_dehumanization['low'], 
                preserving_dignity['low']),
        
        ctrl.Rule(respect_for_human_rights['low'] & cultural_sensitivity_and_identity['medium'] & 
                non_discrimination_and_equity['low'] & avoiding_humiliation_and_dehumanization['medium'], 
                preserving_dignity['low']),
        
        ctrl.Rule(respect_for_human_rights['low'] & cultural_sensitivity_and_identity['medium'] & 
                non_discrimination_and_equity['low'] & avoiding_humiliation_and_dehumanization['high'], 
                preserving_dignity['low']),
        
        ctrl.Rule(respect_for_human_rights['low'] & cultural_sensitivity_and_identity['medium'] & 
                non_discrimination_and_equity['medium'] & avoiding_humiliation_and_dehumanization['low'], 
                preserving_dignity['low']),
        
        ctrl.Rule(respect_for_human_rights['low'] & cultural_sensitivity_and_identity['medium'] & 
                non_discrimination_and_equity['medium'] & avoiding_humiliation_and_dehumanization['medium'], 
                preserving_dignity['low']),
        
        ctrl.Rule(respect_for_human_rights['low'] & cultural_sensitivity_and_identity['medium'] & 
                non_discrimination_and_equity['medium'] & avoiding_humiliation_and_dehumanization['high'], 
                preserving_dignity['medium']),
        
        ctrl.Rule(respect_for_human_rights['low'] & cultural_sensitivity_and_identity['medium'] & 
                non_discrimination_and_equity['high'] & avoiding_humiliation_and_dehumanization['low'], 
                preserving_dignity['low']),
        
        ctrl.Rule(respect_for_human_rights['low'] & cultural_sensitivity_and_identity['medium'] & 
                non_discrimination_and_equity['high'] & avoiding_humiliation_and_dehumanization['medium'], 
                preserving_dignity['medium']),
        
        ctrl.Rule(respect_for_human_rights['low'] & cultural_sensitivity_and_identity['medium'] & 
                non_discrimination_and_equity['high'] & avoiding_humiliation_and_dehumanization['high'], 
                preserving_dignity['medium']),
        
        ctrl.Rule(respect_for_human_rights['low'] & cultural_sensitivity_and_identity['high'] & 
                non_discrimination_and_equity['low'] & avoiding_humiliation_and_dehumanization['low'], 
                preserving_dignity['low']),
        
        ctrl.Rule(respect_for_human_rights['low'] & cultural_sensitivity_and_identity['high'] & 
                non_discrimination_and_equity['low'] & avoiding_humiliation_and_dehumanization['medium'], 
                preserving_dignity['low']),
        
        ctrl.Rule(respect_for_human_rights['low'] & cultural_sensitivity_and_identity['high'] & 
                non_discrimination_and_equity['low'] & avoiding_humiliation_and_dehumanization['high'], 
                preserving_dignity['low']),
        
        ctrl.Rule(respect_for_human_rights['low'] & cultural_sensitivity_and_identity['high'] & 
                non_discrimination_and_equity['medium'] & avoiding_humiliation_and_dehumanization['low'], 
                preserving_dignity['low']),
        
        ctrl.Rule(respect_for_human_rights['low'] & cultural_sensitivity_and_identity['high'] & 
                non_discrimination_and_equity['medium'] & avoiding_humiliation_and_dehumanization['medium'], 
                preserving_dignity['medium']),
        
        ctrl.Rule(respect_for_human_rights['low'] & cultural_sensitivity_and_identity['high'] & 
                non_discrimination_and_equity['medium'] & avoiding_humiliation_and_dehumanization['high'], 
                preserving_dignity['medium']),
        
        ctrl.Rule(respect_for_human_rights['low'] & cultural_sensitivity_and_identity['high'] & 
                non_discrimination_and_equity['high'] & avoiding_humiliation_and_dehumanization['low'], 
                preserving_dignity['low']),
        
        ctrl.Rule(respect_for_human_rights['low'] & cultural_sensitivity_and_identity['high'] & 
                non_discrimination_and_equity['high'] & avoiding_humiliation_and_dehumanization['medium'], 
                preserving_dignity['medium']),
        
        ctrl.Rule(respect_for_human_rights['low'] & cultural_sensitivity_and_identity['high'] & 
                non_discrimination_and_equity['high'] & avoiding_humiliation_and_dehumanization['high'], 
                preserving_dignity['medium']),
        
        # Medium Cases
        ctrl.Rule(respect_for_human_rights['medium'] & cultural_sensitivity_and_identity['medium'] & 
                non_discrimination_and_equity['medium'] & avoiding_humiliation_and_dehumanization['medium'], 
                preserving_dignity['medium']),
        
        ctrl.Rule(respect_for_human_rights['medium'] & cultural_sensitivity_and_identity['medium'] & 
                non_discrimination_and_equity['medium'] & avoiding_humiliation_and_dehumanization['low'], 
                preserving_dignity['medium']),
        
        ctrl.Rule(respect_for_human_rights['medium'] & cultural_sensitivity_and_identity['medium'] & 
                non_discrimination_and_equity['medium'] & avoiding_humiliation_and_dehumanization['high'], 
                preserving_dignity['medium']),
        
        ctrl.Rule(respect_for_human_rights['medium'] & cultural_sensitivity_and_identity['medium'] & 
                non_discrimination_and_equity['low'] & avoiding_humiliation_and_dehumanization['low'], 
                preserving_dignity['medium']),
        
        ctrl.Rule(respect_for_human_rights['medium'] & cultural_sensitivity_and_identity['medium'] & 
                non_discrimination_and_equity['low'] & avoiding_humiliation_and_dehumanization['medium'], 
                preserving_dignity['medium']),
        
        ctrl.Rule(respect_for_human_rights['medium'] & cultural_sensitivity_and_identity['medium'] & 
                non_discrimination_and_equity['low'] & avoiding_humiliation_and_dehumanization['high'], 
                preserving_dignity['medium']),
        
        ctrl.Rule(respect_for_human_rights['medium'] & cultural_sensitivity_and_identity['medium'] & 
                non_discrimination_and_equity['high'] & avoiding_humiliation_and_dehumanization['low'], 
                preserving_dignity['medium']),
        
        ctrl.Rule(respect_for_human_rights['medium'] & cultural_sensitivity_and_identity['medium'] & 
                non_discrimination_and_equity['high'] & avoiding_humiliation_and_dehumanization['medium'], 
                preserving_dignity['medium']),
        
        ctrl.Rule(respect_for_human_rights['medium'] & cultural_sensitivity_and_identity['medium'] & 
                non_discrimination_and_equity['high'] & avoiding_humiliation_and_dehumanization['high'], 
                preserving_dignity['high']),
        
        # Mixed Cases (Low and High)
        ctrl.Rule(respect_for_human_rights['medium'] & cultural_sensitivity_and_identity['low'] & 
                non_discrimination_and_equity['low'] & avoiding_humiliation_and_dehumanization['high'], 
                preserving_dignity['medium']),
        
        ctrl.Rule(respect_for_human_rights['high'] & cultural_sensitivity_and_identity['high'] & 
                non_discrimination_and_equity['high'] & avoiding_humiliation_and_dehumanization['high'], 
                preserving_dignity['high']),
        
        ctrl.Rule(respect_for_human_rights['high'] & cultural_sensitivity_and_identity['high'] & 
                non_discrimination_and_equity['high'] & avoiding_humiliation_and_dehumanization['medium'], 
                preserving_dignity['high']),
        
        ctrl.Rule(respect_for_human_rights['high'] & cultural_sensitivity_and_identity['high'] & 
                non_discrimination_and_equity['high'] & avoiding_humiliation_and_dehumanization['low'], 
                preserving_dignity['high']),
        
        ctrl.Rule(respect_for_human_rights['high'] & cultural_sensitivity_and_identity['high'] & 
                non_discrimination_and_equity['medium'] & avoiding_humiliation_and_dehumanization['high'], 
                preserving_dignity['high']),
        
        ctrl.Rule(respect_for_human_rights['high'] & cultural_sensitivity_and_identity['medium'] & 
                non_discrimination_and_equity['high'] & avoiding_humiliation_and_dehumanization['high'], 
                preserving_dignity['high']),
        
        ctrl.Rule(respect_for_human_rights['high'] & cultural_sensitivity_and_identity['low'] & 
                non_discrimination_and_equity['high'] & avoiding_humiliation_and_dehumanization['high'], 
                preserving_dignity['medium']),
        
        ctrl.Rule(respect_for_human_rights['high'] & cultural_sensitivity_and_identity['medium'] & 
                non_discrimination_and_equity['medium'] & avoiding_humiliation_and_dehumanization['medium'], 
                preserving_dignity['medium']),
        
        ctrl.Rule(respect_for_human_rights['high'] & cultural_sensitivity_and_identity['high'] & 
                non_discrimination_and_equity['low'] & avoiding_humiliation_and_dehumanization['medium'], 
                preserving_dignity['medium']),
    ]


    # Control system and simulation
    preserving_dignity_ctrl = ctrl.ControlSystem(rules)
    preserving_dignity_simulation = ctrl.ControlSystemSimulation(preserving_dignity_ctrl)


    
    respect_for_human_rights_keywords = [
    "Freedom of speech",
    "Equality",
    "Non-discrimination",
    "Right to education",
    "Right to healthcare",
    "Freedom of assembly",
    "Gender equality",
    "Access to justice",
    "Human dignity",
    "Freedom from oppression",
    "Right to privacy",
    "Legal protection",
    "Freedom of religion",
    "Social justice",
    "Right to work",
    "Democratic participation",
    "Protection from torture",
    "Civil rights",
    "Political freedoms",
    "Fair trial",
    "Freedom from slavery",
    "Labor rights",
    "Children’s rights",
    "Indigenous rights",
    "Refugee rights",
    "Disability rights",
    "Cultural rights",
    "Environmental justice",
    "Right to personal security",
    "Freedom of the press"
]
    cultural_sensitivity_and_identity_keywords = [
    "Cultural awareness",
    "Diversity and inclusion",
    "Ethnic heritage",
    "Multiculturalism",
    "Cross-cultural communication",
    "Respect for traditions",
    "Religious tolerance",
    "Indigenous knowledge",
    "Linguistic diversity",
    "Cultural preservation",
    "Intercultural dialogue",
    "Traditional practices",
    "Cultural competency",
    "Identity representation",
    "Heritage protection",
    "Social customs",
    "Folklore and storytelling",
    "Racial and ethnic identity",
    "Gender identity and expression",
    "Community traditions",
    "Culturally responsive education",
    "Historical awareness",
    "Cultural appropriation vs. appreciation",
    "Interfaith harmony",
    "Art and cultural expression",
    "Migrant and refugee integration",
    "Indigenous rights",
    "National identity",
    "Global citizenship",
    "Equity and cultural fairness"
]
    non_discrimination_and_equity_keywords = [
    "Equal opportunity",
    "Social justice",
    "Gender equality",
    "Racial equity",
    "Inclusive policies",
    "Affirmative action",
    "Disability rights",
    "LGBTQ+ inclusion",
    "Workplace diversity",
    "Age equality",
    "Economic justice",
    "Health equity",
    "Equal pay",
    "Fair representation",
    "Accessibility rights",
    "Educational equity",
    "Religious freedom",
    "Anti-racism",
    "Ethnic inclusion",
    "Intersectionality",
    "Legal protections",
    "Freedom from bias",
    "Minority rights",
    "Equity in healthcare",
    "Human rights advocacy",
    "Protection from discrimination",
    "Fair housing policies",
    "Cultural sensitivity",
    "Fair labor practices",
    "Equal justice under law"
]
    avoiding_humiliation_and_dehumanization_keywords = [
    "Human dignity",
    "Respect for individuals",
    "Ethical treatment",
    "Compassion",
    "Empathy",
    "Anti-discrimination",
    "Social inclusion",
    "Cultural sensitivity",
    "Non-stigmatization",
    "Freedom from oppression",
    "Equity and fairness",
    "Protection from abuse",
    "Mental well-being",
    "Psychological safety",
    "Inclusive communication",
    "Diversity and respect",
    "Eliminating bias",
    "Right to self-expression",
    "Consent and autonomy",
    "Restorative justice",
    "Fair representation",
    "Ethical leadership",
    "Trauma-informed care",
    "Respectful discourse",
    "Preventing hate speech",
    "Abolishing stereotypes",
    "Advocacy for vulnerable groups",
    "Human rights protection",
    "Safe and respectful environments",
    "Eliminating marginalization"
]
    
    respect_for_human_rights = evaluate_text(text,'respect for human rights',respect_for_human_rights_keywords)
    cultural_sensitivity_and_identity = evaluate_text(text,'cultural sensitivity and identity',cultural_sensitivity_and_identity_keywords)
    non_discrimination_and_equity = evaluate_text(text,'non discrimination and equity',non_discrimination_and_equity_keywords)
    avoiding_humiliation_and_dehumanization = evaluate_text(text,'avoiding humiliation and dehumanization',avoiding_humiliation_and_dehumanization_keywords)

    
    # Apply evaluation functions
    preserving_dignity_simulation.input['respect_for_human_rights'] = respect_for_human_rights
    preserving_dignity_simulation.input['cultural_sensitivity_and_identity'] = cultural_sensitivity_and_identity
    preserving_dignity_simulation.input['non_discrimination_and_equity'] = non_discrimination_and_equity
    preserving_dignity_simulation.input['avoiding_humiliation_and_dehumanization'] = avoiding_humiliation_and_dehumanization

        
    # Compute the fuzzy output
    preserving_dignity_simulation.compute()
    
    TreeManager.update_node_value_by_name(tree_id,"Preserving Dignity",preserving_dignity_simulation.output['preserving_dignity'])
    
    alpha_cut = 30.0

    TreeManager.add_or_update_node(tree_id,"Preserving Dignity",'Respect for Human Rights',respect_for_human_rights,give_prompt('Respect for Human Rights'),alpha_cut)
    TreeManager.add_or_update_node(tree_id,'Preserving Dignity','Cultural Sensitivity and Identity',cultural_sensitivity_and_identity,give_prompt('Cultural Sensitivity and Identity'),alpha_cut)
    TreeManager.add_or_update_node(tree_id,'Preserving Dignity','Non-Discrimination and Equity',non_discrimination_and_equity,give_prompt('Non-Discrimination and Equity'),alpha_cut)
    TreeManager.add_or_update_node(tree_id,'Preserving Dignity','Avoiding Humiliation and Dehumanization',avoiding_humiliation_and_dehumanization,give_prompt('Avoiding Humiliation and Dehumanization'),alpha_cut)
    
   

    # Output result

    return  preserving_dignity_simulation.output['preserving_dignity']
