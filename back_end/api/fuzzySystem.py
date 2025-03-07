import skfuzzy as fuzz
from skfuzzy import control as ctrl
import numpy as np
from .fuzzy_systems.fuzzySystem_Focus_on_life_and_well_being import calculate_life_wellbeing
from .fuzzy_systems.fuzzySystem_Preserving_Dignity import calculate_preserving_dignity
from .fuzzy_systems.fuzzySystem_Comprehensive_Care import calculate_comprehensive_care
from .fuzzy_systems.fuzzySystem_Targeting_Vulnerable_Populations import calculate_targeting_vulnerable
from .utils.tree_utils import TreeManager

# Define input variables for the overall humanity fuzzy system
focus_on_life_score = ctrl.Antecedent(np.arange(0, 11, 1), 'focus_on_life_score')
vulnerable_population_score = ctrl.Antecedent(np.arange(0, 11, 1), 'vulnerable_population_score')
comprehensive_care_score = ctrl.Antecedent(np.arange(0, 11, 1), 'comprehensive_care_score')
preserving_dignity_score = ctrl.Antecedent(np.arange(0, 11, 1), 'preserving_dignity_score')

# Define output variable for the humanity score
humanity_score = ctrl.Consequent(np.arange(0, 11, 1), 'humanity_score')

# Membership functions for input variables
focus_on_life_score['low'] = fuzz.trimf(focus_on_life_score.universe, [0, 0, 5])
focus_on_life_score['medium'] = fuzz.trimf(focus_on_life_score.universe, [0, 5, 10])
focus_on_life_score['high'] = fuzz.trimf(focus_on_life_score.universe, [5, 10, 10])

vulnerable_population_score['low'] = fuzz.trimf(vulnerable_population_score.universe, [0, 0, 5])
vulnerable_population_score['medium'] = fuzz.trimf(vulnerable_population_score.universe, [0, 5, 10])
vulnerable_population_score['high'] = fuzz.trimf(vulnerable_population_score.universe, [5, 10, 10])

comprehensive_care_score['negative'] = fuzz.trimf(comprehensive_care_score.universe, [0, 0, 5])
comprehensive_care_score['neutral'] = fuzz.trimf(comprehensive_care_score.universe, [0, 5, 10])
comprehensive_care_score['positive'] = fuzz.trimf(comprehensive_care_score.universe, [5, 10, 10])

preserving_dignity_score['low'] = fuzz.trimf(preserving_dignity_score.universe, [0, 0, 5])
preserving_dignity_score['medium'] = fuzz.trimf(preserving_dignity_score.universe, [0, 5, 10])
preserving_dignity_score['high'] = fuzz.trimf(preserving_dignity_score.universe, [5, 10, 10])

# Membership functions for output variable
humanity_score['poor'] = fuzz.trimf(humanity_score.universe, [0, 0, 4])
humanity_score['average'] = fuzz.trimf(humanity_score.universe, [3, 5, 7])
humanity_score['good'] = fuzz.trimf(humanity_score.universe, [6, 10, 10])

# Define fuzzy rules for humanity score based on the four criteria
rule1 = ctrl.Rule(focus_on_life_score['high'] & vulnerable_population_score['high'] & comprehensive_care_score['positive'] & preserving_dignity_score['high'], humanity_score['good'])
rule2 = ctrl.Rule(focus_on_life_score['medium'] | vulnerable_population_score['medium'], humanity_score['average'])
rule3 = ctrl.Rule(focus_on_life_score['low'] & vulnerable_population_score['low'] & comprehensive_care_score['negative'] & preserving_dignity_score['low'], humanity_score['poor'])

# Control system setup
humanity_ctrl = ctrl.ControlSystem([rule1, rule2, rule3])
humanity_simulation = ctrl.ControlSystemSimulation(humanity_ctrl)

def checkValues(data,tree_id):

    x1 = calculate_life_wellbeing(data,tree_id)
    x2 = calculate_targeting_vulnerable(data,tree_id)
    x3 = calculate_comprehensive_care(data,tree_id)
    x4 = calculate_preserving_dignity(data,tree_id)
    
    # Sample inputs for testing the humanity score calculation
    
    humanity_simulation.input['focus_on_life_score'] = x1
    humanity_simulation.input['vulnerable_population_score'] = x2
    humanity_simulation.input['comprehensive_care_score'] = x3
    humanity_simulation.input['preserving_dignity_score'] = x4
    
    print(x1,x2,x3,x4)

    # Compute the fuzzy output for the humanity score
    humanity_simulation.compute()

    # Output result
    print("Humanity Score:", humanity_simulation.output['humanity_score'])
    
    TreeManager.update_node_value_by_name(tree_id,'Focus on Life and Well-being',x1)
    TreeManager.update_node_value_by_name(tree_id,'Targeting Vulnerable Populations',x2)
    TreeManager.update_node_value_by_name(tree_id,'Comprehensive Care',x3)
    TreeManager.update_node_value_by_name(tree_id,'Preserving Dignity',x4)