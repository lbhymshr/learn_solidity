# learn_solidity
I am currently learning Solidity Smart Contract development from the youtube video https://www.youtube.com/watch?v=M576WGiDBdQ

In this video the instructor is walking step by step creating contracts of increasingly complex nature. I want to use this repository as my library to review these codes as often as needed.

# Changes to Code from lectures
I am not using the exact same code as lecture, instead making tweaks to the code that help me better understand the nature of Solidity. For example -

* In the FundMe.sol, I added modifications that allows the Contract Owner to select how much fund will be withdrawn from Contract Balance instead of withdraawing all the funds at one go
* Created a web3py folder which contains a sample code for python scripts that can create a contract & call functions in the said contract

### Web3Py
The python scripts here are modular enough to create any generic contract - as long as the solidity code contains only one contract defined in it. The way to make it work is as follows - 
* Create a new folder that contains the solidity code with the singular contract defined - using simplestorage as an example
* Set up the .env file (using sample.env) which contains the parametrs for CONTRACT_PATH and CONTRACT_NAME
* Set up a new python virttual environment using the requirements.txt file
* Copy the deploy.py & call_contract.py files into the same folder as CONTRACT_PATH
* Execute the deploy.py script first - this will create 2 json files - compiled_code.json & contract_receipt.json; contract receipt is the file that contains the CONTRACT ADDRESS!
* Execute the call_contract.py to interact with the functions within deployed contract; it runs on a while loop letting you run functions as many times as desired
* Note - Each function call creates a new block, with each block with just 1 transaction in it. 
* Note - View functions don't create new blocks as they just read block state and report it back

Please send me a note if you find any bugs with the Web3y module!
