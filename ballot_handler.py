import pyrankvote
from pyrankvote import Ballot
import hashlib


# bush = Candidate("George W. Bush (Republican)")
# gore = Candidate("Al Gore (Democratic)")
# nader = Candidate("Ralph Nader (Green)")

# MD5 IS NOT A SECURE HASH ALGORITHM. THIS HASHER IS ONLY TO SET AN ELECTION ID!
election_name_id_hasher = hashlib.md5()

class Election:
    election_ids = []


    def __init__(self, name, candidates, guild):
        self.name = name
        self.id = hashlib.md5(name.encode('utf-8')).hexdigest()
        self.candiates = []
        self.guild = guild
        self.ballots = []
        for c in candidates:
            self.candiates.append(Candidate(c[0], c[1], c[2]))
        self.num_candidates = len(candidates)

    def get_election(self):
        return self

class Candidate:
    """A candidate in the election."""

    def __init__(self, name: str, id: int, discord_tag: str):
        self.name = name
        self.id = id
        self.tag = discord_tag

    def __str__(self) -> str:
        return self.name

    def __repr__(self) -> str:
        return "<Candidate('%s')>" % self.name

    def __hash__(self):
        return hash(self.name)

    def __eq__(self, other) -> bool:
        if other is None:
            return False

        return self.name == other.name

    def to_string(self) -> str:
        return self.name + ", " + str(self.id) + ", " + self.tag

# candidates = [bush, gore, nader]
# Dictionary - k = (str) name : v = (Candidate) candidate object
candidate_keys = []
candidates = {}

# Bush have most first choice votes, but because Ralph Nader-voters want
# Al Gore if Nader is not elected, the elected candidate is Al Gore
ballots = [
]

def parse_raw_ballot(raw_votes):
    return raw_votes.split(', ')

def cast_ballot(votes):
    ranked = []
    for v in votes:
        candidate = candidates[v]
        ranked.append(candidate)

        # --- Shouldn't need since write-ins aren't permitted ---
        # if v in candidates:
        #     candidate = candidates[v]
        #     ranked.append(candidate)
        # else:
        #     new_candidate = Candidate(v)
        #     ranked.append(new_candidate)
        #     candidates[v] = new_candidate
        #     candidate_keys.append(v)

    ballots.append(Ballot(ranked_candidates=ranked))

def end_election():
    candidates_list = []
    for k in candidate_keys:
        candidates_list.append(candidates[k])
    # You can use your own Candidate and Ballot objects as long as they implement the same properties and methods
    election_result = pyrankvote.instant_runoff_voting(candidates_list, ballots)

    winners = election_result.get_winners()
    # Returns: [<Candidate('Al Gore (Democratic)')>]

    return election_result
# Prints:
"""
ROUND 1
Candidate                      Votes  Status
---------------------------  -------  --------
George W. Bush (Republican)        4  Hopeful
Al Gore (Democratic)               3  Hopeful
Ralph Nader (Green)                2  Rejected

FINAL RESULT
Candidate                      Votes  Status
---------------------------  -------  --------
Al Gore (Democratic)               5  Elected
George W. Bush (Republican)        4  Rejected
Ralph Nader (Green)                0  Rejected
"""