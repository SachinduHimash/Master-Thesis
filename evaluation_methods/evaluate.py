import methods.cosine_similarity as cosine_similarity
import methods.euclidean_distance as euclidean_distance
import methods.shanon_entropy_reduction as shanon_entropy_reduction
from methods.jsd import jensen_shannon 

pre_fuzzy_text = ""
post_fuzzy_text = ""


print("Euclidean Distance: ",euclidean_distance.euclidean_distance(pre_fuzzy_text, post_fuzzy_text))
# print("Cosine Similarity: ",cosine_similarity.cosine_similarity(pre_fuzzy_text, post_fuzzy_text))

# print("Jensen Shanon Divergence: ",jensen_shannon_diverg(pre_fuzzy_text, post_fuzzy_text))
print("Shanon Entropy Reduction: ",shanon_entropy_reduction.shanon_entropy_reduction(pre_fuzzy_text, post_fuzzy_text))

print("JSD :", jensen_shannon(pre_fuzzy_text, post_fuzzy_text))
