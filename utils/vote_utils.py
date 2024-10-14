def register_voter(voter_id, voters):
    if voter_id not in voters:
        public_key, private_key = generate_keys()
        voters[voter_id] = {'public_key': public_key, 'private_key': private_key}

def cast_vote(voter_id, candidate_id, votes):
    votes[voter_id] = candidate_id

def get_results(votes):
    results = {}
    for candidate in votes.values():
        results[candidate] = results.get(candidate, 0) + 1
    return results
