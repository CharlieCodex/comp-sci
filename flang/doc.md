#Flang Language specification
##Examples
I want flang to work something like this.
A "function" object is just basic metadata and a pointer an executable location in memory. Functions are pure and immutable.
calling a function would look like

mov eax, [function location in memory]
jmp eax