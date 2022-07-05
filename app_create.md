# Smart Contract Specialist

## Challenge Overview

In this task, you'll be deploying a smart contract.

On Algorand smart contracts have two distinct parts, the approval program (`approval.teal`) and the clear state program (`clear.teal`). The majority of the logic will typically be in the approval program, but the clear state program is there for users to call in the event that they want to forcefully "Opt Out" of the contract and free up any minimum balance requirement they may have had associated with it. A clear state call cannot fail.

The approval program in this challenge is relatively simple. The first time it's deployed it jumps to the "setup" branch, where it stores the first application argument you provided into a global state called "access_code". Now on subsequent calls you must provide the same argument as it's compared to be the same. This smart contract will iterate a "counter" global state upon every successful call.

A smart contract is required to be compiled down to bytecode before being submitted to the network. Depending on how much global and/or local state data the smart contract uses, the schema must be configured and provided with the rest of the transaction parameters (the approval program provided requires just 1 global byteslice and 1 global int). Once the transaction has been successfully committed to a block, the application ID can be found and can be used to further calculate the application account address. Further calls to the now deployed smart contract can be made using the application ID.

## Prepare for this challenge

https://developer.algorand.org/docs/get-details/dapps/smart-contracts/apps/

https://developer.algorand.org/docs/get-details/dapps/smart-contracts/frontend/apps/

## The Challenge

In this challenge, you need to:

- Compile the smart contract to bytecode
- Construct an application call transaction with the correct parameters
- Deploy the smart contract and identify the application ID
- Call the smart contract with the correct parameters, incrementing the counter

