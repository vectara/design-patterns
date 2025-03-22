# Vectara Attribute Based Access Control - Reference Implementation

## Problem statement
Any system that stores or accesses data needs the ability to enforce access controls so users only see what they are allowed to see. This is also true for Vectara, which can store data from many different sources. Data source systems usually have different access control models

In order to apply access controls in a flexible manner to accommodate the variety of data source systems that feed into Vectara, an Attribute Based Access Control (ABAC) mechanism is provided. This uses a shared responsibility model, where the client application must use the Vectara API appropriately and Vectara enforces the corresponding access control constraints.   
* **Ingest Time** - data objects have metadata attributes applied to them which can be used to enforce access control decisions.
* **Query Time** - user-specific filter expression is applied to specify which data objects the user is permitted to see, in terms of the attributes applied to each data object. Note that the end user who is running the query does not provide this filter expression; rather the application itself provides it, ensuring that the right filter is always applied.

In all cases the end user authenticates to the client application with which they interact. The client application calls Vectara's APIs, authenticating via a service account (API Key or OAuth2 identity). The client application knows which groups, roles, etc an end user has (e.g. via LDAP lookup) and uses that information to construct the necessary filter expression for every query.

The purpose of this reference implementation project is to:
* Explain how Vectara's ABAC approach works
* Provide a working example of doing ABAC that can be applied to a wide variety of applications 
* Provide a baseline that can be easily adapted, with relatively minimal modification, to meet other requirements

Note that this is not the only way to do access control using Vectara. This project represents a common approach that should be representative of many different access control scenarios.


## Access Control Scenarios this Reference Implementation Supports
This reference implementation is flexible enough to handle access control decisions based on data ownership, as well as group and role membership. Common access control pathways this enables are:
* Documents private to an individual and globally accessible documents
* Documents shared at the team/group/organization level
* Shared documents that also require having a specific role
* Additional filtering based on factors not related to access control


## Access Control Framework Specification
Vectara uses query-time filter expressions to allow the client application to specify the access control restrictions. The structure of the filter expression constructed in this access control reference implementation is shown below. Any item prefixed with $ indicates a user-specific value to be substituted at runtime. The `build_access_control_filter` function in `query.py` implements this specification.
```
filter_expr:       (owner_clause OR group_role_clause) AND scope_clause
owner_clause:      (doc.owner in ($user_id, "global"))
group_role_clause: (group_clause AND role_clause)
group_clause:      (doc.groups is not null) AND ($user_group[0] IN doc.groups OR $user_group[1] IN doc.groups OR ...) #for all groups to which a user belongs
role_clause:       (doc.roles is null) OR ($user_role[0] IN doc.roles OR $user_role[1] IN doc.roles OR ...) #for all roles which a user has
scope_clause:      (#application specific filter expression compliant with Vectara filter expression syntax)
```

Notes:
* If no group is assigned to a data object, this implies that the document is viewable only to the owner (or to everyone if the document's owner attribute is set to 'global').
* If no role is assigned to a data object, this implies that the users who are in a permitted group need not also have a permitted role.
* If a role is assigned to a data object, this implies that the users who are in a permitted group must also have a permitted role.
* The filtering logic can be applied at the "part" (i.e. chunk) level as well as the document level. 
* General information on Vectara's filter expressions can be found at https://docs.vectara.com/docs/learn/metadata-search-filtering/filter-overview 


## How to Run this Reference Implementation
```
% pip3 install -r requirements.txt
% export PERSONAL_API_KEY=<ENTER_API_KEY_FROM_CONSOLE>
% export CORPUS_KEY=access_control_test
% python3 setup.py
% python3 index.py
% python3 query.py
% python3 cleanup.py
```
* setup.py - creates the corpus, along with the necessary filter attribute definitions
* index.py - indexes several documents, assigning different metadata attributes to represent different access constraints
* query.py - simulates running several queries by different users, each of whom represent different identities and therefore different levels of access to the documents
* cleanup.py - deletes the corpus (optional)


## Description of the Access Control Scenario in this Reference Implementation
The goal is to enable the following:
* Private documents that only the user who indexed it can see
* Global documents that every user can see
* Documents that only members of a specific group can see
* Documents that only members of a specific group who have a specific role can see
* Usage of filters unrelated to access controls to further restrict the query results beyond the access control restrictions; the 'projects' attribute is used for this

### Simulated Organization
This represents a university with several departments (i.e. groups). There are different types of people within the university (i.e. roles). There are also projects of which people can be a part, to provide an additional way to filter query results.
* Groups: biology, chemistry, computer science, history, religion, physics
* Roles: student, professor, analyst, pii
* Projects: orientation, lectures

### Users
* justin - belongs to 'biology' and 'religion' groups, has 'student' role
* mary - belongs to 'history' and 'religion' groups, has 'professor' and 'dean' roles
* ashish - belongs to 'physics' group, has 'student' role
* jun - belongs to 'history' group, has 'analyst' role
* eliza - belongs to 'physics' group, has 'dean' role
* stephanie - belongs to 'physics' group, has 'pii' role

### Data
* TheGoldenBough.pdf
  * Owner is 'justin'
  * Viewable by justin, and members of 'history' group, but only if they have the 'analyst' role
  * Associated with the 'lectures' project
* TheHerosJourney.pdf
  * Owner is 'jun'
  * Viewable by jun, and members of 'history' and 'religion' groups, regardless of their role
* GreatPhysicists.pdf 
  * Owner is 'stephanie'
  * Viewable by stephanie, and members of 'physics' group, provided that they have either the 'pii' or 'dean' role
* UniversityRules.pdf
  * Owner is 'global', meaning viewable by everyone
  * Associated with the 'orientation' project


## Instructions for how to Implement Specific Access Control Pathways
### Private and Global Documents
TBD

### Team Documents
TBD

### Access Control using Both Groups and Roles 
TBD

### Access Control using Both Groups and Other Attributes
TBD

### Combining Access Control with Other Application-Specific Filters
TBD
