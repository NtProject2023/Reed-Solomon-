# Reed-Solomon-

Implementation of the Integer version of the Reed-Solomon Error Correcting code.

The program takes three inputs:(a,µ,M)

1. A ’message’ a to be transmitted as an (large) integer not larger than a given bound M .
2. Bound µ on the maximum fraction of units that can get corrupted during transmission. Consider every integer transmitted as part of the protocol as one ’unit’ of transmission.

Output:
  If the receiver is able to reconstruct the message, the received message will be printed; otherwise, an error message will be printed.
