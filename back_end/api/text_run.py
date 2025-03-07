# from .utils.tree_utils import TreeManager
# from .utils.text_meaning_utils import getTheMeaningofText
# from .fuzzy_systems.fuzzySystem_Focus_on_life_and_well_being import calculate_life_wellbeing
# from .fuzzy_systems.fuzzySystem_Targeting_Vulnerable_Populations import calculate_targeting_vulnerale
# from .fuzzy_systems.fuzzySystem_Comprehensive_Care import calculate_comprehensive_care
# from .fuzzy_systems.fuzzySystem_Preserving_Dignity import calculate_preserving_dignity



# def handle_conversation(data):
    
#     user_input = data['message']
        
#     text_meaning = getTheMeaningofText(user_input)
    
#     tree_id = TreeManager.build_tree()
    
#     max_diff = 0
    
#     for name,value in text_meaning.items():
#         if(max_diff < value):
#             max_diff = value
#         if(name != 'Humanity'):
#             updating_node = TreeManager.get_node(tree_id,name)
#             TreeManager.update_node_alpha_cut_by_name(tree_id,name,updating_node.alpha_cut*value)
            
#     if(max_diff > 0.1):

#         calculate_values(user_input,tree_id)
#         # TreeManager.print_tree(tree_id);
#         result2=evaluate_nodes(tree_id,user_input)
#         print(user_input,result2)

#         return {user_input,result2}
        
#     else:
#         return user_input
    
# def calculate_values(result,tree_id):
#     calculate_life_wellbeing(result,tree_id)
#     calculate_targeting_vulnerale(result,tree_id)
#     calculate_comprehensive_care(result,tree_id)
#     calculate_preserving_dignity(result,tree_id)
    
# def evaluate_nodes(tree_id,result):
#     outputThreeData = TreeManager.find_node_with_max_diff_and_least_leaf_value(tree_id)
#     if(outputThreeData is not None):
#         question = outputThreeData['max_diff_child'].prompt
     
#     else:
#         return result