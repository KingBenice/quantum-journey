# Post for X

Project 3: quantum teleportation in Qiskit. Alice sends a qubit's exact state to Bob with one entangled pair and two normal bits. Bob's check passed in 1024 of 1024 shots. Nothing moves faster than light: the bits travel normally. #QuantumComputing #Qiskit

Attach: histogram.png. Add your GitHub link in a reply.

## Thread version (4 posts)

1/ I teleported a qubit this week, in a simulator on my laptop with Qiskit. What that means: Alice has a qubit in an unknown state. Quantum rules forbid copying it, but she can move it to Bob if they share an entangled pair. 🧵 #QuantumComputing

2/ Alice links her qubit to her half of the pair and measures both. She gets 2 ordinary random bits and sends them to Bob over a normal channel. Her original state is destroyed in the process.

3/ Bob uses the 2 bits to pick a fix: an X gate, a Z gate, both, or nothing. His qubit now holds Alice's exact state. I checked it 1,024 times: 1,024 passes.

4/ No faster-than-light trick: Bob can't finish until the 2 bits arrive. The same idea sits under future quantum networks. Code and circuit diagram on my GitHub: https://github.com/KingBenice/quantum-journey #Qiskit

Attach circuit.png to post 2 and histogram.png to post 3.
