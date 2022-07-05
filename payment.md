# Transaction Specialist

## Challenge Overview

In this task you'll be crafting a simple payment transaction. While the transaction itself is simple it represents a powerful concept in Algorand, the Transaction.

All interaction with the network is done by creating, signing, and submitting Transactions.

A Payment Transaction is how an account may transfer Algos from themselves to someone else. In order for the transaction to be approved several checks are made at the protocol level including checking the fee is sufficient, the first/last valid rounds are in the correct range for the current state, the sender has enough algos to make the transaction and that the transaction itself was signed correctly.
Prepare for the challenge

## Prepare for this challenge

https://developer.algorand.org/docs/get-details/transactions/

Specifically in the documentation linked above you'll want to familiarize yourself with the suggested parameters present on all transactions and the concept of signing a transaction.


## The Challenge

In this challenge, you need to:

- Get the suggested transaction parameters from an API server
- Construct a Payment Transaction that represents a payment from you, to you, for 1 Algo
- Sign the transaction with the secret key