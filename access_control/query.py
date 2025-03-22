"""
Runs several queries on behalf of, each with different values for the attributes to illustrate different subsets of data.
The documents will be queried by different simulated users, each time using having different access control pathways.
"""

import os
import json
import requests

# load authentication info from environment
PERSONAL_API_KEY = os.environ['PERSONAL_API_KEY']
CORPUS_KEY = os.environ['CORPUS_KEY']

# API endpoint
API_ENDPOINT = f"https://api.vectara.io/v2/corpora/{CORPUS_KEY}/query"


USER_DIRECTORY = {
    "justin": {"user_id": "justin", "groups": ["biology", "religion"], "roles": ["student"]},
    "mary": {"user_id": "mary", "groups": ["history", "religion"], "roles": ["professor", "dean"]},
    "ashish": {"user_id": "ashish", "groups": ["physics"], "roles": ["student"]},
    "jun": {"user_id": "jun", "groups": ["history"], "roles": ["analyst"]},
    "eliza": {"user_id": "eliza", "groups": ["physics"], "roles": ["dean"]},
    "stephanie": {"user_id": "stephanie", "groups": ["physics"], "roles": ["pii"]}
}


def authenticate_user(user_id: str) -> dict:
    user_attributes = USER_DIRECTORY.get(user_id)
    return user_attributes


def build_access_control_filter(user_attributes: dict):
    # Build the clause that controls access based on the owner of the docs
    owner_clause = f"doc.owner IN ('global', '{user_attributes.get('user_id')}')"

    # Build the clause that controls access based on the group(s) of the user
    group_clause = "doc.groups is not null"
    user_groups = user_attributes.get('groups') if 'groups' in user_attributes else []
    user_group_checks = list(map(lambda g: f"('{g}' IN doc.groups)", user_groups))
    if user_group_checks:
        group_clause = f"({group_clause}) AND (" + " OR ".join(user_group_checks) + ")"

    # Build the clause that controls access based on the role(s) of the user
    role_clause = f"doc.roles is null"
    user_roles = user_attributes.get('roles') if 'roles' in user_attributes else []
    user_role_checks = list(map(lambda r: f"('{r}' IN doc.roles)", user_roles))
    if user_role_checks:
        role_clause = f"({role_clause}) OR (" + " OR ".join(user_role_checks) + ")"

    # Consolidate the combined groups and roles clause
    group_role_clause = f"({group_clause}) AND ({role_clause})"

    return f"({owner_clause}) OR ({group_role_clause})"



def query(query_str: str, filter_str: str, user_id: str):
    user_attributes = authenticate_user(user_id)

    final_filter_exp = f"({build_access_control_filter(user_attributes)})"
    if filter_str:
        final_filter_exp += f" AND ({filter_str})"

    payload = json.dumps({
        "query": query_str,
        "search": {
            "metadata_filter": final_filter_exp,
            "reranker": {
                "type": "customer_reranker",
                "reranker_name": "Rerank_Multilingual_v1"
            }
        },
        "generation": {
            "generation_preset_name": "mockingbird-1.0-2024-07-16",
            "max_used_search_results": 5,
            "enable_factual_consistency_score": True
        },
        "stream_response": False,
        "save_history": True
    })

    headers = {
        'Content-Type': 'application/json',
        'Accept': 'application/json',
        'x-api-key': PERSONAL_API_KEY
    }

    print(f"[{user_id}]>>> {query_str}")

    response = requests.request("POST", API_ENDPOINT, headers=headers, data=payload)

    print(f"[{user_id}]<<< {json.loads(response.text).get('summary')}")
    print(f"# Filter used: {final_filter_exp}\n\n")


# Tests access based on document ownership
print("####################################")
print("# jun should get an answer, because she is the owner of the document that has the answer")
query("How many faces does the hero have?", None, "jun")

# Tests access based on group membership
print("####################################")
print("# justin should get an answer, because he is in a group that is permitted to see the document that has the answer")
query("How many faces does the hero have?", None, "justin")

# Tests access denied based on group membership
print("####################################")
print("# eliza should not get an answer, because she is not in the groups permitted to see the document that has the answer")
query("How many faces does the hero have?", None, "eliza")

# Tests access denied based on group membership but not having the right role
print("####################################")
print("# ashish should not get an answer, because while he is in the physics group, he does not have the 'pii' or 'dean' role")
query("Did Isaac Newton work on gravity?", None, "ashish")

# Tests access based on group membership and having the right role
print("####################################")
print("# eliza should get an answer, because she is in the physics group and has one of the required roles ('dean')")
query("Did Isaac Newton work on gravity?", None, "eliza")

# Tests access based on globally accessible document
print("####################################")
print("# mary should get an answer, because the document that has the answer is globally available")
query("Why are students not allowed to go to the forbidden forest?", None, "mary")

# Tests access based on both access control and application-specific filtering
print("####################################")
print("# jun should get an answer, because she is in the history group and has one of the required roles, and is querying about the 'lectures' project")
query("What does Osiris symbolize?", "doc.project='lectures'", "jun")

# Tests access denied based on both access control and application-specific filtering
print("####################################")
print("# jun should not get an answer, because while she is in the history group and has one of the required roles, she is querying about the 'labs' project")
query("What does Osiris symbolize?", "doc.project='labs'", "jun")
