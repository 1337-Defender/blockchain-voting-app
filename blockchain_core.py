# blockchain_core.py
import hashlib
import time
import json


class Block:
    def __init__(self, index, timestamp, data, previous_hash, nonce=0):
        self.index = index
        self.timestamp = timestamp
        self.data = data
        self.previous_hash = previous_hash
        self.nonce = nonce
        self.hash = self.calculate_hash()

    def calculate_hash(self):
        block_data_string = json.dumps(self.data, sort_keys=True) if isinstance(self.data, (dict, list)) else str(
            self.data)
        sha = hashlib.sha256()
        sha.update(
            str(self.index).encode('utf-8') +
            str(self.timestamp).encode('utf-8') +
            block_data_string.encode('utf-8') +
            str(self.previous_hash).encode('utf-8') +
            str(self.nonce).encode('utf-8')
        )
        return sha.hexdigest()

    def mine_block(self, difficulty):
        target = '0' * difficulty
        while self.hash[:difficulty] != target:
            self.nonce += 1
            self.hash = self.calculate_hash()
        # print(f"Block Mined (Block #{self.index}): {self.hash} (Nonce: {self.nonce})") # Keep console clean for web app


class Blockchain:
    def __init__(self):
        self.chain = [self.create_genesis_block()]
        self.difficulty = 2
        self.pending_votes = []
        self.candidates = {
            "Candidate Alice": 0,
            "Candidate Bob": 0,
            "Candidate Charlie": 0
        }
        # Voter registration and has_voted status will be managed by app.py
        # in conjunction with the user store (users.json)

    def create_genesis_block(self):
        return Block(0, time.time(), "Genesis Block - Voting System Initialized", "0")

    def get_latest_block(self):
        return self.chain[-1]

    def add_vote_to_pending(self, voter_id, candidate_choice):
        """
        Adds a vote to pending votes. Assumes eligibility checks are done by caller.
        """
        if candidate_choice not in self.candidates:
            return "Error: Invalid candidate choice."

        vote_data = {"voter_id": voter_id, "candidate": candidate_choice, "timestamp": time.time()}
        self.pending_votes.append(vote_data)
        return f"Vote from '{voter_id}' for '{candidate_choice}' added to pending block."

    def mine_pending_votes(self):
        if not self.pending_votes:
            return "No pending votes to mine."

        new_block_data = list(self.pending_votes)
        new_block = Block(
            index=len(self.chain),
            timestamp=time.time(),
            data=new_block_data,
            previous_hash=self.get_latest_block().hash
        )
        new_block.mine_block(self.difficulty)
        self.chain.append(new_block)

        for vote_data in new_block_data:
            if vote_data['candidate'] in self.candidates:
                self.candidates[vote_data['candidate']] += 1

        self.pending_votes = []
        return f"New block #{new_block.index} successfully mined with {len(new_block_data)} vote(s)."

    def get_results(self):
        return self.candidates

    def get_chain_data_for_display(self):
        display_chain = []
        for block in self.chain:
            display_block = {
                "index": block.index,
                "timestamp": time.ctime(block.timestamp),
                "data": block.data,
                "previous_hash": block.previous_hash,
                "hash": block.hash,
                "nonce": block.nonce
            }
            display_chain.append(display_block)
        return display_chain

    def is_chain_valid(self):
        for i in range(1, len(self.chain)):
            current_block = self.chain[i]
            previous_block = self.chain[i - 1]
            if current_block.hash != current_block.calculate_hash(): return False
            if current_block.previous_hash != previous_block.hash: return False
        return True