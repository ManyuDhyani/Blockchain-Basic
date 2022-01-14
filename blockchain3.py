import datetime
import hashlib

class block:

    def __init__(self, index, timestamp, data, previousHash):
        self.index = index
        self.timestamp = timestamp
        self.data = data
        self.previousHash = previousHash
        self.nonce = 0
        self.hash = self.calculate_Hash()

    def calculate_Hash(self):
        sha = hashlib.sha1()
        sha.update(
            str(self.index) +
            str(self.timestamp) +
            str(self.data) +
            str(self.previousHash) +
            str(self.nonce)
        )
        return sha.hexdigest()

    def mine_block(self, difficulty):
        while(self.hash[:difficulty] != "0" * difficulty):
            self.hash = self.calculate_Hash()
            self.nonce += 1
        print("Mined Block: ", self.hash)
        return self.hash

    def check_if_mined(self, difficulty):
        new_hash = ""
        self.nonce = 0
        while(new_hash[: difficulty] != "0" * difficulty):
            new_hash = self.calculate_Hash()
            self.nonce += 1
        return new_hash


class blockchain(block):

    def __init__(self):
        #for chain
        self.chain = [self.create_genesis_block()]
        #difficulty will be needed for mining
        self.difficulty = 3

    #first block is genesis block

    def create_genesis_block(self):
        return block(0, datetime.datetime.now(), "Genesis Block", "0")

    def get_latest_block(self):
        return self.chain[len(self.chain) -1]

    def add_block(self, new_block):
        new_block.previousHash =self.get_latest_block().hash
        new_block.mine_block(self.difficulty)
        self.chain.append(new_block)

    def print_chain(self):
        print("Starting Blockchain")
        print("Block Num:", self.chain[0].index, "Data:", self.chain[0].data)
        print("Previous Hash:", self.chain[0].previousHash)
        print("Current Hash", self.chain[0].calculate_Hash())
        for i in range(1, len(self.chain)):
            print("Block Num: ", self.chain[i].index, "Data:", self.chain[i].data)
            print("Previous Hash:", self.chain[i].previousHash)
            print("Current Hash", self.chain[i].mine_block(self.difficulty))

    def is_chain_valid(self):
        for i in range(1, len(self.chain)):
            if self.chain[i].hash != self.chain[i].check_if_mined(self.difficulty):
                print("Current Hash", self.chain[i].hash, "Do not match with mined hash", self.chain[i].check_if_mined(self.difficulty))
                return False
            elif self.chain[i-1].hash != self.chain[i].previousHash:
                print("Previous hash", self.chain[i-1].hash, "Does not match with attribute prev hash", self.chain[i].previousHash )
                return False
        return True
		


#testing the chain

my_coin = blockchain()

print("Mining Block 1....")
my_coin.add_block(block("1", "20/12/2018", 20, "0"))
print("Mining Block 2....")
my_coin.add_block(block("2", "21/12/2018", 70, "0"))
print("Mining Block 3....")
my_coin.add_block(block("3", "21/12/2018", 10, "0"))
print("-----------------------------")
my_coin.print_chain()
print("-----------------------------")
print(my_coin.is_chain_valid())
print("-----------------------------")
my_coin.chain[2].data = 100
my_coin.print_chain()
print(my_coin.is_chain_valid())
print("-----------------------------")



