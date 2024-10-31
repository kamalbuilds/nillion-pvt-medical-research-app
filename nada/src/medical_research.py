from nada_dsl import *

def nada_main():
    # Define parties
    patient = Party(name="Party1")
    researcher = Party(name="Party2")
    hospital = Party(name="Party3")
    
    # Secure patient inputs
    age = SecretInteger(Input(name="age", party=patient))
    symptoms = SecretInteger(Input(name="symptoms_bitmap", party=patient))
    medication_response = SecretInteger(Input(name="medication_response", party=patient))
    side_effects = SecretInteger(Input(name="side_effects_bitmap", party=patient))
    treatment_duration = SecretInteger(Input(name="treatment_duration", party=patient))
    
    # Research parameters
    target_symptoms = SecretInteger(Input(name="target_symptoms", party=researcher))
    min_treatment_duration = SecretInteger(Input(name="min_duration", party=researcher))
    age_group_min = SecretInteger(Input(name="age_group_min", party=researcher))
    age_group_max = SecretInteger(Input(name="age_group_max", party=researcher))
    
    # Constants
    hundred = Integer(100)
    zero = Integer(0)
    one = Integer(1)
    
    # Calculate match scores using patterns from boolean_ops.py example
    age_in_range = (age >= age_group_min) & (age <= age_group_max)
    age_match = age_in_range.if_else(one, zero)
    
    # Symptoms match using equality comparison
    symptoms_match = (symptoms == target_symptoms).if_else(one, zero)
    
    # Duration match
    duration_match = (treatment_duration >= min_treatment_duration).if_else(one, zero)
    
    # Calculate effectiveness score (0-100)
    effectiveness = medication_response * hundred / Integer(5)
    
    # Calculate side effect severity (0-100)
    side_effect_score = hundred - (side_effects * Integer(20))
    
    # Calculate overall trial match
    match_sum = age_match + symptoms_match + duration_match
    trial_match = (match_sum == Integer(3)).if_else(one, zero)
    
    # Calculate comprehensive score
    trial_score = (
        (effectiveness * Integer(60) / hundred) +
        (side_effect_score * Integer(40) / hundred)
    )
    
    return [
        # Patient outputs (limited)
        Output(trial_match, "eligible_for_trial", patient),
        Output(effectiveness, "treatment_effectiveness", patient),
        
        # Researcher outputs
        Output(trial_match, "patient_eligibility", researcher),
        Output(trial_score, "patient_response_score", researcher),
        Output(effectiveness, "medication_effectiveness", researcher),
        Output(side_effects, "side_effects", researcher),
        
        # Hospital outputs
        Output(trial_match, "patient_trial_match", hospital),
        Output(side_effect_score, "safety_score", hospital)
    ]