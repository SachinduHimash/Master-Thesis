from langchain_ollama import OllamaLLM
from langchain_core.prompts import ChatPromptTemplate, PromptTemplate
from .utils.tree_utils import TreeManager
from .utils.text_meaning_utils import getTheMeaningofText
from .fuzzy_systems.fuzzySystem_Focus_on_life_and_well_being import calculate_life_wellbeing
from .fuzzy_systems.fuzzySystem_Targeting_Vulnerable_Populations import calculate_targeting_vulnerable
from .fuzzy_systems.fuzzySystem_Comprehensive_Care import calculate_comprehensive_care
from .fuzzy_systems.fuzzySystem_Preserving_Dignity import calculate_preserving_dignity

# Define the template for the conversation
template = """
Answer the question below.
Here is the conversation history:
{context}

Question: {question}

Answer:
"""

# Initialize the model
model = OllamaLLM(model="llama3.2")

# Create a prompt template
prompt_template = PromptTemplate(input_variables=["context", "question"], template=template)

class GlobalData:
    rank_scores = {}


def handle_conversation(data):
    context = ""
    # print("Welcome to the AI chatbot! Type 'exit' to quit.")
    
    # user_input = input("You: ")
    user_input = data['message']
        
    # Format the prompt into a string
    formatted_prompt = prompt_template.format(context=context, question=user_input,max_tokens=300)

    # Pass the formatted string directly to the model
    result = model.invoke(formatted_prompt.strip())  # Strip any excess spaces
    
    # Print the model's response
    # print("Bot:", result)
    
    text_meaning = getTheMeaningofText(result)
    
    tree_id = TreeManager.build_tree()
    
    max_diff = 0
    
    print("text_meaning",text_meaning)
    
    ranked_items = sorted(text_meaning.items(), key=lambda x: x[1], reverse=True)
    GlobalData.rank_scores = {ranked_items[i][0]: 1- (i * 0.1) for i in range(len(ranked_items))}

    print("rank_scores",GlobalData.rank_scores)
    for name,value in text_meaning.items():
        if(max_diff < value):
            max_diff = value
        # if(name != 'Humanity'):
        #     updating_node = TreeManager.get_node(tree_id,name)
        #     TreeManager.update_node_alpha_cut_by_name(tree_id,name,updating_node.alpha_cut)
            
    if(max_diff > 0.1):

        calculate_values(result,tree_id)
        # TreeManager.print_tree(tree_id);
        context += f"\nUser: {user_input}\nAI: {result}"
        result2 = evaluate_nodes(tree_id,context,result)
        # print("result1:",result,"result2",result2)
        tree =  TreeManager.get_tree(tree_id)
        return {"result":result2,"tree":tree,"input":result}
        
    else:
        return {"result":"","input":result}
    
def calculate_values(result,tree_id):
    
    function_mapping = {
        'Focus on Life and Well-being': calculate_life_wellbeing,
        'Targeting Vulnerable Populations': calculate_targeting_vulnerable,
        'Comprehensive Care': calculate_comprehensive_care,
        'Preserving Dignity': calculate_preserving_dignity
    }

    # Call the appropriate function with the assigned value
    for key, value in GlobalData.rank_scores.items():
        if key in function_mapping:
            function_mapping[key](result, tree_id,value)
    
    
def evaluate_nodes(tree_id, context, result):
    cycle = 0
    while True:
        outputThreeData = TreeManager.find_node_with_max_diff_and_least_leaf_value(tree_id)
        print("Evaluating nodes", outputThreeData)

        if outputThreeData is not None and outputThreeData['max_diff_child'] is not None and cycle < 5:
            question = outputThreeData['max_diff_child'].prompt
            formatted_prompt2 = prompt_template.format(context=context, question=question, max_tokens=300)

            result2 = model.invoke(formatted_prompt2.strip())  # Refined response

            calculate_values(result2, tree_id)  # Update fuzzy system with refined answer

            context += f"\nUser: {question}\nAI: {result2}"
            print("result2:", result2)
            cycle += 1
            result = result2  
            
        else:
            print("Final result:", result)
            return result  