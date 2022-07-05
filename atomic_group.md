# Atomic Group Transaction

## Challenge Overview

In this task you'll be constructing an Atomic Group of transactions.

An Atomic Group of transactions is one that requires all transactions in the group succeed or none of them do.  This is a simple but powerful concept. 

An Atomic Group is created by associating individual transactions with a common `group id`, the group id is computed from a hash of all the transactions in the group and up to 16 transactions may be grouped atomically.  

The AtomicTransactionComposer in the SDKs makes this simple by allowing you to add transactions to some group then execute them all in one call.

## Prepare for this challenge

https://developer.algorand.org/docs/get-details/atomic_transfers/

This link provides details about atomic transfers

https://developer.algorand.org/docs/get-details/atc/

This link provides details about using the AtomicTransactionComposer


## The Challenge

In this challenge, you need to:

- Create an AtomicTransactionComposer instance 
- Add 2 Transactions to the AtomicTransactionComposer  
- Execute the transaction group